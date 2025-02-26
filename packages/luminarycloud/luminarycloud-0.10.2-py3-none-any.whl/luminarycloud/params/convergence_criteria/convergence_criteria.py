# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from dataclasses import dataclass, field
from typing import Optional
from luminarycloud.params.param_wrappers._lib import ParamGroupWrapper
from luminarycloud._proto.client import simulation_pb2 as clientpb
from luminarycloud._proto.output import output_pb2 as outputpb
from luminarycloud._proto.quantity import quantity_pb2 as quantitypb
from luminarycloud.params.convergence_criteria import StoppingCondition


@dataclass(kw_only=True)
class ConvergenceCriteria(ParamGroupWrapper[clientpb.ConvergenceCriteria]):
    """Criteria for stopping a simulation."""

    max_iterations: int = 2000
    """Maximum number of iterations (or time steps for transient simulations) to run the simulation."""
    max_physical_time: Optional[float] = None
    """Maximum physical time for transient simulations (this is the simulated time, not the wall-clock time)."""
    max_inner_iterations: int = 5
    """Maximum number of inner iterations per time step for transient simulations."""
    stopping_conditions: list[StoppingCondition] = field(default_factory=list)
    """List of stopping conditions."""
    stop_on_any: bool = False
    """If true, the simulation will stop if any stopping condition is satisfied."""

    def to_proto(self, transient: bool) -> clientpb.ConvergenceCriteria:
        _proto = clientpb.ConvergenceCriteria()
        for sc in self.stopping_conditions:
            sc_proto = sc._to_proto()
            if self.stop_on_any:
                sc_proto.op = outputpb.StoppingConditionOp.STOP_COND_OP_ANY
            else:
                sc_proto.op = outputpb.StoppingConditionOp.STOP_COND_OP_ALL
            if transient:
                # Use the stopping conditions for inner iterations instead of stopping the solver.
                _proto.time_step_stopping_condition.append(sc_proto)
            else:
                _proto.stopping_condition.append(sc_proto)

        max_iterations_sc = outputpb.StoppingCondition()
        max_iterations_sc.output.quantity = quantitypb.ITERATION_INDEX
        max_iterations_sc.threshold.value = self.max_iterations
        max_iterations_sc.op = outputpb.StoppingConditionOp.STOP_COND_OP_FORCE
        _proto.stopping_condition.append(max_iterations_sc)

        if transient:
            max_inner_iters_sc = outputpb.StoppingCondition()
            max_inner_iters_sc.output.quantity = quantitypb.ITERATION_INDEX
            max_inner_iters_sc.threshold.value = self.max_inner_iterations
            max_inner_iters_sc.op = outputpb.StoppingConditionOp.STOP_COND_OP_FORCE
            _proto.time_step_stopping_condition.append(max_inner_iters_sc)

        if transient and self.max_physical_time is not None:
            max_time_sc = outputpb.StoppingCondition()
            max_time_sc.output.quantity = quantitypb.PHYSICAL_TIME
            max_time_sc.threshold.value = self.max_physical_time
            max_time_sc.op = outputpb.StoppingConditionOp.STOP_COND_OP_FORCE
            _proto.stopping_condition.append(max_time_sc)

        return _proto

    def _to_proto(self) -> clientpb.ConvergenceCriteria:
        raise RuntimeError("_to_proto not implemented for ConvergenceCriteria")

    @classmethod
    def from_proto(
        cls, proto: clientpb.ConvergenceCriteria, transient: bool
    ) -> "ConvergenceCriteria":
        _wrapper = cls()
        for sc in proto.stopping_condition:
            if sc.output.quantity == quantitypb.ITERATION_INDEX:
                _wrapper.max_iterations = sc.threshold.value
            elif sc.output.quantity == quantitypb.PHYSICAL_TIME:
                _wrapper.max_physical_time = sc.threshold.value
            elif not transient:
                _wrapper.stopping_conditions.append(StoppingCondition.from_proto(sc))
                if sc.op == outputpb.StoppingConditionOp.STOP_COND_OP_ANY:
                    _wrapper.stop_on_any = True

        if transient:
            for sc in proto.time_step_stopping_condition:
                if sc.output.quantity == quantitypb.ITERATION_INDEX:
                    _wrapper.max_inner_iterations = sc.threshold.value
                else:
                    _wrapper.stopping_conditions.append(StoppingCondition.from_proto(sc))
                    if sc.op == outputpb.StoppingConditionOp.STOP_COND_OP_ANY:
                        _wrapper.stop_on_any = True

        return _wrapper

    def _from_proto(self, proto: clientpb.ConvergenceCriteria) -> None:
        raise RuntimeError("_from_proto not implemented for ConvergenceCriteria")
