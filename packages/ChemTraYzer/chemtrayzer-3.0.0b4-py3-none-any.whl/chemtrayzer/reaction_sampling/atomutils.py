from __future__ import annotations

import warnings
from abc import ABC, abstractmethod  # , abstractclassmethod
from collections import UserDict
from dataclasses import dataclass, field
from functools import partial, lru_cache
from itertools import combinations
from typing import ( FrozenSet,
    TYPE_CHECKING,
    Any,
    Callable,
    FrozenSet,
    Optional,
    Sequence,
    Tuple,
    Iterable,
    Collection,
)

import numpy as np

from chemtrayzer.core.coords import calc_distance_matrix
from chemtrayzer.core.periodic_table import Element
from chemtrayzer.core.periodic_table import PERIODIC_TABLE as PTOE

if TYPE_CHECKING:
    from chemtrayzer.core.coords import Geometry


@dataclass
class BondSelector:
    '''
    Represents the method for the selection of bonds in geometry objects. Atoms are numbered starting with 1.
    :param included_atom_types: set of Elements containing symbol for each atom type
    :type included_atom_types: Set[Element], optional
    :param excluded_atom_types: set of Elements containing symbol for each atom type
    :type excluded_atom_types: Set[Element], optional
    :param included_atoms: set of Elements containing number for each atom
    :type included_atoms: Set[Int], optional
    :param excluded_atoms: set of Elements containing number for each atom
    :type types: Set[Int], optionalIterable tuples containing two atom types
    :type types: Iterable[Iterable[Element]], optional
    :param included_bonds: frozenset of tuples containing two atoms
    :type types: Iterable[Iterable[int]], optional
    :param excluded_bonds: frozenset of tuples containing two atoms
    :type types: Iterable[Iterable[int]], optional
    '''
    included_atom_types: Sequence[Element] = ()
    excluded_atom_types: Sequence[Element] = ()
    included_atoms: Sequence[int] = ()
    excluded_atoms: Sequence[int] = ()
    included_bonds_by_type: Sequence[Tuple[Element, Element]] = () #sorted tuples
    excluded_bonds_by_type: Sequence[Tuple[Element, Element]] = () #sorted tuples
    included_bonds: Sequence[Tuple[int, int]] = () #sorted tuples
    excluded_bonds: Sequence[Tuple[int, int]] = () #sorted tuples

    def __post_init__(self):  # just for error handling

        if self.included_atom_types and self.excluded_atom_types:
            assert "impossible to include and exclude atom types simultaneously"

        if self.included_atoms and self.excluded_atoms:
            if self.included_atoms.symmetric_difference(self.excluded_atoms):
                assert "impossible to include and exclude the same atoms simultaneously"

        if self.included_bonds_by_type and self.excluded_bonds_by_type:
            if self.included_bonds_by_type.symmetric_difference(self.excluded_bonds_by_type):
                assert "impossible to include and exclude bonds between atom types simultaneously"

        if self.included_bonds and self.excluded_bonds:
            if self.included_bonds.symmetric_difference(self.excluded_bonds):
                assert "impossible to include and exclude bonds between atoms simultaneously"


    def __call__(self, geo: Geometry) -> Tuple[Tuple[int, int], ...]:

        included_bonds = set()
        include_bond = False if self.included_atom_types else True

        for (atom1, atom_type1), (atom2, atom_type2) in combinations(enumerate(geo.atom_types), 2):
            # atom numbering for input (atom1, atom2) starts at 0
            atom1, atom2 = tuple(sorted([atom1, atom2]))
            atom_type1, atom_type2 = tuple(sorted([atom_type1, atom_type2]))
            if atom_type1 in self.included_atom_types and atom_type2 in self.included_atom_types:
                include_bond = True
            if atom_type1 in self.excluded_atom_types and atom_type2 in self.excluded_atom_types:
                include_bond = False
            if atom1 in self.included_atoms and atom2 in self.included_atoms:
                include_bond = True
            if atom1 in self. excluded_atoms and atom2 in self.excluded_atoms:
                include_bond = False
            if tuple(sorted((atom_type1, atom_type2))) in self.included_bonds_by_type:
                include_bond = True
            if tuple(sorted((atom_type1, atom_type2))) in self.excluded_bonds_by_type:
                include_bond = False
            if (atom1, atom2) in self.included_bonds:
                include_bond = True
            if (atom1, atom2) in self.excluded_bonds:
                include_bond = False
            if include_bond:
                included_bonds.add((atom1, atom2))

        return tuple(included_bonds)

#DEFAULTS
def default_nn_func(atom_types: Collection[Element]) -> float:
    return 6

def default_mm_func (atom_types: Collection[Element]) -> float:
    return 12

def default_r0_func(atom_types: Collection[Element]) -> float:
    if len(atom_types) == 1:
        raise ValueError('expected exactly two atom types')
    return sum(a.covalent_radius for a in atom_types) * 1.2


