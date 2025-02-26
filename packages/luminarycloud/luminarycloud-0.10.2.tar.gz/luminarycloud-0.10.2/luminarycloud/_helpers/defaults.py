# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from typing import Any

from google.protobuf.any_pb2 import Any as AnyPB
from google.protobuf.descriptor import FieldDescriptor

import luminarycloud._proto.base.base_pb2 as basepb
import luminarycloud._proto.options.options_pb2 as optionspb


def _reset_defaults(params):
    for field in params.DESCRIPTOR.fields:
        if field.label == FieldDescriptor.LABEL_REPEATED:
            for nested in getattr(params, field.name):
                _reset_defaults(nested)
        else:
            _set_default(params, field.name)
            if field.message_type is not None:
                _reset_defaults(getattr(params, field.name))


def _set_default(params: AnyPB, name: str) -> Any:
    field = params.DESCRIPTOR.fields_by_name[name]
    dfl: optionspb.Value = field.GetOptions().Extensions[optionspb.default_value]
    type = dfl.WhichOneof("typ")
    if type == "boolval":
        setattr(params, name, dfl.boolval)
    elif type == "choice":
        setattr(params, name, dfl.choice)
    elif type == "strval":
        setattr(params, name, dfl.strval)
    elif type == "intval":
        param: basepb.Int = getattr(params, name)
        param.value = dfl.intval
    elif type == "real":
        param: basepb.AdFloatType = getattr(params, name)
        param.CopyFrom(dfl.real)
    elif type == "vector3":
        param: basepb.Vector3 = getattr(params, name)
        param.CopyFrom(dfl.vector3)
    return None
