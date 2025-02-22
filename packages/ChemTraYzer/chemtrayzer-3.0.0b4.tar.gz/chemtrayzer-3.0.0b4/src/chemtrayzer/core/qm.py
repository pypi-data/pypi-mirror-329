from __future__ import annotations

from dataclasses import dataclass, field
from collections.abc import Iterable, Sequence
from datetime import timedelta
import re
from typing import Any, Optional, Literal, Protocol

import numpy as np
from pydantic import BaseModel, field_validator

from chemtrayzer.core.periodic_table import Element
from chemtrayzer.engine._submittable import Failure
from chemtrayzer.core.coords import Geometry, ChainOfStates


class QmResourceSpec(BaseModel):
    """specifies the computational resources for QM jobs

    Fields may be integers or mathematical expressions using the variables
    `n_atoms` and `n_heavy` containing the total number of atoms and the number
    of non-hydrogen atoms of the system, respectively. The mathematical
    expressions can contain functions `min()`, `max()`, `abs()`, and `round()`.

    It is recommended to set values based on the type of job, the level of
    theory and system. The default values should work ok for DFT of small
    molecules with medium to large basis sets on CLAIX2023.
    """

    n_cpus_total: int|str = 'min(n_heavy // 4 + 1, 8)'
    """total number of CPUs (may be n_tasks or n_cpus depending on job type)

    default: at most 8 CPUs"""
    runtime: int|str = 'min(max(24, 24 * n_atoms / 100), 5 * 24)'
    """maximum runtime in hours

    default: minimum: 24 hours, maximum: 5 days"""
    memory: int|str = 5200
    """maximum memory per CPU in MB"""

    @field_validator('n_cpus_total', 'runtime', 'memory', mode='after')
    @classmethod
    def check_math_expr(cls, val: int|str) -> int|str:
        # may contain digits, whitespace, arithmetic operators, and the
        # functions abs, min, max, and round
        pattern = (r'^[\d\s\(\)\+\-\*/\.\bmin\b|\babs\b|\bmax\b|\bround\b'
                   r'|\bn_heavy\b|\bn_atoms\b]+$')

        if isinstance(val, str) and not re.match(pattern, val):
            raise ValueError(f'Invalid mathematical expression: "{val}"')

        return val

    def eval(self,
             atoms: Sequence[Element],
             p_type: Literal['shared', 'distributed'] = 'shared'
            ) -> dict[str, Any]:
        """evaluate the expressions for a concrete molecular geometry

        :param atoms: list of atoms, e.g., from Geometry.atom_types
        :param p_type: parallelization type, for shared-memory parallelization,
                       the output contains "n_cpus", for distributed-memory
                       parallelization, the output contains "n_tasks"
        """
        # avoid circular import by importing here
        from chemtrayzer.engine.jobsystem import Memory

        n_atoms = len(atoms)
        n_heavy = sum(1 for atom in atoms if atom.atomic_nr != 1)

        def eval_expr(expr: str|int) -> int:
            if isinstance(expr, int):
                return expr

            return int(eval(expr,
                            {'__builtins__': {'abs': abs, 'min': min,
                                            'max': max, 'round': round}},
                            {'n_atoms': n_atoms, 'n_heavy': n_heavy}))

        match p_type:
            case 'shared':
                n_cpu_key = 'n_cpus'
            case 'distributed':
                n_cpu_key = 'n_tasks'
            case _:
                raise ValueError(f'Illegal value for p_type: {p_type}')

        return {
            n_cpu_key: eval_expr(self.n_cpus_total),
            'runtime': timedelta(hours=eval_expr(self.runtime)),
            'memory': Memory(eval_expr(self.memory), Memory.UNIT_MB)
        }

class OptimizationFailure(Failure):
    """Indicates that a geometry optimization has failed."""


class ImpossibleMultiplicityFailure(Failure):
    """If the combination of n_electrons and the given multiplicity is
    impossible"""

class MaxIterationsReached(OptimizationFailure):
    """Indicates that the maximum number of iterations has been reached."""


