# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
import io
from datetime import datetime
from typing import Optional

from ._client import get_default_client
from ._helpers.timestamp_to_datetime import timestamp_to_datetime
from ._helpers.wait_for_simulation import wait_for_simulation
from ._proto.api.v0.luminarycloud.common import common_pb2 as commonpb
from ._proto.api.v0.luminarycloud.simulation import simulation_pb2 as simulationpb
from ._proto.api.v0.luminarycloud.solution import solution_pb2 as solutionpb
from ._proto.client import simulation_pb2 as clientpb
from ._wrapper import ProtoWrapper, ProtoWrapperBase
from .enum import (
    AveragingType,
    CalculationType,
    QuantityType,
    ResidualNormalization,
    SimulationStatus,
)
from .reference_values import ReferenceValues
from .solution import Solution
from .types import MeshID, ProjectID, SimulationID, Vector3Like
from .types.vector3 import _to_vector3


class _DownloadedTextFile(io.StringIO):
    filename: str

    def __init__(self, file_proto: commonpb.File):
        super().__init__(file_proto.full_contents.decode())
        metadata = file_proto.metadata
        self.filename = metadata.name
        if metadata.ext:
            self.filename += "." + metadata.ext


@ProtoWrapper(simulationpb.Simulation)
class Simulation(ProtoWrapperBase):
    """Represents a simulation object."""

    id: SimulationID
    "Simulation ID."
    name: str
    "Simulation name."
    description: str
    "Simulation description."
    status: SimulationStatus
    "Simulation status. May not reflect current status."
    mesh_id: MeshID
    "ID of the simulation mesh."
    project_id: ProjectID
    "ID of the project containing this simulation."

    _proto: simulationpb.Simulation

    @property
    def create_time(self) -> datetime:
        return timestamp_to_datetime(self._proto.create_time)

    @property
    def update_time(self) -> datetime:
        return timestamp_to_datetime(self._proto.update_time)

    def update(
        self,
        *,
        name: str = None,
    ) -> None:
        """
        Update/Edit simulation attributes.

        Mutates self.

        Parameters
        ----------
        name : str, optional
            New project name.
        """
        req = simulationpb.UpdateSimulationRequest(
            id=self.id,
            name=name,
        )
        res = get_default_client().UpdateSimulation(req)
        self._proto = res.simulation

    def wait(
        self,
        *,
        print_residuals: bool = False,
        interval_seconds: float = 5,
        timeout_seconds: float = float("inf"),
    ) -> SimulationStatus:
        """
        Wait until the simulation is completed, failed, or suspended.

        Parameters
        ----------
        print_residuals : bool, optional
            If true, residual values for the latest completed iteration will be printed.
            Frequency is based on interval_seconds.
        interval : float, optional
            Number of seconds between polls.
        timeout : float, optional
            Number of seconds before timeout.

        Returns
        -------
        luminarycloud.enum.SimulationStatus
            Current status of the simulation.
        """
        wait_for_simulation(
            get_default_client(),
            self._proto,
            print_residuals=print_residuals,
            interval_seconds=interval_seconds,
            timeout_seconds=timeout_seconds,
        )
        self._proto = get_simulation(self.id)._proto
        return self.status

    def refresh(self) -> "Simulation":
        """
        Sync the Simulation object with the backend.

        Returns
        -------
        Simulation
            Updated simulation consistent with the backend.
        """
        self._proto = get_simulation(self.id)._proto
        return self

    def download_global_residuals(
        self,
        normalization: ResidualNormalization = ResidualNormalization.RELATIVE,
    ) -> _DownloadedTextFile:
        """
        Download global residuals in csv format.

        Parameters
        ----------
        normalization : ResidualNormalization, optional
            The type of normalization to use. Default is relative normalization.

        Returns
        -------
        io.StringIO
            Stream of text. The filename can be retrieved from the "filename" attribute of the
            object.

        Examples
        --------
        Create a Pandas dataframe:

        >>> from luminarycloud.enum import ResidualType
        >>> import pandas as pd
        >>> with simulation.download_global_residuals() as dl:
        ...     residuals_df = pd.read_csv(dl)

        Save to disk:

        >>> with download_global_residuals() as dl:
        ...     with open(dl.filename, "wb") as fp:
        ...         fp.write(dl.read())
        """
        req = simulationpb.GetSimulationGlobalResidualsRequest(
            id=self.id,
            residual_normalization=normalization.value,
        )
        res = get_default_client().GetSimulationGlobalResiduals(req)
        return _DownloadedTextFile(res.csv_file)

    def download_surface_output(
        self,
        quantity_type: QuantityType,
        surface_ids: list[str],
        *,
        reference_values: ReferenceValues = None,
        calculation_type: CalculationType = CalculationType.PER_SURFACE,
        frame_id: str = "",
        force_direction: Optional[Vector3Like] = None,
        moment_center: Optional[Vector3Like] = None,
        averaging_type: AveragingType = AveragingType.UNSPECIFIED,
    ) -> _DownloadedTextFile:
        """
        Downloads surface outputs (e.g. lift, drag, ...) in csv format.

        Parameters
        ----------
        quantity_type : luminarycloud.enum.QuantityType
            Surface quantity type to compute (e.g. lift, drag).
        surface_ids : list of str
            List of names of the surfaces to compute the quantities for.
            Should have at least one element.

        Other Parameters
        ----------------
        reference_values : ReferenceValues, optional
            Reference values used for computing forces, moments and
            other non-dimensional output quantities. If not provided, default
            reference values will be used.
        calculation_type : CalculationType, optional
            Whether the calculation should be done for all the surfaces together or each surface
            individually. Default is PER_SURFACE.
        frame_id: str, optional
            The ID of the reference frame that this output should be
            reported in for "force" quantity types.
        force_direction : Vector3Like, optional
            The direction of the query component for "force" quantity types.
            Required for certain quantity types.
        moment_center : Vector3Like, optional
            The center of moment for "force" quantity types.
            Required for certain quantity types. Ignored if not applicable.
        averaging_type : AveragingType, optional
            The averaging method used to compute "surface average" quantity types.
            Ignored if not applicable.

        Returns
        -------
        io.StringIO
            Stream of text. The filename can be retrieved from the "filename" attribute of the
            object.

        Examples
        --------
        Create a Pandas dataframe:

        >>> from luminarycloud.enum import QuantityType
        >>> import pandas as pd
        >>> with simulation.download_surface_output(QuantityType.LIFT, ["0/bound/airfoil"], frame_id="body_frame_id") as dl:
        ...     outputs_df = pd.read_csv(dl)

        Save to disk:

        >>> with simulation.download_surface_output(QuantityType.LIFT, ["0/bound/airfoil"]) as dl:
        ...     with open(dl.filename, "w") as fp:
        ...         fp.write(dl.read())
        """
        req = simulationpb.GetSimulationSurfaceQuantityOutputRequest(
            id=self.id,
            quantity_type=quantity_type.value,
            surface_ids=surface_ids,
            calculation_type=calculation_type.value,
            reference_values=(
                reference_values._to_proto() if reference_values else ReferenceValues()._to_proto()
            ),
            frame_id=frame_id,
            force_direction=_to_vector3(force_direction)._to_proto() if force_direction else None,
            moment_center=_to_vector3(moment_center)._to_proto() if moment_center else None,
            averaging_type=averaging_type.value,
        )
        res = get_default_client().GetSimulationSurfaceQuantityOutput(req)
        return _DownloadedTextFile(res.csv_file)

    def delete(self) -> None:
        """
        Delete the simulation.

        The simulation will be stopped first if running. This operation cannot be reverted and all
        the simulation data will be deleted as part of this request.
        """
        req = simulationpb.DeleteSimulationRequest(id=self.id)
        get_default_client().DeleteSimulation(req)

    def suspend(self) -> None:
        """
        Suspend the simulation.
        """
        req = simulationpb.SuspendSimulationRequest(id=self.id)
        get_default_client().SuspendSimulation(req)

    def list_solutions(self) -> list[Solution]:
        """
        List all solutions for this simulation in ascending order of iteration.
        """
        req = solutionpb.ListSolutionsRequest(simulation_id=self.id)
        res = get_default_client().ListSolutions(req)
        return [Solution(s) for s in res.solutions]

    def get_parameters(self) -> clientpb.SimulationParam:
        req = simulationpb.GetSimulationParametersRequest(id=self.id)
        return get_default_client().GetSimulationParameters(req)


def get_simulation(id: SimulationID) -> Simulation:
    """
    Retrieve a specific simulation by ID.

    Parameters
    ----------
    id : str
        Simulation ID.
    """
    req = simulationpb.GetSimulationRequest(id=id)
    res = get_default_client().GetSimulation(req)
    return Simulation(res.simulation)
