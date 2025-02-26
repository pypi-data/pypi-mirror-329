# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
import json
from contextlib import contextmanager
from dataclasses import dataclass
from itertools import chain
from collections.abc import Iterable, Mapping
from typing import Any, Optional, TypeVar

from google.protobuf.any_pb2 import Any as AnyProto
from google.protobuf.descriptor import Descriptor, FieldDescriptor
from google.protobuf.json_format import MessageToDict

import luminarycloud._proto.condition.condition_pb2 as conditionpb
import luminarycloud._proto.options.options_pb2 as optionspb
from luminarycloud._proto.client.simulation_pb2 import SimulationParam


class ParamMap:
    """
    Provides maps to get the FieldDescriptor for every "param" (see param_registry.py) by name
    or by numner (tag/field number, which is supposed to unique) in the given param group.
    """

    by_name: dict[str, FieldDescriptor]
    by_number: dict[int, FieldDescriptor]

    def __init__(self, param_group: AnyProto):
        self.by_name = dict()
        self.by_number = dict()
        self._build(param_group.DESCRIPTOR)

    def _build(self, param_group_desc: Optional[Descriptor]):
        if param_group_desc is not None:
            if param_group_desc.containing_type is not None:  # to detect map/Entry types
                return self._build(param_group_desc.fields_by_name["value"].message_type)
            for field in param_group_desc.fields:
                if field.name in self.by_name:
                    continue
                if not str.startswith(field.full_name, "luminary.proto.client"):
                    continue
                self.by_name[field.name] = field
                self.by_number[field.number] = field
                self._build(field.message_type)


K = TypeVar("K")
V = TypeVar("V")


class ContextMap(Mapping[K, V]):
    """
    A utility class which implements a Mapping (i.e. dict) interface as a stack of context frames.

    Writes only write to the topmost frame, while reads look at each from frame top to bottom and
    return the first hit. Frames can be pushed and popped onto/from the stack.
    """

    _frames: list[dict[type[K], type[V]]]
    _current_frame: dict[type[K], type[V]]

    def __init__(self):
        self._current_frame = dict()
        self._frames = [self._current_frame]

    @contextmanager
    def scope(self):
        """
        Pushes a new frame on enter, and pops on exit.

        Examples
        --------
        >>> with context_map.scope():
        >>>     context_map[k] = v
        >>>     assert context_map[k] == v
        >>> assert context_map[k] != v
        """
        self.push()
        yield self
        self.pop()

    def push(self) -> None:
        """Pushes a new frame onto the stack"""
        self._current_frame = dict()
        self._frames.append(self._current_frame)

    def pop(self) -> None:
        """Pops the topmost frame from the stack"""
        if len(self._frames) == 1:
            raise IndexError
        self._frames.pop()
        self._current_frame = self._frames[-1]

    def __getitem__(self, key: type[K]) -> Optional[type[V]]:
        for frame in reversed(self._frames):
            if key in frame:
                return frame[key]
        return None

    def __setitem__(self, key: type[K], value: type[V]) -> None:
        self._current_frame[key] = value

    def __iter__(self):
        return chain(*reversed(self._frames))

    def __len__(self):
        return len(self._frames)