@dataclass(frozen=True, kw_only=True)
class OptConvergence:
    """
    A class to define the convergence criteria for geometry optimizations.

    :param max_energy: maximum energy change in Hartree
    :param max_grad: maximum gradient in Hartree/angstrom
    :param rms_grad: root mean square gradient in Hartree/angstrom
    :param max_step: maximum step size in Angstrom
    """
    max_energy: float | None = None
    max_grad: float | None = None
    rms_grad: float | None = None
    max_step: float | None = None
    rms_step: float | None = None

    def __post_init__(self):
        if self.max_energy is not None and self.max_energy <= 0:
            raise ValueError("energy must be non zero and positive")
        if self.max_grad is not None and self.max_grad <= 0:
            raise ValueError("grad must be non zero and positive")
        if self.max_step is not None and self.max_step <= 0:
            raise ValueError("step must be non zero and positive")
        if self.rms_grad is not None and self.rms_grad <= 0:
            raise ValueError("rms_grad must be non zero and positive")
        if self.rms_step is not None and self.rms_step <= 0:
            raise ValueError("rms_step must be non zero and positive")
        if all(value is None for value in (self.max_energy, self.max_grad,
                                           self.rms_grad, self.max_step,
                                           self.rms_step)):
            raise ValueError("At least one convergence criterion must be set")

    @classmethod
    def ams(
        cls,
        quality: Literal["VeryBasic", "Basic", "Normal", "Good", "VeryGood"],
    ):
        return {
            "VeryBasic": cls(max_energy=1e-3, max_grad=1e-1, max_step=1),
            "Basic": cls(max_energy=1e-4, max_grad=1e-2, max_step=0.1),
            "Normal": cls(max_energy=1e-5, max_grad=1e-3, max_step=0.01),
            "Good": cls(max_energy=1e-6, max_grad=1e-4, max_step=0.001),
            "VeryGood": cls(max_energy=1e-7, max_grad=1e-5, max_step=0.0001),
        }[quality]

    @classmethod
    def gaussian(
        cls, quality: Literal["loose", "normal", "tight", "verytight"]
    ):
        return {
            "loose": cls(
                max_grad=2.5e-3,
                rms_grad=1.7e-3,
                max_step=1e-2,
                rms_step=6.7e-3,
            ),
            "normal": cls(
                max_grad=4.5e-4,
                rms_grad=3e-4,
                max_step=1.8e-3,
                rms_step=1.2e-3,
            ),
            "tight": cls(
                max_grad=1.5e-5, rms_grad=1e-5, max_step=6e-5, rms_step=4e-5
            ),
            "verytight": cls(
                max_grad=2e-6, rms_grad=1e-6, max_step=6e-6, rms_step=4e-6
            ),
        }[quality]

    @classmethod
    def turbomole(cls, quality=None):
        return cls(
            max_energy=1e-6,
            max_grad=5e-4,
            rms_grad=5e-4,
            max_step=1e-3,
            rms_step=5e-4,
        )

    @classmethod
    def baker(cls, quality=None):
        """J. Baker, J. Comp. Chem. 14,1085 (1993)"""
        return cls(max_grad=3e-4, rms_grad=2e-4, max_step=3e-4, rms_step=2e-4)


@dataclass(kw_only=True)
class OptResult:
    """results of a geometry optimization."""

    geometries: Sequence[Geometry]
    """last element of the list contains the optimized geometry, if converged
    [Angstrom]
    """
    energies: np.ndarray
    """one-dimensional array of energies in same order as geometries
    [Hartree]"""
    gradients: np.ndarray | None = None
    """n x m array containing the cartesian gradient(s) where n is the number
    of geometries and m is 3 x n_atoms. [Hartree/a_0]
    """
    hessians: np.ndarray | None = None
    """n x m x m array containing the Hessian where n is the
    number of geometries and m is 3 x n_atoms. [Hartree/a_0^2]
    """
    final: FreqResult | None = None
    """Contains frequency information for the optimized geometry, if available.

    If converged, `final.energy` will be set based on `energies`, if not set
    explciitly
    """

    def __post_init__(self):
        n_geos = len(self.geometries)

        self.energies = np.array(self.energies)

        if len(self.energies) != n_geos:
            raise ValueError(
                "energies and geometries must have the same length"
            )
        if self.gradients is not None and self.gradients.shape[0] != n_geos:
            raise ValueError(
                "energies, geometries and gradients must have the same length"
            )
        if self.hessians is not None and self.hessians.shape[0] != n_geos:
            raise ValueError(
                "energies, geometries and hessians must have same length"
            )
        if self.final is not None:
            if self.final.energy is None:
                self.final.energy = self.energies[-1]
            elif self.final.energy != self.energies[-1]:
                raise ValueError('final.energy and energies are inconsistent.')


@dataclass(kw_only=True)
class TSOptResult(OptResult):
    """results of a TS optimization."""

class OptSubmittable(Protocol):
    """
    A class to define a general geometry optimization (can be a job or an
    investigation)
    """

    result: OptResult
    """result of the geometry optimization procedure"""
    convergence: OptConvergence | None = None
    """convergence criteria"""

class TSOptSubmittable(OptSubmittable):
    """
    A class to define the submittable transition state geometry optimization as
    a job or investigation
    """

    result: TSOptResult

@dataclass(kw_only=True)
class EnergyResult:
    """
    A class to define the result of an energy calculation.
    """

    energy: float
    """total electronic energy [Hartree]"""
    gradient: np.ndarray | None = None
    """gradient of the energy [Hartree/a_0]"""
    hessian: np.ndarray | None = None
    """m x m array containing the Hessian [Hartree/a_0^2]
    """

class EnergySubmittable(Protocol):
    """
    A class to define the submittable energy calculation as a job or
    investigation
    """

    result: EnergyResult

