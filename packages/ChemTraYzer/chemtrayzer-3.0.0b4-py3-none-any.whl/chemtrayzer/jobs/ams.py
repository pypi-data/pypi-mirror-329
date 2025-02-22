"""
This module contains classes to read calculations with AMS.
"""

from __future__ import annotations

import logging
from abc import abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar, Literal, Optional, Union, TYPE_CHECKING
from functools import lru_cache

import numpy as np
import pydantic
import scipy.sparse
import scm.plams as plams
from scm.plams import Molecule, Settings
from scm.plams.interfaces.adfsuite.ams import AMSJob as PlamsAMSJob

import chemtrayzer.core.qm as qm
from chemtrayzer.core.coords import ChainOfStates, Geometry
from chemtrayzer.core.graph import MolGraph
from chemtrayzer.core.lot import (
    LevelOfTheory,
    MolecularMechanics,
    QCMethod,
)
from chemtrayzer.core.md import (
    PSTAT_NOT_SET,
    TSTAT_NOT_SET,
    BerendsenPStat,
    BerendsenTStat,
    BoxType,
    MDBarostat,
    MDBox,
    MDIntegrator,
    MDJob,
    MDJobFactory,
    MDMetadata,
    MDThermostat,
    MTKPStat,
    NoseHooverTStat,
    Trajectory,
    TrajectoryParser,
)
from chemtrayzer.core.periodic_table import PERIODIC_TABLE as PTOE
from chemtrayzer.core.periodic_table import Element
from chemtrayzer.engine.jobsystem import (
    Job,
    JobTemplate,
    Memory,
    Program,
    Version,
)

if TYPE_CHECKING:
    from collections.abc import Sequence
    from datetime import timedelta
    from os import PathLike


@pydantic.dataclasses.dataclass
class _MolecularDynamicsBlock:
    """data structure for storing data in General > user input
      > MolecularDynamcis

    Here, we use pydantic for automatic type conversion. The variable names are
    not PEP8 conform because they correspond to the names in the RKF file.
    Default values were taken from
    https://www.scm.com/doc/AMS/Tasks/Molecular_Dynamics.html#general
    """

    @pydantic.dataclasses.dataclass
    class BarostatBlock:
        Pressure: float
        Tau: float
        Type: Literal["Berendsen", "MTK", "None"]
        BulkModulus: float = 2200000000.0
        ConstantVolume: bool = False
        Duration: list[int] | None = None
        Equal: Literal["None", "XYZ", "XY", "YZ", "XZ"] | None = None
        Scale: Literal["XYZ", "Shape", "X", "Y", "Z", "XY", "YZ", "XZ"] = "XYZ"

    @pydantic.dataclasses.dataclass
    class ThermostatBlock:
        Tau: float
        Temperature: float
        Type: Literal["None", "Berendsen", "NHC"]
        BerendsenApply: Literal["Local", "Global"] = "Global"
        ChainLength: int = 10
        Duration: list[int] | None = None

    @pydantic.dataclasses.dataclass
    class ConstraintsBlock:
        Atom: int | None = None
        AtomList: list[int] | None = None
        FixedRegion: str | None = None

    @pydantic.dataclasses.dataclass
    class TrajectoryBlock:
        PrintFreq: int | None = None
        SamplingFreq: int = 100
        WriteBonds: bool = True
        WriteCharges: bool = True
        WriteEndingeGradients: bool = False
        WriteCoordinates: bool = True
        WriteMolecules: bool = True
        WriteVelocities: bool = True

    Trajectory: TrajectoryBlock = pydantic.Field(
        default_factory=TrajectoryBlock
    )
    Barostat: BarostatBlock | None = None
    Thermostat: ThermostatBlock | None = None
    NSteps: int = 1000
    TimeStep: float = 0.25
    Constraints: ConstraintsBlock | None = None

    @pydantic.computed_field
    @property
    def thermostat(self) -> MDThermostat:
        if self.Thermostat is None:
            return TSTAT_NOT_SET

        match self.Thermostat.Type:
            case "None":
                return TSTAT_NOT_SET
            case "Berendsen":
                return BerendsenTStat(
                    tau=self.Thermostat.Tau,
                    temperature=self.Thermostat.Temperature,
                )
            case "NHC":
                return NoseHooverTStat(
                    tau=self.Thermostat.Tau,
                    temperature=self.Thermostat.Temperature,
                    chain_length=self.Thermostat.ChainLength,
                )
            case _:
                raise NotImplementedError(
                    f"Thermostat type {self.Thermostat.Type} not supported"
                )

    @pydantic.computed_field
    @property
    def barostat(self) -> MDBarostat:
        if self.Barostat is None:
            return PSTAT_NOT_SET

        match self.Barostat.Type:
            case "None":
                return PSTAT_NOT_SET
            case "Berendsen":
                return BerendsenPStat(
                    tau=self.Barostat.Tau, pressure=self.Barostat.Pressure
                )
            case "MTK":
                return MTKPStat(
                    tau=self.Barostat.Tau, pressure=self.Barostat.Pressure
                )
            case _:
                raise NotImplementedError(
                    f"Barostat type {self.Barostat.Type} not supported"
                )


