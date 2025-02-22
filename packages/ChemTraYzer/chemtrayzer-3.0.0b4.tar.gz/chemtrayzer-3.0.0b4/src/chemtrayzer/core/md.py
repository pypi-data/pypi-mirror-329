"""Molecular Dynamics

This module contains classes and functions used to analysis molecular dynamics
simulations.
"""

from __future__ import annotations

import dataclasses

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    PlainSerializer,
    computed_field,
    field_validator,
    model_validator,
)


import warnings
import logging
from abc import ABC, abstractmethod
from dataclasses import MISSING, dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING, Annotated, Literal

if TYPE_CHECKING:
    from collections.abc import Iterable
    from os import PathLike

    from chemtrayzer.core.graph import MolGraph

import numpy as np
from numpy import isnan
from numpy.linalg import norm

from chemtrayzer.core.coords import ChainOfStates, Geometry
from chemtrayzer.core.lot import LevelOfTheory  # noqa: TCH001
from chemtrayzer.core.periodic_table import PERIODIC_TABLE as PTOE
from chemtrayzer.core.periodic_table import Element
from chemtrayzer.engine.jobsystem import Job

###############################################################################
# MD metadata
###############################################################################


class MDIntegrator(Enum):
    VELOCITY_VERLET = "velocity Verlet"
    LEAPFROG = "leapfrog"


###############################################################################
# MD metadata > thermostat and barostat
###############################################################################
@dataclass
class MDThermostat(ABC):
    """base class for different thermostats"""

    tau: float
    """coupling time constant [fs]"""
    temperature: float
    """simulation temperature in Kelvin, if constant-T simulation"""

    @property
    @abstractmethod
    def type(self) -> str:
        """thermostat type as string. Defined in subclass and used for
        deserialization. Should be defined as a field of type Literal with
        allowed values that a user can input and a default value (one of the
        allowed values). The field is always set to the default value in
        __post_init__ to simplify comparisons, etc.
        """

    def __post_init__(self):
        # "normalize" the value of self.type
        for field in dataclasses.fields(self):
            if field.name == 'type':
                break

        if field.name != 'type':
            # use warnings over logging, because this is a programming error
            warnings.warn(f'"type" is not a field of {self.__class__.__name__}'
                          '. Normalization does not work.')
        elif field.default == MISSING:
            warnings.warn(f'{self.__class__.__name__}.type has no default '
                          'value.')
        setattr(self, field.name, field.default)


    def __str__(self, width=30):
        s = "Content of MD thermostat:\n"
        s += f'{"tau":{width}} : {self.tau} fs\n'
        s += f'{"temperature":{width}} : {self.temperature} K\n'
        return s


@dataclass(kw_only=True)
class _TStatNotSet_Type(MDThermostat):
    """for cases in which no thermostat was set in the simulation, e.g., for
    a NVE ensemble.
    """

    type: Literal['no-thermostat'] = 'no-thermostat'
    tau: float = 0
    temperature: float = 0

    def __repr__(self):
        return 'no-thermostat'

    def __eq__(self, other):
        return type(self) == type(other)   # noqa: E721


TSTAT_NOT_SET = _TStatNotSet_Type()
"""Singleton instance of the TStatNotSet class. Used to indicate that no
Thermostat was used in the simulation."""


@dataclass(kw_only=True)
class BerendsenTStat(MDThermostat):
    """Berendsen thermostat (usually only used for equilibration)"""

    # only used for deserialization, set to default value so that class can
    # simply be instantiated
    type: Literal['berendsen', 'Berendsen'] = 'berendsen'

@dataclass(kw_only=True)
class NoseHooverTStat(MDThermostat):
    """chained Nosé-Hoover thermostat"""

    type: Literal['nose-hoover',
                  'nosé-hoover',
                  'Nose-Hoover',
                  'Nosé-Hoover'] = 'nose-hoover'
    chain_length: int = 3

@dataclass(kw_only=True)
class VelocityRescalingTStat(MDThermostat):
    """Berendsen thermostat with an added stochastic term that ensures that the
    correct ensemble is sampled (Bussi-Donadio-Parrinello thermostat)."""

    type: Literal['velocity-rescaling',
                  'Velocity-Rescaling'] = 'velocity-rescaling'

