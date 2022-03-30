# This code is part of OpenFE and is licensed under the MIT license.
# For details, see https://github.com/OpenFreeEnergy/gufe

from typing import Dict, Optional

import numpy as np
from openff.toolkit.utils.serialization import Serializable

from .component import Component


class ChemicalState(Serializable):
    """A node of an alchemical network.

    Attributes
    ----------
    components
        The molecular representation of the chemical state, including
        connectivity and coordinates. This is a frozendict with user-defined
        labels as keys, `Component`s as values.
    box_vectors
        Numpy array indicating shape and size of unit cell for the system. May
        be a partial definition to allow for variability on certain dimensions.
    identifier
        Optional identifier for the chemical state; used as part of the
        (hashable) graph node itself when the chemical state is added to an
        `AlchemicalNetwork`.

    """

    def __init__(
        self,
        components: Dict[str, Component],
        box_vectors: Optional[np.ndarray] = None,
        identifier: Optional[str] = None,
    ):
        """Create a node for an alchemical network.

        Attributes
        ----------
        components
            The molecular representation of the chemical state, including
            connectivity and coordinates. Given as a dict with user-defined
            labels as keys, `Component`s as values.
        box_vectors
            Optional `numpy` array indicating shape and size of unit cell for
            the system. May be a partial definition to allow for variability on
            certain dimensions.
        identifier
            Optional identifier for the chemical state; included with the other
            attributes as part of the (hashable) graph node itself when the
            chemical state is added to an `AlchemicalNetwork`.

        """
        self._components = components
        self._identifier = identifier

        if box_vectors is None:
            self._box_vectors = np.array([np.nan] * 9)
        else:
            self._box_vectors = box_vectors

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.identifier != other.identifier:
            return False
        if not np.array_equal(self.box_vectors, other.box_vectors,
                              equal_nan=True):  # nan usually compares to false
            return False
        if self.components.keys() != other.components.keys():
            return False
        for k in self.components:
            if self.components[k] != other.components[k]:
                return False

        return True

    def __hash__(self):
        return hash(
            (
                tuple(sorted(self._components.items())),
                self._box_vectors.tobytes(),
                self._identifier,
            )
        )

    def to_dict(self):
        return {
            "components": {
                key: value.to_dict() for key, value in self.components.items()
            },
            "box_vectors": self.box_vectors.tolist(),
            "identifier": self.identifier,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            components={
                key: Component.from_dict(value) for key, value in d["components"]
            },
            box_vectors=np.array(d["box_vectors"]),
            identifier=d["identifier"],
        )

    @property
    def components(self):
        return dict(self._components)

    @property
    def box_vectors(self):
        return np.array(self._box_vectors)

    @property
    def identifier(self):
        return self._identifier

    @property
    def charge(self):
        """Total charge for the ChemicalState."""
        return sum([component.charge for component in self._components.values()])

    @classmethod
    def as_protein_smallmolecule_solvent(cls):
        """ """
        # alternate initializer for typical protein+ligand+solvent system
        ...

    @classmethod
    def as_smallmolecule_solvent(cls):
        """ """
        # alternate initializer for typical ligand+solvent system
        ...