@pydantic.dataclasses.dataclass
class _UserInput:
    """data structure for storing user input variable in general section"""

    MolecularDynamics: _MolecularDynamicsBlock | None = None

    @classmethod
    def from_str(cls, s: str) -> _UserInput:
        lines = s.splitlines()

        for i, line in enumerate(lines):
            # currently the only block we can read
            if line.strip() == "MolecularDynamics":
                md_block, _ = cls._read_block(lines, i + 1)
                break

        return _UserInput(MolecularDynamics=md_block)

    @classmethod
    def _read_block(cls, lines: list[str], pos: int) -> tuple[dict, int]:
        """
        :param lines: string representation of block as read from rkf file
        :param pos: current position in lines
        :return: block as dictionary, new position
        """
        block = {}

        for _ in range(len(lines)):
            line = lines[pos]
            words = line.split()
            if words[0] == "End":
                return (block, pos)

            if len(words) == 1:
                block[words[0]], pos = cls._read_block(lines, pos + 1)

            else:
                block[words[0]] = " ".join(words[1:])

            pos += 1

        raise RuntimeError(
            "End of user input string reached before end " "of block."
        )


class AMSParser:
    r"""
    A parser of AMS \*.rkf files.

    :param path: file path to the \*.rkf
    :type path: Path
    """

    required_section_names: ClassVar[Sequence[str]] = ("General",)

    def __init__(self, path: Path):
        # KFReader: Python reader for AMS files, without udmpkf, no writing
        # convert in case other PathLike class is used
        self.path = Path(path).resolve()

        self._kf = plams.KFReader(str(self.path))

        # get data structure from RKF:
        # {section1: [var1,var2,...], section2: ...}
        self._kf._create_index()
        self.sections = {
            key: list(self._kf._sections[key].keys())
            for key in self._kf._sections
        }
        self.termination_status = self._get_termination_status()

    def ams_engine_lookup(
        self, ams_engine_string, additional_string_1="", additional_string_2=""
    ):
        """
        Translator for MD engine details found in RKF files into CTY level of
        theory types.

        :param ams_engine_string: Main identifier, e.g. "reaxff" or "dftb"
        :type ams_engine_string: str
        :param additional_string_1: Optional secondary identifier, e.g.
                                    "GF1-XTB"
        :type additional_string_1: str
        :param additional_string_2: Optional tertiary identifier, e.g.
                                    the parametrization name
        :type additional_string_2: str
        :return: CTY level of theory, e.g. "MolecularMechanics.GFN_FF"
        :rtype: LevelOfTheory
        """
        if ams_engine_string == "reaxff":
            # TODO too general: get exact name of force field
            return MolecularMechanics.REAX_FF
        elif ams_engine_string == "dftb":
            if additional_string_1 == "":
                # TODO check which method name should be returned
                raise NotImplementedError
            elif (
                additional_string_1 == "GFN1-xTB"
                or additional_string_1 == "GF1-XTB"
            ):
                QCMethod.GFN_xTB
            elif additional_string_1 == "DFTB":
                # TODO check which method name should be returned
                raise NotImplementedError
                # additional_string_2 == 'DFTB.org/3ob-3-1'
                return (
                    MolecularMechanics.GFN_FF
                )  # should be MolecularMechanics.DFTB

    def _get_termination_status(self):
        """
        Reads the termination status from the .rkf file
        """
        return self._kf.read("General", "termination status")

    def _atom_types(self) -> tuple[Element]:
        """
        Returns the elements of the trajectory in order of atom id

        :return: list of elements
        :rtype: List[Element]
        """
        atnums = self._kf.read("InputMolecule", "AtomicNumbers")
        if not isinstance(atnums, list):
            return tuple(
                PTOE[atnums],
            )
        return tuple([PTOE[nr] for nr in atnums])

    def _get_level_of_theory(self):
        """
        Reads the engine name and possibly the parametrization name from the
        RKF and translates it into CTY level of theory.

        :return: level of theory
        :rtype: LevelOfTheory
        """
        ams_engine_string = self._kf.read("General", "engine")
        additional_string_1 = additional_string_2 = ""
        user_input = self._kf.read("General", "user input")
        # parse Engine section of AMS input
        inside_block = False
        for line in user_input.splitlines():
            if line.startswith("Engine"):
                inside_block = True
                continue

            if inside_block and line.startswith("EndEngine"):
                inside_block = False
                break

            if inside_block:
                if "Model" in line:
                    additional_string_1 = line.split()[1]
                if "ForceField" in line:
                    additional_string_1 = line.split()[1]
                if "ResourcesDir" in line:
                    additional_string_2 = line.split()[1]

        pes = self.ams_engine_lookup(
            ams_engine_string, additional_string_1, additional_string_2
        )
        return LevelOfTheory(method=pes)

    def get_engine_filepath(self) -> Path:
        """
        Returns the path to the engine output file from the RKF file

        :return: path to the engine output file
        :rtype: Path
        """
        return self.path.parent / self._kf.read("EngineResults", "Files(1)")

    def get_coords(self) -> np.array:
        """
        Reads the last coordinates from the engine file

        :return: Coordinates
        :rtype: np.array
        """
        return np.reshape(
            np.array(self._kf.read("Molecule", "Coords")), (-1, 3)
        )

    def get_energy(self) -> float:
        """
        Reads the last energy from the engine file

        :return: Energy
        :rtype: float
        """
        return self._kf.read("AMSResults", "Energy")

    def get_forces(self) -> np.array:
        """
        Reads the last gradients from the engine file

        :return: Forces
        :rtype: np.array
        """
        forces = self._kf.read("AMSResults", "Gradients")
        return np.reshape(np.array(forces), (-1, 3))

    def get_hessian(self) -> np.array:
        """
        Reads the last hessian from the engine file

        :return: Hessian
        :rtype: np.array
        """

        hessian = self._kf.read("AMSResults", "Hessian")
        size = int(np.sqrt(len(hessian)))
        return np.reshape(np.array(hessian), (size, size))

    def get_frequencies(self) -> tuple[float]:
        """
        Reads the vibrational frequencies from the engine file

        :return: Frequencies
        :rtype: tuple[float]
        """
        return tuple(self._kf.read("Vibrations", "Frequencies[cm-1]"))

    def get_n_entries(self) -> int:
        """
        Reads the number of entries from the engine file

        :return: Number of entries
        :rtype: int
        """
        return self._kf.read("History", "nEntries")

    def _get_initial_lattice_vectors_and_pbc(
        self,
    ) -> tuple[np.ndarray | None, tuple[bool, bool, bool]]:
        """
        Reads the first lattice vectors from the RKF.

        :return: lattice vectors
        :rtype: numpy ndarray, shape (3,3) or (3)
        """
        try:
            pbc = {
                3: (True, True, True),
                2: (True, True, False),
                1: (True, False, False),
                0: (False, False, False),
            }[self._kf.read("InputMolecule", "nLatticeVectors")]

            lattice_vectors_tuple = self._kf.read(
                "InputMolecule", "LatticeVectors"
            )

        except KeyError:
            lattice_vectors = None  # (None, None, None)
            pbc = (False, False, False)

        else:
            # according to the AMS doc, the lattice vector of a chain system
            # must point in the x-direction, and for a slab system, the vectors
            # must be in the xy-plane -> expect respective pbc definition
            if pbc == (True, True, True):
                lattice_vectors = (
                    np.array(lattice_vectors_tuple).reshape(3, 3)
                    * 0.529177210903
                )

            elif pbc == (True, True, False):
                lattice_vectors_tuple += [0.0, 0.0, 0.0]
                lattice_vectors = (
                    np.array(lattice_vectors_tuple).reshape(3, 3)
                    * 0.529177210903
                )

            elif pbc == (True, False, False):
                lattice_vectors_tuple += [
                    0.0,
                ] * 6
                lattice_vectors = (
                    np.array(lattice_vectors_tuple).reshape(3, 3)
                    * 0.529177210903
                )
            else:
                raise ValueError(
                    "Unexpected periodic boundary conditions. "
                    "Expected lattice vectors in the xyz"
                    "directions, just the xy-plane or just the"
                    "x-axis."
                )

        return lattice_vectors, pbc