@dataclass
class MDBarostat:
    """Base class for barostats used in MD simulations"""

    tau: float
    """coupling time constant [fs]"""
    pressure: float
    """simulation pressure in Pascal, if pressure was held constant"""

    def __str__(self, width=30):
        s = "Content of MD barostat:\n"
        s += f'{"tau":{width}} : {self.tau} fs\n'
        s += f'{"pressure":{width}} : {self.pressure} Pa\n'
        return s

    @property
    @abstractmethod
    def type(self) -> str:
        """thermostat type as string. Defined in subclass and used for
        deserialization. Should be defined as a field of type Literal with
        allowed values that a user can input and a default value (one of the
        allowed values). The field is always set to the default value in
        __post_init__ to simplify comparisons, etc.
        """

    def __post_init__(self):
        # "normalize" the value of self.type
        for field in dataclasses.fields(self):
            if field.name == 'type':
                break

        if field.name != 'type':
            # use warnings over logging, because this is a programming error
            warnings.warn(f'"type" is not a field of {self.__class__.__name__}'
                          '. Normalization does not work.')
        elif field.default == MISSING:
            warnings.warn(f'{self.__class__.__name__}.type has no default '
                          'value.')
        setattr(self, field.name, field.default)

@dataclass(kw_only=True)
class _PStatNotSet_Type(MDBarostat):
    """for cases in which no barostat was set in thes imulation. E.g. in an
    NVT ensemble.
    """

    type: Literal['no-barostat'] = 'no-barostat'
    tau: float = 0
    pressure: float = 0

    def __repr__(self):
        return "no-barostat"

    def __eq__(self, other):
        return type(self) == type(other)  # noqa: E721

PSTAT_NOT_SET = _PStatNotSet_Type()
"""Singleton instance of the PStatNotSet class. Used to indicate that no
Barostat was used in the simulation."""


@dataclass(kw_only=True)
class BerendsenPStat(MDBarostat):
    """Berendsen barostat"""

    type: Literal['berendsen', 'Berendsen'] = 'berendsen'

@dataclass(kw_only=True)
class MTKPStat(MDBarostat):
    """Martyna-Tobias-Klein barostat"""

    type: Literal['mtk',
                  'martyna-tobias-klein',
                  'Martyna-Tobias-Klein',
                  'MTK']    = 'mtk'


################################################################################
# MD metadata > simulation box box
################################################################################


class BoxType(Enum):
    """Enumeration of box types for molecular dynamics simulations.

    This enumeration is used to specify the type of box in the MDBox class.
    When adding new box types, ensure they are also added to the MDBox class
    type hints and update the validate method to check for compliance with the
    new box type.
    """

    # Boxes with 3 basis vectors
    ORTHOGONAL = auto()
    """Three dimensional box with orthogonal basis vectors"""
    TRICLINIC = auto()
    """Three dimensional box with non-orthogonal basis vectors"""

    # Boxes with 2 basis vectors
    ORTHOGONALSLAB = auto()
    """Two dimensional box with orthogonal basis vectors"""
    TRICLINICSLAB = auto()
    """Two dimensional box with non-orthogonal basis vectors"""

    @classmethod
    def from_box_vectors(cls, box_vectors: np.ndarray) -> BoxType:
        """determines the box type from the box vectors

        :param box_vectors: 3x3 matrix whose columns contain the box vectors
        :return: BoxType
        """
        assert box_vectors.shape == (3, 3), "box_vectors must be a 3x3 matrix"
        # check if box is a slab
        if norm(box_vectors[2]) in [0, np.inf] or isnan(norm(box_vectors[2])):
            # check orthogonality of the first two basis vectors
            if np.isclose(box_vectors[0] @ box_vectors[1], 0, atol=1e-6):
                return cls.ORTHOGONALSLAB
            else:
                return cls.TRICLINICSLAB
        # box is 3 dimensional
        else:
            if np.isclose(box_vectors[0] @ box_vectors[1], 0, atol=1e-6):
                return cls.ORTHOGONAL
            else:
                return cls.TRICLINIC

# some stuff to use numpy arrays for box vectors with pydantic
def _convert_to_numpy_float_array(array_like) -> np.ndarray:
    try:
        return np.array(array_like, dtype=float)
    except Exception as err:
        raise ValueError('Object not convertible to numpy float array'
                         ) from err

def _numpy_array_to_list(arr: np.ndarray):
    return arr.tolist()

