from .._proto.base.base_pb2 import AdFloatType, FirstOrderAdType, SecondOrderAdType


class FirstOrderAdFloat(float):
    """An immutable float with first order adjoints/tangents attached."""

    tangent: tuple[float]
    adjoint: tuple[float]

    def __new__(cls, value: float, *extra_args):
        return super().__new__(cls, value)

    def __init__(self, value: float, tangent: tuple[float], adjoint: tuple[float]):
        self.tangent = tuple(float(t) for t in tangent)
        self.adjoint = tuple(float(a) for a in adjoint)


class SecondOrderAdFloat(float):
    """An immutable float with second order adjoints/tangents attached."""

    value: FirstOrderAdFloat
    tangent: tuple[FirstOrderAdFloat]
    adjoint: tuple[FirstOrderAdFloat]

    def __new__(cls, value: FirstOrderAdFloat, *extra_args):
        return super().__new__(cls, value)

    def __init__(
        self,
        value: FirstOrderAdFloat,
        tangent: tuple[FirstOrderAdFloat],
        adjoint: tuple[FirstOrderAdFloat],
    ):
        if not isinstance(value, FirstOrderAdFloat):
            raise TypeError("Value must be a FirstOrderAdFloat")
        for t in tangent:
            if not isinstance(t, FirstOrderAdFloat):
                raise TypeError("Tangent must be a tuple of FirstOrderAdFloat")
        for a in adjoint:
            if not isinstance(a, FirstOrderAdFloat):
                raise TypeError("Adjoint must be a tuple of FirstOrderAdFloat")

        self.value = value
        self.tangent = tangent
        self.adjoint = adjoint


def _to_ad_proto(value: float) -> AdFloatType:
    """Convert a float to an AdFloatType proto."""
    if isinstance(value, FirstOrderAdFloat):
        return AdFloatType(
            first_order=FirstOrderAdType(
                value=float(value),
                tangent=value.tangent,
                adjoint=value.adjoint,
            )
        )
    elif isinstance(value, SecondOrderAdFloat):
        return AdFloatType(
            second_order=SecondOrderAdType(
                value=_to_ad_proto(value.value).first_order,
                tangent=[_to_ad_proto(t).first_order for t in value.tangent],
                adjoint=[_to_ad_proto(a).first_order for a in value.adjoint],
            )
        )
    return AdFloatType(value=float(value))


def _from_ad_proto(proto: AdFloatType) -> float:
    """Convert an AdFloatType proto to a float."""
    if proto.HasField("first_order"):
        return _from_ad_proto_helper(proto.first_order)
    elif proto.HasField("second_order"):
        return _from_ad_proto_helper(proto.second_order)
    elif proto.HasField("value"):
        return proto.value


def _from_ad_proto_helper(proto: FirstOrderAdType | SecondOrderAdType) -> float:
    if isinstance(proto, FirstOrderAdType):
        return FirstOrderAdFloat(
            proto.value,
            proto.tangent,
            proto.adjoint,
        )
    elif isinstance(proto, SecondOrderAdType):
        return SecondOrderAdFloat(
            _from_ad_proto_helper(proto.value),
            tuple(_from_ad_proto_helper(t) for t in proto.tangent),
            tuple(_from_ad_proto_helper(a) for a in proto.adjoint),
        )