class AMSTrajectoryParser(AMSParser, TrajectoryParser):
    r"""
    A parser of AMS \*.rkf files.

    :param path: file path to the \*.rkf
    :type path: Path
    """

    required_section_names: ClassVar[Sequence[str]] = (
        "General",
        "History",
        "InputMolecule",
    )

    def __init__(self, path: Path) -> None:
        super().__init__(path)

        self._next_frame = 0        # zero-based

        self._next_frame = 0  # zero-based

        self._check_available_sections()

        # are there bonds and charges?
        self.has_bonds = "Bonds.Index(1)" in self.sections["History"]
        self.has_charges = (
            "MDHistory" in self.sections
            and "Charges(1)" in self.sections["MDHistory"]
        )
        self.has_lattice = "LatticeVectors" in self.sections["InputMolecule"]

        # some extra variables
        self.n_frames = self._n_frames
        self.atom_types = self._atom_types()

    def _check_available_sections(self) -> None:
        """
        Checks the sections in the RKF and throws an error if something is
        missing. Currently, the required sections are: "General", "History",
        "InputMolecule", "General.engine", "General.terminationstatus"
        "InputMolecule.AtomicNumbers", "InputMolecule.LatticeVectors",
        "History.nEntries", "History.Coords(1)".
        """

        if any(
            name not in self.sections for name in self.required_section_names
        ):
            logging.error(
                "This AMS trajectory is missing one of the required data "
                f"sections: {'/'.join(self.required_section_names)}"
            )

        if (
            ("engine" not in self.sections["General"])
            or ("termination status" not in self.sections["General"])
            or ("AtomicNumbers" not in self.sections["InputMolecule"])
            or ("LatticeVectors" not in self.sections["InputMolecule"])
            or ("nEntries" not in self.sections["History"])
            or ("Coords(1)" not in self.sections["History"])
        ):
            logging.error(
                "This AMS trajectory is missing one of the required data "
                "fields:engine/AtomicNumbers/LatticeVectors/nEntries/Coords(1)"
            )

    @property
    @lru_cache(maxsize=1)
    def _n_atoms(self) -> int:
        """
        Reads the number of atoms from the RKF.
        lrucache is used to avoid multiple reads of the same value.

        :return: number of atoms
        :rtype: int
        """
        return self._kf.read("InputMolecule", "nAtoms")

    @property
    @lru_cache(maxsize=1)
    def _n_frames(self) -> int:
        """
        Reads the number of frames from the RKF.
        lrucache is used to avoid multiple reads of the same value.

        :return: number of frames
        :rtype: int
        """
        return self._kf.read("History", "nEntries")

    def _get_integration_time(self) -> float:
        """
        Reads the integration time step from the RKF. It is assumed that the
        integration step is constant throughout the trajectory.
        RKFs don't store the time step directly, because it can be variable.
        Returns the AMS default time step of 0.25 fs in case of missing
        information.

        :return: integration time step in femtoseconds
        :rtype: float
        """
        dt = 0.0
        if "MDHistory" in self.sections:
            data_block_size = self._kf.read("MDHistory", "blockSize")
            steps = self._kf.read("MDHistory", "Step(1)")
            times = self._kf.read("MDHistory", "Time(1)")
            # check first 5 entries. time steps might vary in geometry
            # optimizations with AMS
            dts = [
                (times[i + 1] - times[i]) / (steps[i + 1] - steps[i])
                for i in range(min(data_block_size - 1, 5))
            ]
            dt = dts[0]
            if any(round(d, 4) != round(dt, 4) for d in dts[1:]):
                logging.warning(
                    "Time steps and MD steps have a varying ratio: "
                    f"{'/'.join(map(str, dts))}... . The integration time "
                    f"step is not constant. Set to {dt} fs"
                )
        elif "MDResults" in self.sections:
            # look in MD section
            start_step = self._kf.read("MDResults", "StartStep")
            end_step = self._kf.read("MDResults", "EndStep")
            start_time = self._kf.read("MDResults", "StartTime[fs]")
            end_time = self._kf.read("MDResults", "EndTime[fs]")
            dt = (end_time - start_time) / (end_step - start_step)
        if dt == 0.0:
            # AMS default
            logging.warning(
                "Integration time step was not found. Set to 0.25."
            )
            dt = 0.25
        return dt

    def _get_average_temperature(self):
        """
        Reads the average temperature from the RKF. Issues a warning if the
        standard deviation of temperature is greater than expected for an NVT
        ensemble (stdev > <T>/sqrt(N)).

        :return: average temperature in Kelvin
        :rtype: float
        """
        avg_temp = 0
        if "MDResults" in self.sections:
            avg_temp = self._kf.read("MDResults", "MeanTemperature")
            dev_temp = self._kf.read("MDResults", "StdDevTemperature")
            if dev_temp > avg_temp / len(self.atom_types) ** 0.5:
                logging.info(
                    "The standard deviation of temperature in this "
                    "trajectory is bigger than expected for a NVT ensemble "
                    f"({dev_temp}>{avg_temp}/sqrt({len(self.atom_types)}))."
                )
        else:
            logging.warning("The temperature was not found.")
        return avg_temp

    def _read_metadata(self):
        """
        initial_box: MDBox
        level_of_theory: LevelOfTheory
        number_of_steps: int
        timestep: float
        integration_method: MDIntegrator
        sampling_frequency: int
        pressure: float
        barostat: MDBarostat
        thermostat: MDThermostat
        temperature: float
        path: Path
        """
        user_input_str = self._kf.read("General", "user input")
        user_input = _UserInput.from_str(user_input_str)
        md_block = user_input.MolecularDynamics

        lattice_vectors, pbc = self._get_initial_lattice_vectors_and_pbc()

        if lattice_vectors is not None:
            # current definition: vectors are the columns -> transpose
            lattice_vectors = lattice_vectors.T

        metadata = MDMetadata(
            # do boxes in ams always start at 0,0,0? How to get the box origin?
            initial_box=MDBox(
                box_origin=(0.0, 0.0, 0.0),
                box_vectors=lattice_vectors,
                box_type=BoxType.from_box_vectors(lattice_vectors),
                pbc=pbc,
            ),
            level_of_theory=self._get_level_of_theory(),
            number_of_steps=self.n_frames,
            timestep=self._get_integration_time(),
            # AMS always uses Velocity_Verlet
            integration_method=MDIntegrator.VELOCITY_VERLET,
            sampling_frequency=md_block.Trajectory.SamplingFreq,
            barostat=md_block.barostat,
            thermostat=md_block.thermostat,
        )
        return metadata

    def _get_graphs(self, n_steps, connectivity) -> list[MolGraph]:
        """
        Reads the bond information from the RKF, and translates it to Graphs.

        :return: list of graphs
        """

        graphs = []
        for i in range(n_steps):
            graphs.append(
                MolGraph.from_atom_types_and_bond_order_matrix(
                    self.atom_types,
                    connectivity[i],
                    threshold=0.01,
                    include_bond_order=True,
                )
            )
        return graphs

    def _read(self, n_steps: int) -> tuple[np.ndarray, np.ndarray, list]:
        """
        Reads n_steps from the RKF file. If the remaining trajectory is shorter
        than n_steps, the returned arrays are resized accordingly.

        :return: coordinates (n_steps x n_atoms x 3),
                 charges (n_steps x n_atoms), and
                 connectivities (list of scipy sparse matrices)
        """
        coords, charges, connectivities = self._init_arrays(n_steps)

        i = 0  # if n_steps = 0
        try:
            for i in range(n_steps):
                frame = self._next_frame + i + 1  # one-based
                coords[i] = np.reshape(
                    self._kf.read("History", f"Coords({frame})"),  # type: ignore
                    (-1, 3),
                )
                charges[i] = self._kf.read("MDHistory", f"Charges({frame})")

                connectivities.append(self._get_connectivity(frame))
        except KeyError:
            # means the frame number requested does not exist, trajectory is
            # shorter, last step not read
            i -= 1

        self._next_frame += i + 1

        # Unit conversion Bohr->Angstrom. Faster than plams.Unit.convert
        coords *= 0.529177210903

        # trajectory ended before n_steps could be read -> resize
        if i < n_steps - 1:
            coords = coords[: i + 1]
            connectivities = connectivities[: i + 1]
            charges = charges[: i + 1]

        return coords, charges, connectivities

    def _init_arrays(
        self, n_steps: int
    ) -> tuple[np.ndarray, np.ndarray, list]:
        """
        :return: empty arrays for coordinates, charges, and connectivities
        """
        coords = np.zeros((n_steps, self._n_atoms, 3))
        charges_list = np.zeros((n_steps, self._n_atoms))

        return coords, charges_list, []

    def _get_connectivity(self, frame) -> scipy.sparse.csr_array:
        """
        Reads the bond information from the RKF. Returns a 3D array of
        connectivities, where frames is the first dimension, and atom ids are
        the remaining ones.

        :frame: one-based frame number to get the connectivity from
        :return: list of lower triangular matrices of connectivities per frame.
        :rtype: scipy sparse csr matrix
        """

        # bonds_atoms[bonds_index[i]-1:bonds_indsx[i+1]-1] contains the
        # one-based atom ids of atoms bonded to atom i, and
        # bonds_atoms[bonds_index[i]-1:bonds_indsx[i+1]-1] contains the
        # respective bonds orders.
        bonds_index = self._kf.read("History", f"Bonds.Index({frame})")
        bonds_atoms = self._kf.read("History", f"Bonds.Atoms({frame})")
        bonds_orders = self._kf.read("History", f"Bonds.Orders({frame})")

        # the above arrays are essentially a lower triangular matrix of
        # bond orders in CSR format
        conn_arr = scipy.sparse.csr_array(
            (
                bonds_orders,
                np.array(bonds_atoms) - 1,  # one-based atom ids
                np.array(bonds_index) - 1,
            ),
            shape=(self._n_atoms, self._n_atoms),
            dtype=float,
        )

        return conn_arr

    def parse(self, n_steps: int = -1) -> Trajectory:
        """
        read from AMS RKF file into a Result object that contains the
        Trajectory
        :return: Result
        """
        if n_steps == -1:
            n_steps = self._n_frames

        coords, charges, connectivity = self._read(n_steps)

        traj = Trajectory(
            metadata=self._read_metadata(),
            atom_types=self._atom_types(),
            coords=coords,
        )

        # correct for actually read
        n_read = traj.n_frames

        # add path
        traj.path = self.path

        # add connectivity
        traj.graphs = (
            self._get_graphs(n_read, connectivity) if self.has_bonds else None
        )

        # add charges
        traj.charges = charges if self.has_charges else None

        return traj