@dataclass(kw_only=True)
class FreqResult:
    """holds data generated by a frequency calculation"""

    frequencies: list[float]
    """harmonic oscillator frequencies [1/cm]"""
    hessian: np.ndarray
    """Hessian matrix [Hartree/a_0^2]"""
    energy: float | None = None
    """total energy [Hartree]"""
    gradient: np.ndarray | None = None
    """Cartesian gradient [Hartree/a_0]"""
    ir_intensities: np.ndarray | None = None
    """IR intensities belonging to the frequencies [KM/Mole]"""
    rotational_symmetry_nr: int | None = None
    """rotational symmetry number"""

class FreqSubmittable(Protocol):
    """
    A class to define the submittable frequency calculation as a job or
    investigation
    :param result: result of the frequency calculation
    :type result: FreqResult
    """

    result: FreqResult


@dataclass(kw_only=True)
class IRCResult:
    """
    A class to define the result of an intrinsic reaction coordinate
    calculation.
    """

    forward_geometries: Sequence[Geometry] = field(default_factory=list)
    """geometries in "forward" direction [Angstrom]"""
    forward_energies: list[float] = field(default_factory=list)
    """electronic energies belonging to forward_geometries [Hartree]"""
    forward_gradients: Optional[list[np.ndarray]] = None
    """gradients belonging to forward_geometries [Hartree/a_0]"""
    reverse_geometries: Sequence[Geometry] = field(default_factory=list)
    """geometries in "reverse" direction [Angstrom]"""
    reverse_energies: list[float] = field(default_factory=list)
    """electronic energies belonging to reverse_geometries [Hartree]"""
    reverse_gradients: Optional[list[np.ndarray]] = None
    """gradients belonging to reverse_geometries [Hartree/a_0]"""

    def __post_init__(self):
        if self.forward_gradients is not None:
            if (
                not len(self.forward_geometries)
                == len(self.forward_energies)
                == len(self.forward_gradients)
            ):
                raise ValueError(
                    "energies, geometries and gradients must have the same "
                    "length"
                )
        else:
            if not len(self.forward_geometries) == len(self.forward_energies):
                raise ValueError(
                    "energies and geometries must have the same length"
                )

        if self.reverse_gradients is not None:
            if (
                not len(self.reverse_geometries)
                == len(self.reverse_energies)
                == len(self.reverse_gradients)
            ):
                raise ValueError(
                    "energies, geometries and gradients must have the same "
                    "length"
                )
        else:
            if not len(self.reverse_geometries) == len(self.reverse_energies):
                raise ValueError(
                    "energies and geometries must have the same length"
                )


class IRCSubmittable(Protocol):
    """
    A class to define the submittable intrinsic reaction coordinate calculation
    as a job or investigation
    :param result: result of the intrinsic reaction coordinate calculation
    """

    result: IRCResult


@dataclass(frozen=True)
class NEBOptions:
    """
    :ivar climbing_image: Activates the Climbing Image
    :ivar climbing_shreshold: Sets the threshold for convergence of the
                              Climbing Image in Hartree/bohr
    :ivar free_end: Endpoints are fixed during calculation if False.
    :ivar spring: Force constant of spring in Hartree/bohr^2
    :ivar optimize_ends: If endpoints should be Optimized before optimization.
    """
    climbing_image: bool = False
    climbing_threshold: float | None = None #Hartree/bohr
    free_end: bool = False
    spring: float = 1.0  # Hartree/bohr^2
    optimize_ends: bool = False

    def __post_init__(self):
        if self.climbing_image is True:
            if self.climbing_threshold is None or self.climbing_threshold <= 0:
                raise ValueError("climbing_threshold must be non zero and "
                                 "positive")
        elif self.climbing_threshold is not False:
            if self.climbing_threshold not in (None, 0):
                raise ValueError("climbing_threshold must be None or False")

        if self.spring <= 0:
            raise ValueError("spring must be non zero and positive")

        if self.free_end is True and self.optimize_ends is True:
            raise ValueError("If NEB endpoints are preoptimized it is useless "
                             "to use free end during NEB optimizations.")


@dataclass
class NEBResult:
    """Container for storing NEB-Output"""

    cos: ChainOfStates = field(default_factory = lambda: ChainOfStates())
    """Chain of states"""
    energies: list[float] = field(default_factory=list)
    """energies of the images [Hartree]"""


class NEBSubmittable(Protocol):
    """
    A class to define the submittable NEB calculation as a job or investigation
    """
    result : NEBResult
    neb_options: NEBOptions | None = None


def lowest_multiplicity(atom_types: Iterable[Element], charge: int = 0
                        ) -> Literal[1,2]:
    """
    Distinguishes between even and odd number of electrons.
    Returns the lowest possible spin multiplicities for a given set of atom
    types and charge.
    To get the next higher possible spin multiplicity, add 2 to the result.
    :param atom_types: atom types
    :param charge: charge
    :return: lowest possible multiplicity
    """
    n_electrons = sum(atom_type.atomic_nr for atom_type in atom_types) - charge
    return 1 if n_electrons % 2 == 0 else 2