class AtomPairProperty(dict):
    default_func: Optional[Callable[[Collection[Element]], Any]] = None
    """
    Class to get Element pair specific properties. Atomic numbers, Symbols and Element objects can be used as keys.
    Useful for expected vdW radii or bond length for specific atom types from the periodic table of elements (PTOE)
    Values can be defined manually or calculated using a atom type specific function during initiation.
    ..code-block:: python
    def covalent_bond_length(key: Iterable[Element]) -> float:
        return (key[0].covalent_radius + key[1].covalent_radius)
    expected_bond_length = AtomPairProperty(func=covalent_bond_length)
    print(expected_bond_length['H','C'])
    """

    def __repr__(self):
        return str(dict(sorted(self.items())))

    @staticmethod
    def _raises_keyerror(*args, **kwargs):
        raise KeyError()

    def __init__(self, *args, default_func:Optional[Callable[[Collection[Element, Element]], Any]] = None, **kwargs):
        if default_func is None:
            default_func = self._raises_keyerror()
        self.default_func = default_func
        super().__init__(*args, **kwargs)

    def __missing__(self, key:Collection[Element]):
        fset_key = frozenset({PTOE[i] for i in key})
        if self.get(fset_key, None) is None:
            if len(fset_key) == 2:
                self[fset_key] = self.default_func(fset_key)
            elif len(fset_key) == 1:
                single_element_type = next(iter(fset_key))
                self[fset_key] = self.default_func((single_element_type, single_element_type))
            else:
                raise ValueError("wrong number of atom types")
        return self[fset_key]

    def __hash__(self):
        return hash(tuple(self.items()))

    @lru_cache(maxsize=2, typed=True)
    def array(self, atom_types: Sequence[Element]) -> np.ndarray:
        n_atoms = len(atom_types)
        array = np.zeros((n_atoms,n_atoms))
        for (atom1, atom_type1), (atom2, atom_type2) in \
                combinations(enumerate(atom_types), 2):
            value = self[frozenset({atom_type1, atom_type2})]
            array[atom1][atom2] = value
            array[atom2][atom1] = value
        return array


class ISwitchingFunction(ABC):
    @abstractmethod
    def __call__(self, distance: float, atom_types: Tuple[Element, Element]) -> float: ...

    def array(self, coords: np.ndarray, atom_types: Collection[Element]) -> np.ndarray:
        dist_mat = calc_distance_matrix(coords)
        atom_types_mat = np.array([[(i,j) for j in atom_types] for i in atom_types])
        return np.vectorize(self.__call__)(dist_mat, atom_types_mat)


@dataclass
class StepSwitchingFunction(ISwitchingFunction):
    r0: AtomPairProperty = field(default_factory =
                                 partial(AtomPairProperty,default_func=default_r0_func))

    def __call__(self, distance:float, atom_types:Tuple[Element, Element]):
        if distance < 0:
            raise ValueError('distance can not be negative')
        else:
            return 1 if distance < self.r0[atom_types] else 0

    def array(self, coords, atom_types: Sequence[Element]) -> np.ndarray:
        return np.where(calc_distance_matrix(coords) < self.r0.array(atom_types), 1, 0)

class StaticStepSwitchingFunction(ISwitchingFunction):
    """like StepSwitchingFunction only that r0 is evaluated once during
    initiation for a given set of atom types. This is useful when the switching
    function should be evaluated for many geometries with the same atom types.

    .. note::  The atom_types argument passed to array will be ignored.
    """
    r0: AtomPairProperty
    r0_array: np.ndarray
    atom_types: Sequence[Element]

    def __init__(self,
                 atom_types: Sequence[Element],
                 r0: AtomPairProperty = AtomPairProperty(
                                                default_func=default_r0_func)):
        self.r0 = r0
        self.r0_array = r0.array(atom_types)
        self.atom_types = atom_types

    def __call__(self, distance:float, atom_types:Tuple[Element, Element]):
        if distance < 0:
            raise ValueError('distance can not be negative')
        else:
            return 1 if distance < self.r0[atom_types] else 0

    def array(self, coords, _: Sequence[Element]) -> np.ndarray:
        return np.where(calc_distance_matrix(coords) < self.r0_array, 1, 0)

@dataclass
class RationalSwitchingFunction(ISwitchingFunction):
    r0: AtomPairProperty = field(default_factory =
                                 partial(AtomPairProperty,default_func=default_r0_func))
    nn: AtomPairProperty = field(default_factory =
                                 partial(AtomPairProperty,default_func=default_nn_func))
    mm: AtomPairProperty = field(default_factory =
                                 partial(AtomPairProperty,default_func=default_mm_func))

    def __call__(self, distance:float, atom_types: Tuple[Element, Element]):
        if distance < 0:
            raise ValueError('distance can not be negative')
        elif distance == self.r0[atom_types]:
            return 0.5
        else:
            r0, nn, mm = self.r0[atom_types], self.nn[atom_types], self.mm[atom_types]
            return (1-pow(distance/r0,nn))/(1-pow(distance/r0,mm))

    def array(self, coords: np.ndarray, atom_types: Sequence[Element]) -> np.ndarray:
        """applies the reference function to all aton pairwise distances in the input geometry
        diagonal elements are nan
        :return: array of reference values
        :rtype: np.ndarray
        """
        nn_array = self.nn.array(atom_types)
        mm_array = self.mm.array(atom_types)
        r0_array = self.r0.array(atom_types)

        with warnings.catch_warnings():
            warnings.simplefilter(action="ignore", category=RuntimeWarning)
            # diagonal elements are NAN
            r_div_r0 = np.divide(calc_distance_matrix(coords), r0_array) # r / r0

        r_div_r0_pow_nn = np.power(r_div_r0, nn_array) # (r/r0)**nn
        r_div_r0_pow_mm = np.power(r_div_r0, mm_array) # (r/r0)**mm
        shape = np.shape(nn_array)
        numerator = np.subtract(np.ones(shape),r_div_r0_pow_nn) # 1 - ( r / r0 ) ** nn
        denominator = np.subtract(np.ones(shape), r_div_r0_pow_mm) # 1 - ( r / r0 ) ** mm

        with warnings.catch_warnings():
            warnings.simplefilter(action="ignore", category=RuntimeWarning)

            # diagonal elements are NAN
            reference_array = np.divide(numerator, denominator)
        np.fill_diagonal(reference_array, 0)
        return reference_array
