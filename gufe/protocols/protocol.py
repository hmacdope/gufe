# This code is part of OpenFE and is licensed under the MIT license.
# For details, see https://github.com/OpenFreeEnergy/gufe

import abc
from typing import Optional, Iterable

from pydantic import BaseModel, validator
from openff.toolkit.utils.serialization import Serializable

from ..chemicalsystem import ChemicalSystem
from ..mapping import Mapping

from .protocolunit import ProtocolUnit, ProtocolDAG
from .results import ProtocolResult


class Protocol(Serializable, abc.ABC):
    """A protocol that implements an alchemical transformation.

    Takes a `ProtocolSettings` object specific to the protocol on init.
    This configures the protocol for repeated execution on `ChemicalSystem`s.

    Attributes
    ----------
    settings : ProtocolSettings

    """
    ...

    def __init__(
            self,
            settings: "ProtocolSettings" = None
        ):
        """

        """
        self._settings = settings

    def to_dict(self) -> dict:
        ...

    @classmethod
    def from_dict(cls, d: dict):
        ...

    def __hash__(self):
        return hash(
            (
                self._settings
            )
        )

    @classmethod
    @abc.abstractmethod
    def get_default_settings(cls):
        """Get the default settings for this protocol.

        These can be modified and passed back in to the class init.

        """
        ...

    @abc.abstractmethod
    def create(self, 
            initial: ChemicalSystem, 
            final: ChemicalSystem,
            mapping: Optional[Mapping] = None,
            protocol_result: Optional[ProtocolResult] = None,
            settings: Optional["ProtocolSettings"] = None
        ) -> ProtocolDAG:
        """Prepare a `ProtocolDAG` with all information required for execution.

        A `ProtocolDAG` is composed of `ProtocolUnit`s, with dependencies
        established between them. These form a directed, acyclic graph,
        and each `ProtocolUnit` can be executed once its dependencies have
        completed.

        A `ProtocolDAG` can be passed to a `Scheduler` for execution on its
        resources. A `ProtocolResult` can be retrieved from the `Scheduler` upon
        completion of all `ProtocolUnit`s in the `ProtocolDAG`.

        Parameters
        ----------
        initial : ChemicalSystem
            The starting `ChemicalSystem` for the transformation.
        final : ChemicalSystem
            The ending `ChemicalSystem` for the transformation.
        mapping : Optional[Mapping]
            Mapping of e.g. atoms between the `initial` and `final` `ChemicalSystem`s.
        protocol_result : Optional[ProtocolResult]
            If provided, then the `ProtocolDAG` produced will start from the
            end state of the given `ProtocolResult`. This allows for extension
            from a previously-run `ProtocolDAG`.
        settings : Optional[ProtocolSettings]
            Overrides for e.g. Level 3 settings to change sampling approach from
            the given `Protocol.settings`.

        Returns
        -------
        ProtocolDAG
            A directed, acyclic graph that can be executed by a `Scheduler`.

        """
        ...
