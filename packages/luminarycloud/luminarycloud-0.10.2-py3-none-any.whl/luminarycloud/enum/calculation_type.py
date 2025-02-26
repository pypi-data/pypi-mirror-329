# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
from enum import IntEnum
from .._proto.api.v0.luminarycloud.simulation import simulation_pb2


class CalculationType(IntEnum):
    """
    Represents a calculation type when calculating surface outputs.

    Attributes
    ----------
    UNSPECIFIED
    AGGREGATE
        Calculate a single value for the surfaces altogether.
    PER_SURFACE
        Calculate a separate value for each surface.
    """

    UNSPECIFIED = simulation_pb2.CalculationType.CALCULATION_TYPE_UNSPECIFIED
    AGGREGATE = simulation_pb2.CalculationType.CALCULATION_TYPE_AGGREGATE
    PER_SURFACE = simulation_pb2.CalculationType.CALCULATION_TYPE_PER_SURFACE
