from dataclasses import dataclass


@dataclass
class SizingStrategy:
    """Sizing strategy parameters."""

    pass


@dataclass
class MinimalCount(SizingStrategy):
    """
    Minimal sizing strategy parameters.

    If this is used, all other meshing parameters are ignored.
    """

    pass


@dataclass
class TargetCount(SizingStrategy):
    """
    Sizing strategy based on a target number of cells.

    To reach a target number of cells, the edge length specifications will be proportionally scaled
    throughout the mesh. Requested boundary layer profiles will be maintained.
    """

    target_count: int
    "The target number of cells in the mesh"


@dataclass
class MaxCount(SizingStrategy):
    """
    Sizing strategy based on a maximum number of cells.

    If the mesh becomes larger than the max cell count, the mesh will be scaled.
    Requested boundary layer profiles will be maintained.
    """

    max_count: int
    "The maximum number of cells in the mesh"