_NdArray = Annotated[
    np.ndarray,
    BeforeValidator(_convert_to_numpy_float_array),
    PlainSerializer(_numpy_array_to_list, return_type=list)
]

# use pydantic as we always want to validate boxes
class MDBox(BaseModel):
    """Class representing a three-dimensional box with up to three basis
    vectors.

    This class is designed for any box that can be represented by three or
    fewer basis vectors, such as orthorhombic and triclinic boxes, as well as
    triclinic slabs. If the original box dimensions are fewer than three, the
    user must still specify three basis vectors. The third basis vector can
    be constructed using the `construct_third_basis_vector` function.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True) # allow np.ndarray

    box_vectors: _NdArray
    """A 3x3 numpy array where each row represents a basis vector of the box.
    If the original box dimension is less than 3, the third basis vector can be
    constructed using the `construct_third_basis_vector` function."""
    box_origin: tuple[float, float, float]
    """A tuple representing the origin of the box in 3D space."""
    pbc: tuple[bool, bool, bool]
    """Periodic boundary conditions in the x, y, and z directions. If the box
    is a slab, only the first two elements are used. If the box is
    one-dimensional, e.g. for molecular strings, only the first element is
    used."""
    box_type: BoxType
    """The type of the box. If new box types are added, they should be added
    to the `BoxType` enum as well. Compliance with the box
    attributes should be checked in the `validate` method."""

    @computed_field
    @property
    def volume(self) -> float:
        """The volume of the box, calculated once during initialization."""
        return self._get_volume()

    @field_validator('box_vectors')
    @classmethod
    def has_three_by_three_shape(cls, v: np.ndarray) -> np.ndarray:
        if v.shape != (3, 3):
            raise ValueError(
                "Box vectors must be a 3x3 numpy array where rows represent "
                "basis vectors.If the original box dimension is less than 3, "
                "the third basis vector can be constructed using the "
                "`construct_third_basis_vector` function."
            )
        return v

    @model_validator(mode='after')
    def _validate_box_type_against_shape(self):
        ### Orthorhombic and Triclinic boxes
        if self.box_type in [BoxType.ORTHOGONAL, BoxType.TRICLINIC]:
            for i in range(3):
                if norm(self.box_vectors[i]) in [0, np.inf] or isnan(
                    norm(self.box_vectors[i])
                ):
                    raise ValueError(
                        f"Basis vector {i + 1} cannot be zero, infinite or "
                        "nan."
                    )

            _is_orthogonal = self.is_orthogonal(
                self.box_vectors, is_slab=False
            )

            if self.box_type == BoxType.ORTHOGONAL and not _is_orthogonal:
                raise ValueError("Box vectors are not orthogonal")
            if self.box_type == BoxType.TRICLINIC and _is_orthogonal:
                # raise an error because the user should use the appropriate
                # box type, because the class methods depend on the specific
                # box type
                raise ValueError(
                    (
                        "Box vectors are orthogonal, please only use the "
                        "TRICLINIC box type for non-orthogonal box vectors."
                    )
                )

        #### Slabs
        if self.box_type in [BoxType.ORTHOGONALSLAB, BoxType.TRICLINICSLAB]:
            # assert that only the 3rd basis vector can be zero or infinite
            for i in range(2):
                if norm(self.box_vectors[i]) in [0, np.inf] or isnan(
                    norm(self.box_vectors[i])
                ):
                    raise ValueError(
                        f"Basis vector {i + 1} cannot be zero, "
                        "infinite or nan."
                    )

            _is_orthogonal = self.is_orthogonal(self.box_vectors, is_slab=True)

            # for slabs the third basis vector can be zero or infinite
            if self.box_type == BoxType.ORTHOGONALSLAB and not _is_orthogonal:
                raise ValueError(
                    (
                        "Box vectors are not orthogonal. For Orthogonal "
                        "Slabs the first two basis vectors must be orthogonal."
                    )
                )
            if self.box_type == BoxType.TRICLINICSLAB and _is_orthogonal:
                # raise an error because the user should use the appropriate
                # box type, because the class methods depend on the specific
                # box type
                raise ValueError(
                    (
                        "Box vectors are orthogonal, please only use the "
                        "TRICLINICSLAB box type if the first two basis "
                        "vectors are not orthogonal."
                    )
                )

        return self

    def _get_volume(self):
        """Method to calculate the volume of the box using the scalar triple
        product of the box vectors. Checks are done to ensure the box vectors
        are valid. Warnings are raised for negative, zero, infinite, or NaN
        volumes.

        This method is automatically called during initialization.
        returns: volume of the box
        """

        vol = np.dot(
            np.cross(self.box_vectors[0], self.box_vectors[1]),
            self.box_vectors[2],
        )
        # check for zero, infinite, or NaN volumes
        if vol <= 0 or vol == np.inf or np.isnan(vol):
            warnings.warn(
                f"""The volume of the box is {vol}. This might lead
                          to undefined behavior."""
            )

        return vol

    @staticmethod
    def is_orthogonal(box_vectors, is_slab=False):
        """Method to check if the box vectors are orthogonal. Since the box
        vectors can have a length of zero or infinity, we cannot simply check
        for orthogonality using the triple product. The method implements a
        robust check for orthogonality. If the box is a slab, and only the
        first two basis vectors are properly defined (third basis vector is
        zero or infinite), the method will check for orthogonality of the first
         two basis vectors. Orthogonality checks are not applicable to
        molecular strings and therefore are not handled. Returns True if the
        box vectors are orthogonal, False otherwise.
        """

        a, b, c = box_vectors
        # check if the box is a slab
        if is_slab:
            # Check if dot(a, b) is close to 0
            return np.isclose(a @ b, 0, atol=1e-06)

        # Check if any of the basis vectors are zero or infinite
        for i in range(3):
            if norm(box_vectors[i]) in [0, np.inf] or isnan(
                norm(box_vectors[i])
            ):
                raise ValueError(
                    f"""Basis vector {i + 1} cannot be zero, infinite or nan.
                Only for slabs the third basis vector can be zero or infinite.
                """
                )

        # check for orthogonality
        else:
            # Check if dot(a, b) is close to 0
            if not np.isclose(a @ b, 0, atol=1e-6):
                return False
            # Check if dot(a, c) is close to 0
            if not np.isclose(a @ c, 0, atol=1e-6):
                return False
            # Check if dot(b, c) is close to 0
            return np.isclose(b @ c, 0, atol=1e-6)

    @staticmethod
    def construct_third_basis_vector(v1, v2, height):
        """
        Construct the third basis vector of the box from the first two basis
        vectors.

        The third basis vector is constructed via the cross product of the
        first two basis vectors and scaled by the height parameter. If height
        is not explicitly available, it can be derived from heuristics such as
        slab thickness. As a last resort, height can be set to infinity or
        zero, but this may result in a cell with infinite/zero volume,
        potentially breaking other methods.
        """
        cross = np.cross(v1, v2)
        c = height * cross / np.linalg.norm(cross)
        box_vectors = np.vstack((v1, v2, c))
        return box_vectors


# Pydantic chooses the correct type in the union based on the discriminator
# Using just the Union would also work but the errors would be less informative
ThermostatT = Annotated[BerendsenTStat | NoseHooverTStat
                          | VelocityRescalingTStat | _TStatNotSet_Type,
                          Field(discriminator='type')]

BarostatT = Annotated[BerendsenPStat | MTKPStat | _PStatNotSet_Type,
                          Field(discriminator='type')]


class MDMetadata(BaseModel):

    model_config = ConfigDict(arbitrary_types_allowed=True,  # allow LOT objs.
                              )

    initial_box: MDBox|None = None
    """initial box geometry"""
    level_of_theory: LevelOfTheory|None = None
    """potential energy method used in the simulation"""
    number_of_steps: int|None = None
    """number of timesteps"""
    timestep: float|None = None
    """size of a single timestep in femtoseconds"""
    integration_method: MDIntegrator|None = None
    """integration method"""
    sampling_frequency: int|None = None
    """number of timesteps after which the next frame is written to disk during
    the simulation"""
    thermostat: ThermostatT|_TStatNotSet_Type|None = None
    """thermostat used during the simulation"""
    barostat: BarostatT|_PStatNotSet_Type|None = None
    """barostat used during simulation"""
    seed: int|None = None
    """seed used to generate initial velocity distribution. If seed is None, no
    velocities will be generated"""

    def __str__(self, width=30):
        s = "Content of MD meta data:\n"
        s += f'{"level of theory":{width}} : {self.level_of_theory}\n'
        s += f'{"number of steps":{width}} : {self.number_of_steps} steps\n'
        s += f'{"timestep":{width}} : {self.timestep} fs\n'
        s += f'{"integration method":{width}} : {self.integration_method}\n'
        s += (
            f'{"sampling frequency":{width}} : '
            f"{self.sampling_frequency} steps\n"
        )
        # only print thermostat if it has been set
        if self.thermostat is not None:
            s += f'{"thermostat":{width}} : {self.thermostat:.2f} K\n'
        # only print barostat if it has been set
        if self.barostat is not None:
            s += f'{"barostat":{width}} : {self.barostat:.2f} Pa\n'
        return s


################################################################################
# MD molecule & rate constants
################################################################################


class MDMolecule:
    """
    Molecule representation as seen in a molecular dynamics simulation.

    :param start_frame: first frame of the molecule's occurrence in MD
    :param graph: molecular graph in MolGraph format
    :param name: some descriptive string name
    :param end_frame: last frame of the molecule's occurrence in MD
    :ivar predecessors: List of MDMolecules, reactants of the reaction that
                        created this MDMolecule
    :ivar successors: List of MDMolecules, products of the reaction that
                      consumed this MDMolecule
    """

    def __init__(self, start_frame: int, graph: MolGraph, name: str = ""):
        # IDs
        self._internal_id = id(self)
        self._name = name
        # molecular graph
        self.graph = graph
        # frames
        self.start_frame = start_frame
        self.is_stable = False
        # molecule history
        self.predecessors: list[MDMolecule] = []
        self.successors: list[MDMolecule] = []

    def __repr__(self):
        return f"#{self.internal_id} @{self.start_frame}"

    def __str__(self):
        text = ""
        text += f'MD Molecule #{self.internal_id} "{self.name}"\n'
        text += f"from: {self.start_frame}\n"
        text += f"to: {self.end_frame()}\n"
        return text

    @property
    def internal_id(self) -> int:
        """
        An object-unique integer to distinguish between MDMolecule objects.
        """
        return self._internal_id

    @internal_id.setter
    def internal_id(self, value: int):
        self._internal_id = value

    @property
    def name(self) -> str:
        """
        A placeholder for a name.
        """
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    def atoms(self) -> tuple[int]:
        """
        The integer atom IDs as set during construction. In general, those are
        not consecutive.
        """
        return self.graph.atoms

    def end_frame(self) -> float:
        """
        The frame number at which the molecule cease to exist in a simulation.
        Returns float('inf') when the molecule persists.
        """
        return (
            min([successor.start_frame for successor in self.successors])
            if self.successors
            else float("inf")
        )


@dataclass
class RateConstantRecord:
    """
    A helper class for storing info about 1 reaction.
    :param flux: list of directions, +1 for forward, -1 for backward,
                 0 otherwise
    :param rate: rate constant in cm3, mol, s
    :param events: number of reactive events
    :param integral: concentration integral
    :param upper_k: upper bound for rate constant
    :param lower_k: lower bound for rate constant
    :param rateB: reverse rate constant
    :param eventsB: number of reverse reactive events
    :param integralB: concentration integral for reverse reaction
    :param upper_kB: upper bound for reverse rate constant
    :param lower_kB: lower bound for reverse rate constant
    """

    flux: list = None
    rate: int = 0
    events: int = 0
    integral: int = 0
    upper_k: float = 0.0
    lower_k: float = 0.0
    rateB: int = 0
    eventsB: int = 0
    integralB: int = 0
    upper_kB: float = 0.0
    lower_kB: float = 0.0


###############################################################################
# trajectory
###############################################################################


class Trajectory(ChainOfStates):
    """
    Container for contiguous atom trajectories of a molecular dynamics
    simulation with a constant number of atoms.

    .. note::

        While box_vectors, box_origin, graphs and coords can be set
        independently from each other, it is the responsibility of the caller,
        that they must have the same length along the first axis, i.e., the
        axis representing the frame index

    :param metadata:
    :param atom_types:
    :param coords:
    :param box_vectors: if None, the box vectors from metadata are used
                        (only if no barostat is used)
    :param box_origin: if None, the box origin from metadata is used
    :param first_timestep:
    """

    metadata: MDMetadata
    """container for MD settings like number of steps, etc."""
    box_vectors: np.ndarray
    """n_frames x 3 x 3 array containing the box vectors (in each column/along
    second axis) for each frame
    """
    box_origin: np.ndarray
    """n_frames x 3 array containing the origin of the box
    """
    first_timestep: int
    """id of the first timestep in case this object contains only a part of the
    trajectory
    """
    charges: np.ndarray = None
    graphs: list[MolGraph] = None
    """conductivities for each frame. The atom/node ids are considered to be
       the same as in `coords` and `atom_types`
    """

    def __init__(
        self,
        *,
        metadata: MDMetadata,
        atom_types: tuple[Element],
        coords: Iterable[Iterable[Iterable[float]]],
        box_vectors: np.ndarray = None,
        box_origin: np.ndarray = None,
        graphs: list[MolGraph] = None,
        first_timestep: int = 0,
    ):
        self.metadata: MDMetadata = metadata

        if box_vectors is None:
            if metadata.barostat == PSTAT_NOT_SET:
                # broadcasting creates a readonly view with the correct size,
                # but does not copy the values -> it looks like a
                # n_frame x 3 x 3 array but stores only 9 numbers
                self.box_vectors = np.broadcast_to(
                    metadata.initial_box.box_vectors, (len(coords), 3, 3)
                )
            elif metadata.barostat is None: # unkown, if barostat was used
                raise ValueError("It could not be determined, if a barostat "
                    "was used and box vectors over time were not provided. ")
            else:
                raise ValueError(
                    "box_vectors must be provided if a barostat is " "used"
                )
        else:
            box_vectors = np.array(box_vectors)
            if box_vectors.shape != (len(coords), 3, 3):
                raise ValueError(
                    "box_vectors must have the shape n_frames x 3 x 3"
                )
            self.box_vectors = box_vectors

        if box_origin is None:
            self.box_origin = np.broadcast_to(
                metadata.initial_box.box_origin, (len(coords), 3)
            )
        else:
            box_origin = np.array(box_origin)
            if box_origin.shape != (len(coords), 3):
                raise ValueError("box_origin must have the shape n_frames x 3")
            self.box_origin = box_origin

        self.first_timestep = first_timestep
        self.graphs = graphs

        super().__init__(atom_types=atom_types, coords_list=coords)

    def __str__(self):
        """
        Prints some information about the trajectory.

        :return: str
        """
        text = "CTY3 Trajectory\n"
        text += (
            f"{self.n_frames} frames * {self.metadata.timestep} fs/frame = "
            f"{self.length()} fs\n"
        )
        if self.graphs is not None:
            text += "has connectivity\n"
        if self.charges is not None:
            text += "has charges\n"
        text += str(self.metadata)
        return text

    def __getitem__(self, n: int):
        """
        Returns the geometry of the specified frame.

        :param n: frame number
        :type n: int
        :return: Geometry
        """
        return self.get_geometry(n)

    def length(self):
        """
        Returns the length of the trajectory in femtoseconds.

        :return: length of the trajectory in femtoseconds
        """
        if self.metadata.timestep is None:
            return 0
        return self.metadata.timestep * (self.n_frames - 1)

    def cell_volume(self, n: int | slice):
        """
        :param n: frame number(s) at which to return the cell volume
        :return: the cell volume of the trajectory [Angstrom^3]
        """
        return np.abs(np.linalg.det(self.box_vectors[n]))

    def append_data(self, other: Trajectory):
        """
            Append coordinates and optionally connectivities or charges. The
            Metadata will be updated to reflect the new number of frames in the
            Trajectory object.
        """
        assert isinstance(other.coords, np.ndarray)
        assert isinstance(other.graphs, list)
        assert isinstance(other.charges, np.ndarray)

        if self.n_frames == 0:
            self.coords = other.coords
            self.graphs = other.graphs
            self.charges = other.charges
            return
        # check: append data to None?!
        if self.coords is None and other.coords is not None:
            logging.warning("Trajectory: trying to append to an non-existing "
                            "coordinate array. Aborted.")
            return
        if self.graphs is None and other.graphs is not None:
            logging.warning("Trajectory: trying to append to an non-existing "
                            "graphs array. Aborted.")
            return
        if self.charges is None and other.charges is not None:
            logging.warning("Trajectory: trying to append to an non-existing "
                            "charges array. Aborted.")
            return
        # check: same data in both?
        if other.coords is None and self.coords is not None:
            logging.warning("Trajectory: trying to append empty coordinates "
                            "to existing data. Aborted.")
            return
        if other.graphs is None and self.graphs is not None:
            logging.warning("Trajectory: trying to append empty graphs to "
                            "existing data. Aborted.")
            return
        if other.charges is None and self.charges is not None:
            logging.warning("Trajectory: trying to append empty charges to "
                            "existing data. Aborted.")
            return

        # do the actual appending
        if len(other.coords) > 0:
            # self.append(coords=other.coords)
            self.coords = np.concatenate((self.coords, other.coords))
        if self.graphs is not None:
            self.graphs += other.graphs
        if self.charges is not None:
            self.charges = np.vstack([self.charges, other.charges])

        # update some metadata
        self.metadata.number_of_steps = self.n_frames

        return

    def remove_last_frame(self):
        """
        The last frame of a trajectory might be undesired, e.g. when
        concatenating. This function removes the last coordinate frame, and if
        available, the last frames of connectivity and charges. The metadata
        will be updated to reflect the new number of frames in the Trajectory
        """
        # remove the last frame of each data array
        self.coords = self.coords[:-1]
        if self.graphs is not None:
            self.graphs = self.graphs[:-1]
        if self.charges is not None:
            self.charges = self.charges[:-1]
        # update some metadata
        self.metadata.number_of_steps = self.n_frames

    def remove_first_frame(self):
        """
        The first frame of a trajectory might be undesired, esp. when
        concatenating. This function removes the first coordinate frame, and if
        available, the first frames of connectivity and charges. The metadata
        will be updated to reflect the new number of frames in the Trajectory
        """
        # remove the first frame of each data array
        self.coords = self.coords[1:]
        if self.graphs is not None:
            self.graphs = self.graphs[1:]
        if self.charges is not None:
            self.charges = self.charges[1:]
        # update some metadata
        self.metadata.number_of_steps = self.n_frames


class TrajectoryParser(ABC):
    """
    base class for trajectory parsers. Trajectory parsers need to remember the
    index of the next frame to be read from the trajectory file. This index is
    used to read the trajectory in small chunks without needing to load the
    whole trajectory into memory at once. The index is updated after each call
    to the parse method.
    """

    @abstractmethod
    def parse(self, n_steps: int = -1) -> Trajectory:
        """
        parses a piece (or all) of the trajectory

        :param n_steps: Read at most this many steps from the file and
                        remember how many steps have been read. A subsequent
                        call to this function should continue from the first
                        step, that has not been read yet. By default (-1),
                        the whole trajectory is read
        :return: piece of the trajectory that has been read. The trajectory
                 may be empty, if it has been read, completely"""

@dataclass
class XYZTrajectoryParser(TrajectoryParser):
    """
    Trajectory parser for  xyz files
    """

    filename: PathLike
    metadata: MDMetadata

    def __post_init__(self):
        self._pos = 0
        with open(self.filename, "r", encoding="utf-8") as xyz_file:
            self._n_atoms = int(xyz_file.readline())
            _ = xyz_file.readline()
            self.atom_types = tuple(
                PTOE[xyz_file.readline().split()[0]]
                for _ in range(self._n_atoms)
            )

    def parse(self, n_steps):
        if self._pos is None:
            raise StopIteration()

        with open(self.filename, "r", encoding="utf-8") as xyz_file:
            xyz_file.seek(self._pos, 0)
            traj = []
            for step in range(n_steps):
                n_atoms, _ = xyz_file.readline(), xyz_file.readline()

                if n_atoms.strip() == "":
                    self._pos = None
                    break
                yd = [[float(coord)
                       for coord in xyz_file.readline().split()[1:4]
                      ] for line in range(self._n_atoms)]
                traj.append(yd)
                self._pos = xyz_file.tell()

        return Trajectory(
            atom_types=self.atom_types,
            coords=np.array(traj),
            metadata=self.metadata,
        )

class MultiTrajectoryParser(TrajectoryParser):
    """
    Provides a reader for multiple trajectory files treated as contiguous data.
    Each file is managed by its own TrajectoryParser instance, and they are
    read in the order they are provided. This parser can handle reading in
    small chunks without needing to load all trajectories into memory at once.
    """
    _active_parser_queue: list[TrajectoryParser]
    "The queue of parsers that are currently active."
    _inactive_parser_stack: list[TrajectoryParser]
    "The stack of parsers that have been completely read and are now inactive."
    _discard_first_steps: bool
    "Flag indicating whether the first frame of each parser "
    "(except the first) should be discarded to avoid duplication."
    _steps_read: int
    "Number of steps read so far from the current parser."

    def __init__(
        self,
        parsers: list[TrajectoryParser],
        discard_first_steps=True,
    ):
        self._active_parser_queue = parsers

        self._inactive_parser_stack = []

        self._discard_first_steps = discard_first_steps

        self._steps_read = 0

    def add_parser(self, parser: TrajectoryParser):
        """
        Add a new parser to the active queue.

        This method allows for dynamic loading of additional parsers after
        the initial instantiation.
        """
        self._active_parser_queue.append(parser)

    def _read_n_steps(self, n_steps: int) -> Trajectory:
        """
        Reads a specified number of steps from the active parser queue and
        returns a Trajectory object.

        Algorithm:
        1. Attempt to read n_steps from the current active parser.
        2. If the returned trajectory is empty:
           a. Move the current parser to the inactive stack.
           b. If there are no more parsers, return the empty trajectory.
           c. Otherwise, recursively call _read_n_steps with the same n_steps.
        3. If the returned trajectory is not empty:
           a. If this is not the first parser and _discard_first_steps is
              True, remove the first frame to avoid duplication.
           b. Update the steps_read count.
           c. If n_steps is not satisfied, recursively call _read_n_steps
              for the remaining steps and append them to the current
              trajectory.

        The method stops when:
        - The requested number of steps (n_steps) has been read.
        - All parsers have been exhausted (returns whatever steps were read).
        - n_steps is -1, indicating to read all available steps from all
          parsers.
        """

        trajectory =  self._active_parser_queue[0].parse(n_steps)
        # two cases: either the returned trajectory is empty, or it is not

        #case 1: trajectory is empty
        if trajectory.n_frames == 0:
            self._steps_read = 0
            # if we reached the end of the parser, move it to the inactive
            # stack
            self._inactive_parser_stack.append(self._active_parser_queue.pop(0))
            # if there are no more parsers, return the trajectory
            if not self._active_parser_queue:
                return trajectory # return empty trajectory
            # otherwise, get the next parser
            return self._read_n_steps(n_steps)

        # case 2: trajectory is not empty
        else:
            deleted_step = False
            if (
                # this is not the first parser
                bool(self._inactive_parser_stack)
                # we want to discard the first frame
                and self._discard_first_steps
                # we read the traj from the beginning
                and not self._steps_read
            ):
                trajectory.remove_first_frame()
                deleted_step = True
            self._steps_read += trajectory.n_frames + deleted_step

            if n_steps != -1:
                n_steps -= len(trajectory)
            if n_steps != 0:
                trajectory.append_data(self._read_n_steps(n_steps))
                return trajectory
            else: # n_steps == 0
                return trajectory


    def parse(self, n_steps: int = -1) -> Trajectory:
        """
        Read a given number of steps from all parsers and return a trajectory.

        This method serves as the main entry point for reading steps. It
        handles the case when no steps are left to parse and delegates the
        actual reading to the _read_n_steps method.
        """
        # case: no steps left to parse
        if not self._active_parser_queue:
            logging.debug("MultiTrajectoryParser: End of parsers reached.")
            if self._inactive_parser_stack:
                # return an empty traj based on the parser that was last added
                # to the stack s.t. the metadata is still available
                return self._inactive_parser_stack[-1].parse(1)
            else:
                #raise an exception if the user didn't provide any parsers
                raise ValueError("No parsers provided to "
                                 "MultiTrajectoryParser.")

        # recursive execution through _read_n_steps
        trajectory = self._read_n_steps(n_steps)

        return trajectory


################################################################################
# MD job
###############################################################################
class MDJob(Job):
    """
    Job for running a molecular dynamics simulation.
    """

    result: Result

    @dataclass
    class Result(Job.Result, TrajectoryParser):
        """Container for storing MD-Output, and parser."""


class MDJobFactory(ABC):
    """
    Base Class for MDJob factories.
    """

    @abstractmethod
    def create(
        self,
        metadata: MDMetadata,
        initial_geometry: Geometry,
        name: str = None,
    ) -> MDJob:
        """
        create a MDJob
        :param metadata: options and settings for MD
        :param initial_geometry: initial box geometry
        :param name: optional name
        """
