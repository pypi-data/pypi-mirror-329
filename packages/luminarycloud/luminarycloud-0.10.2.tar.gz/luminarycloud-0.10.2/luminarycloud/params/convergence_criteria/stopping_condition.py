# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from dataclasses import dataclass
from luminarycloud.params.param_wrappers._lib import ParamGroupWrapper
from luminarycloud._proto.output import output_pb2 as outputpb
from luminarycloud.params.outputs import Output, ResidualOutput
from typing import TypeVar


Self = TypeVar("Self")


@dataclass(kw_only=True)
class StoppingCondition(ParamGroupWrapper[outputpb.StoppingCondition]):
    """Stopping condition for the solver"""

    output: Output
    threshold: float

    def _to_proto(self) -> outputpb.StoppingCondition:
        _proto = outputpb.StoppingCondition()
        _proto.output.CopyFrom(self.output._to_proto())
        _proto.threshold.value = self.threshold
        return _proto

    def _from_proto(self, proto: outputpb.StoppingCondition) -> Self:  # type: ignore
        return cls.from_proto(proto)

    @classmethod
    def from_proto(cls, proto: outputpb.StoppingCondition) -> Self:  # type: ignore
        if not proto.output.HasField("residual_properties"):
            raise TypeError("SDK stopping conditions are only compatible with residual outputs.")
        return cls(output=ResidualOutput.from_proto(proto.output), threshold=proto.threshold.value)
