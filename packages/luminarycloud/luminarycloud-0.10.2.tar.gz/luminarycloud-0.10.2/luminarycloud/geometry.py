# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from typing_extensions import TYPE_CHECKING

import luminarycloud as lc

from ._client import get_default_client
from ._helpers.timestamp_to_datetime import timestamp_to_datetime
from ._proto.api.v0.luminarycloud.geometry import geometry_pb2 as geometrypb
from ._proto.geometry import geometry_pb2 as gpb

from .params.geometry import Surface, Volume
from .tag import Tag
from ._wrapper import ProtoWrapper, ProtoWrapperBase
from .params.geometry import (
    Shape,
    shapes,
)
from .types import Vector3
from .volume_selection import VolumeSelection

if TYPE_CHECKING:
    from .project import Project


@ProtoWrapper(geometrypb.Geometry)
class Geometry(ProtoWrapperBase):
    """Represents a Geometry object."""

    id: str
    "Geometry ID."
    name: str
    "Geometry name."

    _proto: geometrypb.Geometry

    @property
    def create_time(self) -> datetime:
        """
        The time the geometry was created.
        """
        return timestamp_to_datetime(self._proto.create_time)

    def project(self) -> Project:
        """
        The project the geometry belongs to.
        """
        return lc.get_project(self._proto.project_id)

    def modify(self, modification: gpb.Modification) -> None:
        """
        Apply a modification to the geometry.

        Parameters
        ----------
        modification : Modification
            The modification to apply to the geometry.
        """
        req = geometrypb.ModifyGeometryRequest(
            geometry_id=self.id,
            modification=modification,
        )
        get_default_client().ModifyGeometry(req)

    def select_volumes(self, volumes: list[Volume | int]) -> VolumeSelection:
        """
        Select the given volumes in the geometry for modification.

        Parameters
        ----------
        volumes : list[Volume | int]
            The volumes or volume IDs to select. Empty selection is allowed.
        """
        if not isinstance(volumes, list):
            raise TypeError("volumes must be a list")
        return VolumeSelection(self, volumes)

    def add_farfield(self, shape: Shape) -> None:
        """
        Create a farfield feature in the geometry.

        Parameters
        ----------
        shape : Cube | Cylinder | HalfSphere | Sphere | Torus | Cone
            The shape of the farfield.
        """
        create_proto = gpb.Create()
        if isinstance(shape, shapes.Sphere):
            create_proto.sphere.CopyFrom(shape._to_proto())
        elif isinstance(shape, shapes.Cube):
            create_proto.box.CopyFrom(shape._to_proto())
        elif isinstance(shape, shapes.Cylinder):
            create_proto.cylinder.CopyFrom(shape._to_proto())
        elif isinstance(shape, shapes.Torus):
            create_proto.torus.CopyFrom(shape._to_proto())
        elif isinstance(shape, shapes.Cone):
            create_proto.cone.CopyFrom(shape._to_proto())
        elif isinstance(shape, shapes.HalfSphere):
            create_proto.half_sphere.CopyFrom(shape._to_proto())
        else:
            raise TypeError(f"Unsupported shape for farfield: {type(shape)}")
        self.modify(
            modification=gpb.Modification(
                mod_type=gpb.Modification.MODIFICATION_TYPE_CREATE_FEATURE,
                feature=gpb.Feature(
                    id=str(uuid4()),
                    feature_name="Farfield",
                    farfield=gpb.Farfield(
                        create=create_proto,
                    ),
                ),
            )
        )

    def check(self) -> tuple[bool, list[str]]:
        """
        Check the geometry for any issues that may prevent meshing.

        Returns
        -------
        ok : boolean
            If true, the geometry is ready for meshing.

            If false, the geometry contains errors. Inspect issues and resolve
            any errors.
        issues : list[str]
            A list of issues with the geometry.

            When ok=True, issues may be empty or non-empty but contain only
            warning or informational messages. When ok=False, issues will
            contain at least one error message and possibly additional warning
            or informational messages.
        """
        res: geometrypb.CheckGeometryResponse = get_default_client().CheckGeometry(
            geometrypb.CheckGeometryRequest(geometry_id=self.id)
        )
        return res.ok, list(res.issues)

    def create_tag(self, name: str, entities: list[Volume | Surface]) -> None:
        """
        Create a tag in the geometry.

        Parameters
        ----------
        name : str
            The name of the tag to create.
        entities : list of Volumes or Surfaces
            The Volumes and Surfaces to tag.
        """
        volume_ids = []
        surface_ids = []
        for entity in entities:
            if isinstance(entity, Volume):
                volume_ids.append(int(entity.id))
            elif isinstance(entity, Surface):
                surface_ids.append(int(entity._native_id))
            else:
                raise TypeError("entities must be of type Volume or Surface")

        req = geometrypb.ModifyGeometryRequest(
            geometry_id=self.id,
            modification=gpb.Modification(
                mod_type=gpb.Modification.MODIFICATION_TYPE_CREATE_TAG,
                create_or_update_tag=gpb.CreateOrUpdateTag(
                    name=name,
                    bodies=volume_ids,
                    faces=surface_ids,
                ),
            ),
        )
        get_default_client().ModifyGeometry(req)

    def list_tags(self) -> list[Tag]:
        """
        Get the tags currently associated with the geometry.

        Returns
        -------
        list[Tag]
        """
        req = geometrypb.ListTagsRequest(
            geometry_id=self.id,
        )
        res: geometrypb.ListTagsResponse = get_default_client().ListTags(req)
        return [Tag(t) for t in res.tags]

    def list_entities(self) -> tuple[list[Surface], list[Volume]]:
        """
        List all the entities in the geometry.

        Returns
        -------
        surfaces : list[Surface]
            A list of all the surfaces in the geometry.
        volumes : list[Volume]
            A list of all the volumes in the geometry.
        """

        res: geometrypb.ListGeometryEntitiesResponse = get_default_client().ListGeometryEntities(
            geometrypb.ListGeometryEntitiesRequest(geometry_id=self.id)
        )
        surfaces = [
            Surface(
                geometry_id=self.id,
                id=f.id,
                _native_id=f.native_id,
                bbox_min=Vector3(f.bbox_min.x, f.bbox_min.y, f.bbox_min.z),
                bbox_max=Vector3(f.bbox_max.x, f.bbox_max.y, f.bbox_max.z),
            )
            for f in res.faces
        ]
        volumes = [
            Volume(
                geometry_id=self.id,
                id=str(b.id),
                _lcn_id=str(b.lcn_id),
                bbox_min=Vector3(b.bbox_min.x, b.bbox_min.y, b.bbox_min.z),
                bbox_max=Vector3(b.bbox_max.x, b.bbox_max.y, b.bbox_max.z),
            )
            for b in res.bodies
        ]
        return surfaces, volumes

    def list_features(
        self,
    ) -> list[gpb.Feature]:
        """
        List the current features in the geometry.

        Returns
        -------
        features : list[Feature]
            A list of the current features in the geometry.
        """
        req = geometrypb.ListGeometryFeaturesRequest(
            geometry_id=self.id,
        )
        res: geometrypb.ListGeometryFeaturesResponse = get_default_client().ListGeometryFeatures(
            req
        )
        return list(res.features)

    def list_feature_issues(
        self,
    ) -> list[gpb.FeatureIssues]:
        """
        List any issues with features in the geometry.

        Returns
        -------
        feature_issues : list[FeatureIssues]
            A list of any issues with features in the geometry. Issues may be
            informational, warnings or errors.
        """
        req = geometrypb.ListGeometryFeatureIssuesRequest(
            geometry_id=self.id,
        )
        res: geometrypb.ListGeometryFeatureIssuesResponse = (
            get_default_client().ListGeometryFeatureIssues(req)
        )
        return list(res.features_issues)


def get_geometry(id: str) -> Geometry:
    """
    Get a specific geometry with the given ID.

    Parameters
    ----------
    id : str
        Geometry ID.

    Returns
    -------
    Geometry
        The requested Geometry.
    """

    req = geometrypb.GetGeometryRequest(geometry_id=id)
    res: geometrypb.GetGeometryResponse = get_default_client().GetGeometry(req)
    return Geometry(res.geometry)