class AMS(Program):
    """AMS molecular dynamics program. Should store all necessary information
    regarding the AMS software, that is not affected by specific jobs"""

    def __init__(
        self,
        amshome: Path,
        scmlicense: Path,
        version: Optional[Version] = None,
        scm_opengl_software: Literal["0", "1"] = "1",
    ) -> None:
        super().__init__(executable="", version=version)
        self.amshome = amshome
        self.scmlicense = scmlicense
        self.scm_opengl_software = scm_opengl_software


class AMSJob(Job):
    """Base class for all AMS job objects"""

    ams_settings: Settings

    _CMD_TMPL = '''
export AMSHOME=${amshome}
export AMSBIN=$AMSHOME/bin
export AMSRESOURCES=$AMSHOME/atomicdata
export SCM_OPENGL_SOFTWARE=${scm_opengl_software}
export SCMLICENSE=${scmlicense}
export NSCM=${n_tasks}

AMS_JOBNAME="ams" AMS_RESULTSDIR=. $AMSBIN/ams <"ams.in"'''

    _INPUT_TMPLS = {"ams.in": ""}

    def __init__(
        self,
        program: AMS,
        *,
        lot: Optional[LevelOfTheory] = None,
        reaxff_path: Optional[Path] = None,
        forcefield: Optional[str] = None,
        extra_settings: Optional[Settings] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        if self.n_cpus != 1:
            raise ValueError("AMS uses MPI. Only n_tasks supported.")

        self.ams_settings = (
            extra_settings if extra_settings is not None else Settings()
        )
        # set up the paths pointing to the corresponding
        # ams installation and license file
        self.program = program
        self.amshome = program.amshome
        self.scmlicense = program.scmlicense
        self.scm_opengl_software = program.scm_opengl_software
        self._template: JobTemplate = JobTemplate(
            self, self._CMD_TMPL, self._INPUT_TMPLS
        )
        # Set up the bash settings for the AMS job
        self.lot = lot

        if self.lot is not None:
            # if the method specified in metadata is ReaxFF,
            # create a job with ReaxFF settings
            if self.lot.method == MolecularMechanics.REAX_FF:
                if forcefield is None or reaxff_path is None:
                    raise ValueError(
                        "Forcefield and path must be provided for ReaxFF "
                        "calculations"
                    )
                else:
                    self.ams_settings.input.ReaxFF.ForceField = (
                        reaxff_path / forcefield
                    ).name

            elif self.lot.method == QCMethod.GFN_xTB:
                self.ams_settings.input.DFTB.Model = "GFN1-xTB"

            else:
                raise NotImplementedError(
                    f"{self.lot} is not supported by {self.__class__}"
                )

    def gen_input(self, path: Union[str, PathLike]):
        _path = Path(path)
        plamsjob: PlamsAMSJob = PlamsAMSJob(
            molecule=getattr(self, "plams_mol", None),
            settings=self.ams_settings,
            name="ams",
        )

        inputscript = plamsjob.get_input()

        self._INPUT_TMPLS["ams.in"] = inputscript
        if getattr(self, "_template", None) is None:
            raise ValueError("Template not set")

        self._template.gen_input(_path)

    @property
    def command(self):
        return self._template.command

    @abstractmethod
    def parse_result(self, path: Path): ...

@dataclass(kw_only=True)
class AMSMDSettings:
    """
    Settings to be passed to the AMS_MD_Job. Supports all currently implemented
    settings for the Molecular dynamics Job API in AMS molecular dynamics
    software, that are not covered by the MDMetadata class. Check the PLAMS
    documentation for more information on available settings and functionality
    at https://www.scm.com/doc/plams/examples/MDJobs.html?highlight=plams

    To implement settings that are currently not supported by this class, use
    the user_settings parameter in the AMS_MD_Job class to pass a dictionary
    with the settings to the AMS directly.

    Trajectory options:

    :param checkpointfrequency: How frequently to write MDStep*.rkf checkpoint
                                files. Defaults to None.
    :type checkpointfrequency: int, optional
    :param writevelocities: Whether to save velocities to ams.rkf (needed for
                            example to restart from individual frames or to
                            calculate velocity autocorrelation functions).
                            Defaults to None.
    :type writevelocities: bool, optional
    :param writebonds: Whether to save bonds to ams.rkf. Defaults to None.
    :type writebonds: bool, optional
    :param writemolecules: Whether to write molecules to ams.rkf. Defaults to
                           None.
    :type writemolecules: bool, optional
    :param writeenginegradients: Whether to save engine gradients (negative of
                                 atomic forces) to ams.rkf. Defaults to None.
    :type writeenginegradients: bool, optional
    :param writecharges: Whether to write charges to ams.rkf. Defaults to None.
    :type writecharges: bool, optional

    :param equal: ‘XYZ’ etc. Defaults to None.
    :type equal: str, optional
    :param scale: ‘XYZ’ etc. Defaults to None.
    :type scale: str, optional
    :param constantvolume: Whether to use constant volume. Defaults to None.
    :type constantvolume: bool, optional

    Other options:
    :param calcpressure: Whether to calculate pressure. Defaults to None.
    :type calcpressure: bool, optional
    :param user_settings: A dictionary with additional user settings that need
                          to be added to the AMS_MD_Settings object. Used to
                          implement settings or that are not supported by plams
                          by default. Check beforehand if the setting you want
                          to specify isn't already implemented in the
                          AMS_MD_Settings class
    :type user_settings: dict, optional

    """

    checkpointfrequency: int = 1000000
    writevelocities: bool = True
    writebonds: bool = True
    writemolecules: bool = True
    writecharges: bool = True
    writeenginegradients: bool = False
    calcpressure: bool = False
    scale: str = "XYZ"
    equal: str = "all"
    constantvolume: bool = False

    _user_settings: dict = field(default_factory=dict)

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def update_with_dict(self, settings: dict) -> None:
        """this function is used to update the AMS_MD_Settings object with a
        dictionary. You can only add or update existing settings that are
        supported by plams. For parameters that are not supported by plams use
        the add_user_setting method

        :param settings: A dictionary with the settings that need to be added
                         to the AMS_MD_Settings object
        """

        for key, value in settings.items():
            if key in self.__dict__:
                self[key] = value
            else:
                raise KeyError(
                    f"{key} is not a valid parameter for AMS_MD_Settings"
                )

    def update_user_setting(self, user_settings: dict) -> None:
        """Using this function the user can add additional user settings to the
           AMS input file, that are not supported by plams by default. However,
           use this method with caution as correct syntax and structure is
           required for the ams input file. Check beforehand if the setting you
           want to specify isn't already implemented in the AMS_MD_Settings
           class

        :param user_settings: A dictionary with the user settings that need to
                              be added to the AMS_MD_Settings object
        """
        self._user_settings.update(user_settings)

    def get_user_setting(self) -> dict:
        """Using this function the user can get the user settings that have
        been added to the AMS_MD_Settings object"""

        return self._user_settings


class AMSMDJob(AMSJob, MDJob):
    @dataclass
    class Result(MDJob.Result):
        _trajectory_parser: AMSTrajectoryParser

        def parse(self, n_steps: int = -1) -> Trajectory:
            return self._trajectory_parser.parse(n_steps=n_steps)

    def __init__(
        self,
        *,
        program: AMS,
        initial_geometry: Geometry,
        metadata: MDMetadata,
        ams_md_settings: Optional[AMSMDSettings] = None,
        plumed_input: Optional[str] = None,
        **kwargs,
    ) -> None:
        super().__init__(
            program=program, lot=metadata.level_of_theory, **kwargs
        )

        if self.lot is None:
            raise ValueError(
                f"Level of theory must be provided for {self.__class__}"
            )

        if (
            metadata.integration_method is not MDIntegrator.VELOCITY_VERLET
            and metadata.integration_method is not None
        ):
            raise ValueError(
                "Only Velocity Verlet integrator is supported by "
                f"{self.__class__}"
            )

        self.ams_settings.input.ams.Task = "MolecularDynamics"
        self.initial_geometry = initial_geometry
        self.ams_md_settings = (
            ams_md_settings if ams_md_settings is not None else AMSMDSettings()
        )
        self.metadata = metadata if metadata is not None else MDMetadata()
        self.plumed_input = plumed_input

        if (
            self.metadata.initial_box.pbc is None
            or self.metadata.initial_box.pbc == (False, False, False)
        ):
            self.plams_mol = Molecule(
                positions=self.initial_geometry.coords,
                numbers=[
                    atom.atomic_nr for atom in self.initial_geometry.atom_types
                ],
            )
        else:
            if (
                self.metadata.initial_box.box_origin is None
                or self.metadata.initial_box.box_vectors is None
                or self.metadata.initial_box.box_type is not BoxType.ORTHOGONAL
            ):
                raise ValueError(
                    f"Only orthogonal boxes are supported by {self.__class__}"
                )
            else:
                self.plams_mol = Molecule(
                    positions=self.initial_geometry.coords,
                    numbers=[
                        atom.atomic_nr
                        for atom in self.initial_geometry.atom_types
                    ],
                    lattice=self.metadata.initial_box.box_vectors,
                )

        md_settings = self.ams_settings.input.ams.MolecularDynamics

        if self.plumed_input is not None:
            md_settings.Plumed.Input = self.plumed_input

        if isinstance(self.metadata.thermostat, BerendsenTStat):
            md_settings.Thermostat.Type = "Berendsen"
            md_settings.Thermostat.Tau = self.metadata.thermostat.tau
            md_settings.Thermostat.Temperature = (
                self.metadata.thermostat.temperature
            )

        elif isinstance(self.metadata.thermostat, NoseHooverTStat):
            md_settings.Thermostat.Type = "NHC"
            md_settings.Tau = self.metadata.thermostat.tau
            md_settings.Thermostat.ChainLength = (
                self.metadata.thermostat.chain_length
            )
            md_settings.Thermostat.Temperature = (
                self.metadata.thermostat.temperature
            )

        elif self.metadata.thermostat is not None:
            raise ValueError(
                "Thermostat {self.metadata.thermostat} is not supported "
                f"by {self.__class__}"
            )

        if isinstance(self.metadata.barostat, BerendsenPStat):
            md_settings.Barostat.Type = "Berendsen"
            md_settings.Barostat.Tau = self.metadata.barostat.tau
            md_settings.Barostat.Pressure = self.metadata.barostat.pressure

        elif isinstance(self.metadata.barostat, MTKPStat):
            md_settings.Barostat.Type = "MTK"
            md_settings.Barostat.Tau = self.metadata.barostat.tau
            md_settings.Barostat.Pressure = self.metadata.barostat.pressure

        elif self.metadata.barostat is not None:
            raise ValueError(
                f"Barostat {self.metadata.barostat} is not supported by "
                f"{self.__class__}"
            )

        md_settings.InitialVelocities.Temperature = (
            self.metadata.thermostat.temperature
        )
        md_settings.InitialVelocities.Type = "Random"

        md_settings.TimeStep = self.metadata.timestep
        md_settings.Trajectory.SamplingFreq = self.metadata.sampling_frequency
        md_settings.NSteps = self.metadata.number_of_steps
        md_settings.Trajectory.WriteVelocities = str(
            self.ams_md_settings["writevelocities"]
        )
        md_settings.Trajectory.WriteBonds = str(
            self.ams_md_settings["writebonds"]
        )
        md_settings.Trajectory.WriteMolecules = str(
            self.ams_md_settings["writemolecules"]
        )

        md_settings.Trajectory.WriteCharges = str(
            self.ams_md_settings["writecharges"]
        )

        md_settings.Trajectory.WriteEngineGradients = str(
            self.ams_md_settings["writeenginegradients"]
        )

        md_settings.CalcPressure = str(self.ams_md_settings["calcpressure"])
        md_settings.Checkpoint.Frequency = self.ams_md_settings[
            "checkpointfrequency"
        ]

    def parse_result(self, path):
        try:
            path = Path(path)
            parser = AMSTrajectoryParser(path=path / "ams.rkf")
            self.result = AMSMDJob.Result(parser)

            if (
                parser.termination_status == "NORMAL TERMINATION"
                or parser.termination_status
                == "NORMAL TERMINATION with warnings"
            ):
                self.succeed()
            else:
                self.fail(reason=parser.termination_status)
        except Exception as err:
            self.fail(reason=err)


@dataclass
class AMSMDJobFactory(MDJobFactory):
    """
    Factory for creating AMS MD Jobs.

    :param ams: AMS software
    :param n_cpus: number of CPUs to use
    :param n_tasks: number of tasks to use
    :param memory: maximum memory per cpu
    :param runtime: maximum runtime
    :param forcefield: The name of the force field file, e.g., "CHON-2019.ff".
    :param reaxff_path: The path to the ReaxFF files.
    :param ams_md_settings: AMSMDSettings object that specifies the parameters
                            for the simulation. Check out the AMSMDSettings
                            class for available parameters and options.
                            Can be updated during the create() call by passing
                            a MDMetadata object.
    """

    def __init__(
        self,
        *,
        program: AMS,
        n_tasks: int,
        memory: Memory,
        runtime: timedelta,
        ams_md_settings: AMSMDSettings,
        forcefield: Optional[str] = None,
        reaxff_path: Optional[Path] = Path(),
        **kwargs,
    ) -> None:
        self.program = program
        self.kwargs = dict(
            n_cpus=1, n_tasks=n_tasks, memory=memory, runtime=runtime
        )
        self.forcefield = forcefield
        self.reaxff_path = reaxff_path
        self.ams_md_settings = ams_md_settings

    def create(
        self,
        metadata: MDMetadata,
        initial_geometry: Geometry,
        name: str = "plamsjob",
    ) -> AMSMDJob:
        """
        create a AMS MD Job.
        :param metadata: options and settings for MD, overwrites the settings
                         in ams_md_settings
        :param initial_geometry: initial box geometry
        :param name: optional name
        """

        # if the method specified in metadata is GFN_xTB, create a job with
        # GFN_xTB settings
        job: AMSMDJob = AMSMDJob(
            program=self.program,
            metadata=metadata,
            initial_geometry=initial_geometry,
            ams_md_settings=self.ams_md_settings,
            forcefield=self.forcefield,
            reaxff_path=self.reaxff_path,
            name=name,
            **self.kwargs,
        )

        # if the method specified in metadata is ReaxFF, create a job with
        # ReaxFF settings

        return job