class CondHelper:
    @dataclass
    class _Node:
        """
        Represents an actual field in an instance of client params. Unlike the "param" it is
        an instance of, a node has a value, a parent, and can be active/inactive.
        """

        name: str
        "Param name"
        parent_name: Optional[str]
        "Param name of parent"
        value: Any
        is_active: Optional[bool]

    def __init__(self):
        self.params = ParamMap(SimulationParam)
        self.node_by_name = ContextMap[str, self._Node]()
        self.node_by_number = ContextMap[int, self._Node]()

    def prune(self, tree: dict[str, Any]) -> dict[str, Any]:
        """
        Takes a dict of client parameters and returns a pruned tree, with inactive nodes and empty
        values removed.
        """
        # Scan subtree to register all nodes.
        self._scan_subtree(tree, None)
        # Then, prune, using our registered nodes to evaluate conds.
        return self._prune_subtree(tree)

    def _scan_subtree(self, subtree: dict[str, Any], parent_name: Optional[str]) -> None:
        """
        From the root, traverses the tree to register all nodes, ignoring "repeated" and
        "map" fields (we will only recurse into those fields after pushing a new frame onto the node
        maps).
        """
        for key, value in subtree.items():
            param = self.params.by_name.get(key, None)
            if param is None:
                continue
            node = self._Node(name=key, parent_name=parent_name, value=value, is_active=None)

            if param.message_type is not None and param.label != FieldDescriptor.LABEL_REPEATED:
                self._scan_subtree(value, param.name)

            self.node_by_name[param.name] = node
            self.node_by_number[param.number] = node

    def _prune_subtree(self, subtree: dict[str, Any]) -> dict[str, Any]:
        """
        Prunes the tree, using the node maps to evaluate the conds.
        """
        pruned_tree = dict()
        for key, value in subtree.items():
            param = self.params.by_name.get(key, None)
            if (
                param is None or key == "surface_name"
            ):  # "surface_name" is repeated twice in the tree...
                pruned_tree[key] = value
                continue
            node = self.node_by_name[key]
            if self._is_node_active(node):
                if param.message_type is None or not str.startswith(
                    param.message_type.full_name, "luminary.proto.client"
                ):
                    if not (isinstance(value, Iterable) and len(value) == 0):
                        pruned_tree[key] = value
                elif key == "physics":
                    pruned_tree[key] = [self._prune_single_physics(subtree, v) for v in value]
                elif param.label == FieldDescriptor.LABEL_REPEATED:
                    # map types show up as REPEATED in descriptor, so we need to distinguish
                    if isinstance(value, dict) and len(value) > 0:
                        pruned_tree[key] = {k: self._prune_repeated(v) for k, v in value.items()}
                    elif isinstance(value, Iterable) and len(value) > 0:
                        pruned_tree[key] = [self._prune_repeated(v) for v in value]
                else:
                    pruned_value = self._prune_subtree(value)
                    if len(pruned_value) > 0:
                        pruned_tree[key] = pruned_value
        return pruned_tree

    def _prune_repeated(self, value: Any) -> dict[str, Any]:
        """Prunes a single element of a repeated field."""
        if not isinstance(value, dict):
            return value
        with self.node_by_name.scope():
            with self.node_by_number.scope():
                return self.prune(value)

    def _prune_single_physics(
        self, root: dict[str, Any], physics: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Prunes a single physics object of the repeated physics field

        Attempts to find the material associated with the physics, and if it finds one, scans the
        material subtree to register all material properties in the node context before calling
        prune() on the physics.
        """
        try:
            physics_id = physics["physics_identifier"]["id"]
            material_id = self._get_material_id_by_physics_id(root, physics_id)
            material = self._get_material_by_id(root, material_id)
        except (KeyError, StopIteration, TypeError):
            material = None
        with self.node_by_name.scope():
            with self.node_by_number.scope():
                if material is not None:
                    self._scan_subtree(material, None)
                return self.prune(physics)

    def _get_material_id_by_physics_id(
        self, root: dict[str, Any], physics_id: str
    ) -> dict[str, Any]:
        volume_id = self._get_volume_id_by_physics_id(root, physics_id)
        return self._get_material_id_by_volume_id(root, volume_id)

    def _get_volume_id_by_physics_id(self, root: dict[str, Any], physics_id: str) -> str:
        entity_relationships = root["entity_relationships"]
        return next(
            link["volume_identifier"]["id"]
            for link in entity_relationships["volume_physics_relationship"]
            if link["physics_identifier"]["id"] == physics_id
        )

    def _get_material_id_by_volume_id(self, root: dict[str, Any], volume_id: str) -> str:
        entity_relationships = root["entity_relationships"]
        return next(
            link["material_identifier"]["id"]
            for link in entity_relationships["volume_material_relationship"]
            if link["volume_identifier"]["id"] == volume_id
        )

    def _get_material_by_id(self, root: dict[str, Any], material_id: str) -> dict[str, Any]:
        return next(
            m for m in root["material_entity"] if m["material_identifier"]["id"] == material_id
        )

    def _is_node_active(self, node: "_Node") -> bool:
        """
        Checks if a node is active.

        Checks the parent first, and then the conds. Only does this once.
        """
        if node.is_active is None:
            if node.parent_name is not None:
                parent = self.node_by_name[node.parent_name]
                if not self._is_node_active(parent):
                    node.is_active = False
                    return False
            cond = get_cond(self.params.by_name[node.name])
            node.is_active = self._check_cond(cond)
        return node.is_active

    def _check_cond(self, cond: conditionpb.Condition) -> bool:
        type = cond.WhichOneof("typ")
        if type is None:
            return True
        if type == "choice":
            return self._check_choice(cond.choice)
        elif type == "boolean":
            return self._check_boolean(cond.boolean)
        elif type == "allof":
            return all(self._check_cond(c) for c in cond.allof.cond)
        elif type == "anyof":
            return any(self._check_cond(c) for c in cond.anyof.cond)
        elif type == "not":
            return not self._check_cond(getattr(cond, "not").cond)
        elif type == "tag":
            return self._check_tag(cond.tag)
        elif type == "false":
            return (
                True  # CondFalse is generally used to control visibility in UI and can be ignored
            )
        return False

    def _check_choice(self, cond_choice: conditionpb.Choice) -> bool:
        name = cond_choice.param_name
        node = self.node_by_name[name]
        if node is None:
            param = self.params.by_name[name]
            return param == cond_choice.tag
        return self._is_node_active(node) and node.value == cond_choice.name

    def _check_boolean(self, cond_boolean: conditionpb.TrueFalse) -> bool:
        tag = cond_boolean.param_name_tag
        node = self.node_by_number[tag]
        if node is None:
            param = self.params.by_number[tag]
            return bool(param)
        return self._is_node_active(node) and bool(node.value)

    def _check_tag(self, cond_tag: conditionpb.Tag) -> bool:
        name = cond_tag.tag_name
        node = self.node_by_name[name]
        return node is not None and self._is_node_active(node)


def params_to_dict(sim_params: SimulationParam) -> dict[str, Any]:
    tree = MessageToDict(
        sim_params,
        preserving_proto_field_name=True,
        including_default_value_fields=False,
    )
    helper = CondHelper()
    return helper.prune(tree)


def params_to_str(sim_params: SimulationParam) -> str:
    return json.dumps(params_to_dict(sim_params), indent=4)


def get_cond(param: FieldDescriptor) -> conditionpb.Condition:
    return param.GetOptions().Extensions[optionspb.cond]


def get_default(param: FieldDescriptor) -> Any:
    dfl = param.GetOptions().Extensions[optionspb.default_value]
    type = dfl.WhichOneof("typ")
    if type == "boolval":
        return dfl.boolval
    elif type == "choice":
        return dfl.choice
    elif type == "intval":
        return dfl.intval
    elif type == "strval":
        return dfl.strval
    elif type == "real":
        return dfl.real
    elif type == "vector3":
        return dfl.vector3
    return None
