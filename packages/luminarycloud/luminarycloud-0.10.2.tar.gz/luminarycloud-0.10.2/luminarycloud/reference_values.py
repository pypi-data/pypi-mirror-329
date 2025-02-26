# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from dataclasses import dataclass
from ._proto.base.base_pb2 import AdFloatType
from ._proto.output import reference_values_pb2 as refvalpb
from .enum import ReferenceValuesType


@dataclass(kw_only=True)
class ReferenceValues:
    """
    Reference values needed for computing forces, moments and other
    non-dimensional output quantities.
    """

    reference_value_type: ReferenceValuesType = ReferenceValuesType.PRESCRIBE_VALUES
    """
    Method of specification for the reference values used in force and moment
    computations. Default: PRESCRIBE_VALUES
    """

    area_ref: float = 1.0
    "Reference area for computing force and moment coefficients. Default: 1.0"

    length_ref: float = 1.0
    "Reference length for computing moment coefficients. Default: 1.0"

    use_aero_moment_ref_lengths: bool = False
    "Whether to use separate reference lengths for pitching, rolling and yawing moments. Default: False"

    length_ref_pitch: float = 1.0
    "Reference length for computing pitching moment coefficients. Default: 1.0"

    length_ref_roll: float = 1.0
    "Reference length for computing rolling moment coefficients. Default: 1.0"

    length_ref_yaw: float = 1.0
    "Reference length for computing yawing moment coefficients. Default: 1.0"

    p_ref: float = 101325.0
    """
    Absolute static reference pressure for computing force and moment
    coefficients. This value is independent of the simulation reference
    pressure. Default: 101325.0
    """

    t_ref: float = 288.15
    """
    Reference temperature for computing force and moment coefficients.
    Default: 288.15
    """

    v_ref: float = 1.0
    """
    Reference velocity magnitude for computing force and moment coefficients.
    Default: 1.0
    """

    def _to_proto(self) -> refvalpb.ReferenceValues:
        return refvalpb.ReferenceValues(
            reference_value_type=self.reference_value_type.value,
            area_ref=AdFloatType(value=self.area_ref),
            length_ref=AdFloatType(value=self.length_ref),
            use_aero_moment_ref_lengths=self.use_aero_moment_ref_lengths,
            length_ref_pitch=AdFloatType(value=self.length_ref_pitch),
            length_ref_roll=AdFloatType(value=self.length_ref_roll),
            length_ref_yaw=AdFloatType(value=self.length_ref_yaw),
            p_ref=AdFloatType(value=self.p_ref),
            t_ref=AdFloatType(value=self.t_ref),
            v_ref=AdFloatType(value=self.v_ref),
        )
