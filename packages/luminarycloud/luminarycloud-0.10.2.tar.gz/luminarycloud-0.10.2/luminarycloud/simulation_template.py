# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
from datetime import datetime
from os import PathLike
from typing import Optional, Union
from difflib import Differ

from .enum import TableType
from ._client import get_default_client
from ._helpers.simulation_params_from_json import simulation_params_from_json_path
from ._helpers.timestamp_to_datetime import timestamp_to_datetime
from ._proto.api.v0.luminarycloud.simulation_template import (
    simulation_template_pb2 as simtemplatepb,
)
from ._proto.client import simulation_pb2 as clientpb
from ._wrapper import ProtoWrapper, ProtoWrapperBase
from .types import SimulationTemplateID
from .tables import RectilinearTable
from .simulation_param import SimulationParam


@ProtoWrapper(simtemplatepb.SimulationTemplate)
class SimulationTemplate(ProtoWrapperBase):
    """
    Represents a simulation template object.

    Simulation templates can be used to create simulations with the same parameters.
    However, unlike simulations, the parameters of a simulation template are mutable.
    They can be used to partially set up the parameters of a simulation and then be
    persisted to the Luminary Cloud backend.
    """

    id: SimulationTemplateID
    "Simulation template ID."
    name: str
    "Simulation name."
    parameters: clientpb.SimulationParam
    "Simulation description."

    _proto: simtemplatepb.SimulationTemplate

    @property
    def create_time(self) -> datetime:
        return timestamp_to_datetime(self._proto.create_time)

    @property
    def update_time(self) -> datetime:
        return timestamp_to_datetime(self._proto.update_time)

    def update(
        self,
        *,
        name: Optional[str] = None,
        parameters: Optional[Union[clientpb.SimulationParam, SimulationParam, PathLike]] = None,
    ) -> None:
        """
        Update simulation template.

        Parameters
        ----------
        name : str, optional
            New project name.
        parameters : SimulationParam or path-like
            New complete simulation parameters object or path to local JSON file containing
            simulation parameters. In the former case, the input argument is modified to reflect
            changes applied by the backend (server), for example due to presets. Any differences
            between input and result are printed on screen.
        """
        req = simtemplatepb.UpdateSimulationTemplateRequest(id=self.id)

        if name is not None:
            req.name = name

        if parameters is not None:
            if isinstance(parameters, SimulationParam):
                param_proto = parameters._to_proto()
            elif isinstance(parameters, clientpb.SimulationParam):
                param_proto = clientpb.SimulationParam()
                param_proto.CopyFrom(parameters)
            else:
                param_proto = simulation_params_from_json_path(parameters)

            if isinstance(parameters, (SimulationParam, clientpb.SimulationParam)):
                # Table references are manipulated via the simulation template, hence we need to persist
                # them when we update the parameters.
                param_proto.table_references.clear()
                for k, v in self.parameters.table_references.items():
                    param_proto.table_references[k].CopyFrom(v)

            req.parameters.CopyFrom(param_proto)

        res = get_default_client().UpdateSimulationTemplate(req)
        self._proto = res.simulation_template

        def print_diff(
            old: Union[clientpb.SimulationParam, SimulationParam],
            new: Union[clientpb.SimulationParam, SimulationParam],
        ) -> None:
            diffs = list(Differ().compare(str(old).split("\n"), str(new).split("\n")))
            has_diffs = False
            for diff in diffs:
                if diff.startswith("-") or diff.startswith("+"):
                    if not has_diffs:
                        print("The input parameters have been modified:\n")
                        has_diffs = True
                    print(diff)

        # Show any inconsistency after the update and update the input argument.
        if isinstance(parameters, SimulationParam):
            old_param = parameters._to_proto()
            print_diff(old_param, self.parameters)
            parameters._from_proto(self.parameters)
        elif isinstance(parameters, clientpb.SimulationParam):
            print_diff(parameters, self.parameters)
            parameters.CopyFrom(self.parameters)

    def delete(self) -> None:
        """
        Delete the simulation template.
        """
        req = simtemplatepb.DeleteSimulationTemplateRequest(id=self.id)
        get_default_client().DeleteSimulationTemplate(req)

    def get_simulation_param(self) -> SimulationParam:
        """
        Returns the simulation parameters associated with this template to allow customization of
        the parameters.
        """
        return SimulationParam.from_proto(self.parameters)

    def list_tables(
        self,
        table_type: Optional[TableType] = None,
    ) -> list[RectilinearTable]:
        """
        Lists the tables available in the simulation template.

        Parameters
        ----------
        table_type : TableType
            (Optional) Filter the list to only include this type of table.

        Returns
        -------
        list[RectilinearTable]
            List of tables.
        """
        res: list[RectilinearTable] = []
        for id, metadata in self.parameters.table_references.items():
            if table_type is None or table_type == metadata.table_type:
                res.append(
                    RectilinearTable(
                        id=id,
                        name=metadata.uploaded_filename,
                        table_type=TableType(metadata.table_type),
                    )
                )
        return res


def get_simulation_template(id: SimulationTemplateID) -> SimulationTemplate:
    """
    Retrieve a specific simulation template by ID.

    Parameters
    ----------
    id : str
        Simulation template ID.
    """
    req = simtemplatepb.GetSimulationTemplateRequest(id=id)
    res = get_default_client().GetSimulationTemplate(req)
    return SimulationTemplate(res.simulation_template)
