"""
This module contains classes to perform calculations with Orca.
"""

import dataclasses
import os
from abc import ABC
from dataclasses import dataclass
from datetime import timedelta
from enum import Enum
from io import TextIOBase
from pathlib import Path
from collections.abc import Iterable
from typing import Generic, TypeVar, TypedDict

import numpy as np

from chemtrayzer.engine import Result
from chemtrayzer.core.coords import ChainOfStates, Geometry
from chemtrayzer.core.lot import (
    DLPNO_CCSD_T,
    RI_CORRESPONDING_BS,
    RI_GENERATE_BS,
    CoupledCluster,
    Dft,
    LevelOfTheory,
    QMSoftware,
)
from chemtrayzer.core.lot import QCMethod as QCM
from chemtrayzer.engine.jobsystem import (
    Job,
    JobTemplate,
    Memory,
    Program,
    Version,
)
import chemtrayzer.core.qm as qm
import contextlib


class Orca(Program):
    """
    Utility functions and settings for ORCA computational chemistry program.

    The auxiliary basis for the density fitting (resolution of identity)
    approximation in the level of theory object is ignored and the ORCA default
    is used instead.

    :param conv_thres:convergence threshold for SCF iterations and geometry
                      optimizations. If None, the ORCA default behavior is used
                       for most levels of theory. For DLPNO-CCSD(T) TIGHTSCF is
                       chosen as default.
    :param maxcore_pct:ORCA's SCF module cannot control exactly how much memory
                       is allocated, so the manual advised to set MaxCore to
                       significantly less than the physical memory (or in our
                       case the memory allocated for the job). The ORCA website
                       advises 75%
    """

    class ConvergenceThreshold(Enum):
        """controls how tightly SCF and geometry optimizations will be
        converged"""

        LOOSESCF = "LOOSESCF"
        SLOPPYSCF = "SLOPPYSCF"
        NORMALSCF = "NORMALSCF"
        STRONGSCF = "STRONGSCF"
        TIGHTSCF = "TIGHTSCF"
        VERYTIGHTSCF = "VERYTIGHTSCF"

    def __init__(
        self,
        executable: str,
        version: Version = None,
        conv_thresh: ConvergenceThreshold = None,
        maxcore_pct: float = 0.75,
    ) -> None:
        super().__init__(executable, version)
        self.conv_thresh = conv_thresh
        self.maxcore_pct = maxcore_pct

    def gen_keyword_lines(self, lot: LevelOfTheory) -> str:
        """
        generates "simple input" keyword lines (i.e. the one starting with !)
        based on the level of theory.

        :param lot: level of theory with method and basis set to use
        :raises: NotImplementedError if the level of theory has not been
                 implemented in this Python code
        """
        additional_keywords = ""

        if lot.method in self._METHOD_NAMES:
            method_str = self._METHOD_NAMES[lot.method]
        else:
            raise NotImplementedError(
                f"Method {repr(lot.method)} has not been"
                " added to this Python code."
            )

        if lot.el_struc.basis_set.name in self._BASIS_SETS:
            basis_set_str = self._BASIS_SETS[lot.el_struc.basis_set.name]
        else:
            raise NotImplementedError(
                "Requested basis set has not been"
                " added to this Python code."
            )

        # auxiliary basis sets:
        if isinstance(lot.method, Dft):
            aux_basis_j = lot.method.density_fit_J

            if aux_basis_j is not None:
                method_str += " SPLIT-RI-J"

                if aux_basis_j == RI_CORRESPONDING_BS:
                    if lot.el_struc.basis_set.name.startswith("def2"):
                        basis_set_str += " Def2/J"
                elif aux_basis_j == RI_GENERATE_BS:
                    basis_set_str += " AutoAux"
                elif aux_basis_j.name in self._BASIS_SETS:
                    basis_set_str += " " + self._BASIS_SETS[aux_basis_j.name]
                else:
                    raise ValueError(
                        f"Auxiliary basis set {lot.method.density_fit_J.name} "
                        "not supported or has not been implemented here."
                    )

        elif isinstance(lot.method, DLPNO_CCSD_T):
            if self.conv_thresh is None:
                self.conv_thresh = Orca.ConvergenceThreshold.TIGHTSCF

            if lot.method.aux_basis == RI_CORRESPONDING_BS:
                # simply try to add /C behind the basis set name (this ony
                # works for some predefined basis sets in ORCA, but it should
                # cover the most common cases
                basis_set_str += (
                    " " + self._BASIS_SETS[lot.el_struc.basis_set.name] + "/C"
                )
            elif lot.el_struc.basis_set == RI_GENERATE_BS:
                basis_set_str += " AutoAux"

            else:
                raise NotImplementedError(
                    "Auxiliary basis set "
                    f"{lot.method.aux_basis.name} has not"
                    " been added to this Python code."
                )

        if self.conv_thresh is not None:
            additional_keywords += " " + self.conv_thresh.value

        return "! " + method_str + " " + basis_set_str + additional_keywords


    # keywords for method or functional (incl. dispersion correction)
    _METHOD_NAMES = {
        QCM.GFN_xTB: "XTB1",
        QCM.GFN2_xTB: "XTB2",
        QCM.HF: "HF",
        QCM.B3LYP_G_D3: "B3LYP/G D3ZERO",
        QCM.B3LYP_TM_D3: "B3LYP D3ZERO",
        QCM.B3LYP_G_D3BJ: "B3LYP/G D3BJ",
        QCM.B3LYP_TM_D3BJ: "B3LYP D3BJ",
        QCM.B3LYP_G_D4: "B3LYP/G D4",
        QCM.B3LYP_TM_D4: "B3LYP D4",
        QCM.B97M_V: "B97M-V",
        QCM.B97M_D3BJ: "B97M-D3BJ",
        QCM.TPSS_D3: "TPSS D3ZERO",
        QCM.TPSS_D3BJ: "TPSS D3BJ",
        QCM.TPSS_D4: "TPSS D4",
        QCM.wB97M_V: "wB97M-V",
        QCM.wB97M_D4: "wB97M-D4",
        QCM.wB97X_V: "wB97X-V",
        QCM.wB97X_D4: "wB97X-D4",
        QCM.DLPNO_CCSD_T: "DLPNO-CCSD(T)",
    }

    # translates names from moldata.basissets.basis_sets to ORCA keywords
    _BASIS_SETS = {
        # standard basis sets
        "6-31G*": "6-31G*",
        "6-31++G": "6-31++G",
        "6-31++G*": "6-31++G(d)",
        "6-31++G**": "6-31++G(d,p)",
        "6-311G": "6-311G",
        "6-311+G": "6-31+1G",
        "6-311++G": "6-311++G",
        "6-311+G*": "6-311+G*",
        "6-311+G**": "6-311+G**",
        "6-31+G": "6-31+G",
        "def2-SV(P)": "def2-SV(P)",
        "def2-SVP": "def2-SVP",
        "def2-TZVP": "def2-TZVP",
        "def2-TZVPP": "def2-TZVPP",
        "def2-QZVP": "def2-QZVP",
        "def2-QZVPP": "def2-QZVPP",
        "cc-pVTZ": "cc-pVTZ",
        "cc-pVQZ": "cc-pVQZ",
        # resolution of identity (density fitting) basis sets
        "def2-universal-JFIT": "Def2/J",
        "def2-universal-JKFIT": "Def2/JK",
    }

class OrcaParsingError(Exception):
    """raised when an error occurred while parsing an ORCA related file"""

    def __init__(self, path, *args: object) -> None:
        if len(args) > 0:
            msg = f"Error parsing file {str(path)}:\n" + args[0]
        else:
            msg = f"Error parsing file {str(path)}."

        new_args = (msg, *args[1:]) if len(args) > 1 else (msg,)

        super().__init__(*new_args)

class OrcaOutParser:
    """Parser for ORCA output"""

    # values that cclib uses to convert from Hartree to eV
    _CCLIB_EV_IN_HARTREE = 27.21138505

    @dataclass
    class Result:
        """container to store parsed data"""

        spe_energies: np.ndarray = None
        """single point energies in Hartree in the order that they were read;
        contains only a single element for a single point energy calculation,
        but may contain more for optimizations and scans"""
        t1_diagnostic: np.ndarray = None
        """For CC calculations, this will contain the values of the T1
        diagnostic in the order that they were read. Contains only a single
        element for a single point energy calculation"""
        opt_run_done: bool = False
        """for geometry optimizations, this has to be true or the number of
        iterations was not sufficient to converge the geometry optimization"""
        terminated_normally: bool = False
        """if this is false, the calculation was not terminated normally"""
        timings: dict = None
        """dictionary containing the timings for the individual modules in
        seconds"""

    def __init__(self, out_file: str | os.PathLike) -> None:
        self.out_file = out_file

    def parse(self) -> Result:
        """parses the output file and returns its contents as result object"""
        spe_energies = []
        t1_diag = []
        timings = {}
        terminated_normally = False
        opt_run_done = False
        try:
            with open(self.out_file, encoding="utf-8") as fp:
                for line in fp:
                    if line[:25] == "FINAL SINGLE POINT ENERGY":
                        spe_energies.append(float(line[27:]))

                    elif line[:13] == "T1 diagnostic":
                        t1_diag.append(float(line[46:]))

                    elif line[32:61] == "*** OPTIMIZATION RUN DONE ***":
                        opt_run_done = True

                    elif line[0:31] == "Timings for individual modules:":
                        next(fp)
                        while True:
                            timing_line = next(fp)
                            if "..." not in timing_line:
                                if (
                                    timing_line[29:61]
                                    == "****ORCA TERMINATED NORMALLY****"
                                ):
                                    terminated_normally = True
                                break
                            name, timing_str = timing_line.split("...")
                            timing_sec = float(timing_str.split()[0].strip())
                            timings[name.strip()] = timing_sec

                    elif line[29:61] == "****ORCA TERMINATED NORMALLY****":
                        terminated_normally = True

                if terminated_normally is False:
                    raise OrcaParsingError(
                        self.out_file, "ORCA did not terminate normally."
                    )

        except FileNotFoundError:
            raise OrcaParsingError(self.out_file, "File not found.")
        except Exception as err:
            raise OrcaParsingError(self.out_file) from err

        result = OrcaOutParser.Result()
        result.spe_energies = np.array(spe_energies) if spe_energies else None
        result.t1_diagnostic = np.array(t1_diag) if t1_diag else None
        result.opt_run_done = opt_run_done
        result.terminated_normally = terminated_normally
        result.timings = timings

        return result

    def _skip_lines(self, fp: TextIOBase, n: int) -> str:
        """skip n lines.

        :param fp: file pointer in which to skip
        :param n: number of lines to skip. For n=1 this is basically
                  fp.readline()
        :return: content of current line + n. Empty string, if fp is at EOF
        """
        try:
            for i in range(n):
                line = next(fp)
        except StopIteration:
            line = ""

        return line

class OrcaHessParser:
    """Parser for orca.hess files"""

    class Result(TypedDict):
        hessian: np.ndarray
        vibrational_frequencies: np.ndarray

    def __init__(self, path: Path|str|bytes):
        self.path = Path(path)

    def parse(self) -> Result:
        hessian = freqs = None

        with open(self.path, 'r', encoding='utf-8') as fp:
            for line in fp:
                match line.strip(' \n'):
                    case '$hessian':
                        hessian=self._get_hessian(fp)
                    case'$vibrational_frequencies':
                        freqs=self._get_freqs(fp)

        if hessian is None or freqs is None:
            raise OrcaParsingError(
                self.path, "Could not read hessian or frequencies."
            )

        return self.Result(
                        hessian=hessian,
                        vibrational_frequencies=freqs)


    def _get_hessian(self, fp: TextIOBase) -> np.ndarray:
        """
        Obtains the hessian matrix from an orca calculation.
        :param input_file: orca.hess
        :return: hessian matrix in Hartree/Bohr^2
        """
        try:
            n = int(next(fp).strip())
            hess = np.zeros((n, n), dtype=float)

            # loop over blocks of n rows + 1 header line
            while True:
                indices = tuple(int(v) for v in next(fp).split())
                for i in range(n):
                    str_line = next(fp).split()
                    assert str_line[0] == str(i) # first element is the atom nr

                    hess[i, indices] = str_line[1:]  # numpy converts to float

                if indices[-1] == n - 1:
                    break

            return hess
        except StopIteration:
            raise OrcaParsingError(self.path, "File ended unexpectedly.")
        except Exception as err:
            raise OrcaParsingError(
                self.path, "Error parsing hessian."
            ) from err


    def _get_freqs(self, fp: TextIOBase) -> np.ndarray:
        """
        Obtains the frequencies from an orca calculation.
        :param input_file: orca.hess
        :return: frequencies in 1/cm
        """
        try:
            n = int(next(fp).strip())
            freqs = np.zeros(n, dtype=float)

            for i in range(n):
                _i, val = next(fp).split()
                assert _i == str(i)
                freqs[i] = float(val)

            return freqs
        except Exception as err:
            raise OrcaParsingError(
                self.path, "Error parsing frequencies."
            ) from err

S = TypeVar('S', bound=Result)
class OrcaJob(Job[S], ABC, Generic[S]):
    """base class for all ORCA jobs"""

    _CMD_TMPL = "${executable} orca.inp > results.out"

    def __init__(
        self, geometry: Geometry, *,
        program: Orca,
        lot: LevelOfTheory,
        memory: Memory,
        runtime: timedelta,
        n_tasks: int,
        **kwargs
    ) -> None:
        self.lot = dataclasses.replace(lot, software=QMSoftware.ORCA)
        self.program = program

        self.memory_mb = int(
            program.maxcore_pct
            * memory.amount_in_unit(Memory.UNIT_MB)
        )

        super().__init__(n_cpus=1, n_tasks=n_tasks, memory=memory,
                         runtime=runtime, **kwargs)


@dataclass
class OrcaEnergyResult(qm.EnergyResult, Result):
    """container to store parsed data"""

    t1_diagnostic: float|None = None
    """T1 diagnostic for coupled cluster calculations, or None"""

class OrcaEnergyJob(OrcaJob[OrcaEnergyResult]):
    """
    :param geometry: molecular coordinates for which the SPE should be computed
    :param program: instance of Orca class with executable path
    :param lot: level of theory for computation of SPE
    :param n_tasks: number of CPUs to use
    :param memory: amount of memory to use
    :param runtime: maximum runtime
    :param ressources: ressource specification, if n_cpus, memory and runtime
                       are not given
    :ivar result: dictionary containing
                  'energy' - electronic energy in Hartree
                  't1_diagnostic' - value of T1 diagnostic for coupled cluster
                  calculations, or None
    """

    _INPUT_TMPLS = {
        "orca.inp": """\
# orca input file generated from chemtrayzer
${keyword_lines}
%maxcore ${memory_mb}
%pal nprocs ${n_tasks}
     end
* xyzfile ${charge} ${multiplicity} geo.xyz
"""
    }


    def __init__(
        self, geometry: Geometry, program: Orca, lot: LevelOfTheory, **kwargs
    ) -> None:
        super().__init__(geometry=geometry, program=program, lot=lot, **kwargs)
        self.geometry = geometry
        self.charge = lot.el_struc.charge
        self.multiplicity = lot.el_struc.multiplicity
        self.executable = program.executable
        self.program = program
        self.keyword_lines = program.gen_keyword_lines(lot)

        self._template = JobTemplate(self, self._CMD_TMPL, self._INPUT_TMPLS)

    def gen_input(self, path):
        self.geometry.to_xyz(os.path.join(path, "geo.xyz"))
        self._template.gen_input(path)  # for orca.inp

    @property
    def command(self):
        return self._template.command

    def parse_result(self, path):
        try:
            file = Path(path) / "results.out"
            parser = OrcaOutParser(file)
            result = parser.parse()

            if result.spe_energies is None:
                raise OrcaParsingError(file, "Could not read energy.")

            self.result = OrcaEnergyResult(
                energy=result.spe_energies[-1],
                t1_diagnostic=(
                    result.t1_diagnostic[-1]
                    if isinstance(self.lot.method, CoupledCluster)
                    else None
                ),
            )

            self.succeed()
        except OrcaParsingError as err:
            self.fail(reason=err)


class OrcaInitialWavefunctionEnergyJob(OrcaEnergyJob):
    """
    Similar to an OrcaEnergyJob but first an initial wavefunction is generated
    with the lot_preopt level of theory.
    Afterwards the energy is calculated with the lot level of theory starting
    from the initial wavefunction.

    :param lot_preopt: LevelOfTheory
    :param lot: LevelOfTheory
    :param n_tasks: number of CPUs to use
    :param memory: amount of memory to use
    :param runtime: maximum runtime
    :param ressources: ressource specification, if n_cpus, memory and runtime
                       are not given
    """

    _CMD_TMPL = (
        "${executable} orca_preopt.inp > results_orbital_preopt.out\n"
        "${executable} orca.inp > results.out"
    )

    _INPUT_TMPLS = {
        "orca_preopt.inp": """\
# orca input file generated from chemtrayzer
${keyword_lines_preopt}
%maxcore ${memory_mb}
%pal nprocs ${n_tasks}
end
* xyzfile ${charge} ${multiplicity} geo.xyz
""",
        "orca.inp": """# orca input file generated from chemtrayzer
${keyword_lines} MORead NoIter
%moinp "orca_preopt.gbw"
%maxcore ${memory_mb}
%pal nprocs ${n_tasks}
end
* xyzfile ${charge} ${multiplicity} geo.xyz
""",
    }

    def __init__(
        self,
        program: Orca,
        lot_preopt: LevelOfTheory,
        lot: LevelOfTheory,
        **kwargs,
    ) -> None:
        super().__init__(program=program, lot=lot, **kwargs)
        self.keyword_lines_preopt = program.gen_keyword_lines(lot_preopt)

@dataclass
class OrcaOptResult(qm.OptResult, Result):
    """container to store parsed data"""

class OrcaOptJob(OrcaJob[OrcaOptResult]):
    """
    Orca Opt Job class for optimization of minima and transition states.
    :param geometry: starting molecular coordinates for geometry optimization
    :type geometry: Geometry
    :param ts: if True, the geometry is optimized towards a transition state,
               default False
    :type ts: bool
    :param freeze: list of atom indices to be frozen during optimization,
                   default None
    :type freeze: Iterable[int]
    :param lot: level of theory for computation
    :type lot: LevelOfTheory
    :param charge: charge
    :type charge: int
    :param multiplicity: multiplicity
    :type multiplicity: int
    :param program: instance of Orca class with executable path
    :type program: Orca
    :param lot: level of theory for computation of SPE
    :type lot: LevelOfTheory
    :param n_tasks: number of CPUs to use
    :param memory: amount of memory to use
    :param runtime: maximum runtime
    :param ressources: ressource specification, if n_cpus, memory and runtime
                       are not given
    :ivar result: dictionary containing:
                    'energy' - electronic energy of TS in Hartree,
                    'geo' - geometry of the optimized structure

    """

    _INPUT_TMPLS = {
        "orca.inp": """\
# orca input file generated from chemtrayzer
%maxcore ${memory_mb}
%PAL NPROCS ${n_tasks} END
${keyword_lines} ${opt}${geom_section}
* xyzfile ${charge} ${multiplicity} geo.xyz
"""
    }

    def __init__(
        self,
        geometry: Geometry,
        program: Orca,
        lot: LevelOfTheory,
        ts: bool = False,
        charge: int = None,
        multiplicity: int = None,
        freeze: Iterable[int] = None,
        **kwargs,
    ) -> None:
        self.opt = "OPT" if ts is False else "OptTS"
        self.geometry = geometry
        super().__init__(
            geometry=self.geometry, program=program, lot=lot, **kwargs
        )
        self.charge = charge
        self.multiplicity = multiplicity
        self.geometry = geometry
        self.charge = lot.el_struc.charge
        self.multiplicity = lot.el_struc.multiplicity
        self.executable = program.executable
        self.program = program
        self.keyword_lines = program.gen_keyword_lines(lot)
        self.freeze = freeze

        constraints_str = (
            "Constraints"
            + "".join(f"\n{{C {i} C}}" for i in self.freeze)
            + "\nend\n"
            if freeze is not None
            else ""
        )
        calc_hess = "Calc_Hess true\n" if ts is True else ""
        self.geom_section = (
            f"\n%geom\n{calc_hess}{constraints_str}end"
            if calc_hess or constraints_str
            else ""
        )

        self._template = JobTemplate(self, self._CMD_TMPL, self._INPUT_TMPLS)

    def gen_input(self, path):
        self.geometry.to_xyz(os.path.join(path, "geo.xyz"))
        self._template.gen_input(path)  # for orca.inp

    @property
    def command(self):
        return self._template.command

    def parse_result(self, path):
        try:
            file = Path(path) / "results.out"
            geo_filepath = Path(path) / "orca.xyz"
            parser = OrcaOutParser(file)
            result = parser.parse()

            if result.spe_energies is None:
                raise OrcaParsingError(file, "Could not read energy.")

            if result.opt_run_done is False:
                raise OrcaParsingError(
                    file,
                    "Optimization did not converge. "
                    "Try increasing the number of iterations.",
                )

            # we cannot currently read all geometries -> only give last one
            self.result = OrcaOptResult(
                energies=[result.spe_energies[-1]],
                geometries=[Geometry.from_xyz_file(geo_filepath)],
            )

            self.succeed()
        except OrcaParsingError as err:
            self.fail(err)


class OrcaFreqResult(qm.FreqResult, Result):
    """container to store parsed data"""

class _OrcaFreqJobBase(OrcaJob[S], Generic[S]):
    """Base class for ORCA jobs that calculate vibrational frequencies"""

    _INPUT_TMPLS = {
        "orca.inp": """\
# orca input file generated from chemtrayzer
%maxcore ${memory_mb}
%PAL NPROCS ${n_tasks} END
${keyword_lines} ${job_type}
* xyzfile ${charge} ${multiplicity} geo.xyz
"""
    }

    def __init__(
        self,
        geometry: Geometry,
        program: Orca,
        lot: LevelOfTheory,
        charge: int = None,
        multiplicity: int = None,
        **kwargs,
    ) -> None:
        # no analytical hessians for GFN-xTB available in ORCA
        self.job_type = (
            "Numfreq" if lot in (QCM.GFN_xTB, QCM.GFN2_xTB) else "Freq"
        )
        self.geometry = geometry
        super().__init__(
            geometry=self.geometry, program=program, lot=lot, **kwargs
        )
        self.charge = charge
        self.multiplicity = multiplicity
        self.charge = lot.el_struc.charge
        self.multiplicity = lot.el_struc.multiplicity
        self.executable = program.executable
        self.program = program
        self.keyword_lines = program.gen_keyword_lines(lot)

        self._template = JobTemplate(self, self._CMD_TMPL, self._INPUT_TMPLS)

    def gen_input(self, path):
        self.geometry.to_xyz(os.path.join(path, "geo.xyz"))
        self._template.gen_input(path)  # for orca.inp

    @property
    def command(self):
        return self._template.command

    def _set_freq_result(self, path):
        """parse the output file, and calls succeed() or fail() accordingly
        """
        try:
            out_parser = OrcaOutParser(Path(path) / "results.out")
            hess_parser = OrcaHessParser(Path(path) / "orca.hess")
        except OrcaParsingError as err:
            self.fail(err)
            return None
        else:
            out = out_parser.parse()
            hess = hess_parser.parse()

            freqs = list(filter(lambda num: num != 0,         # remove zeros
                                hess["vibrational_frequencies"]))

            self.result = OrcaFreqResult( # type: ignore
                            frequencies=freqs,
                            hessian=hess["hessian"],
                        )
            if out.terminated_normally:
                self.succeed()
            else:
                self.fail("Orca terminated abnormally.")

class OrcaFreqJob(_OrcaFreqJobBase[OrcaFreqResult]):
    """ORCA job to calculate vibrational frequencies


    :param n_tasks: number of CPUs to use
    :param memory: amount of memory to use
    :param runtime: maximum runtime
    :param ressources: ressource specification, if n_cpus, memory and runtime
                       are not given
"""

    def parse_result(self, path):
        self._set_freq_result(path)

@dataclass
class OrcaIRCResult(OrcaFreqResult):
    """container to store parsed data"""

    irc_forward: ChainOfStates
    """IRC forward"""
    irc_backward: ChainOfStates
    """IRC backward"""

class OrcaIRCJob(OrcaFreqJob):
    """"intrinsic reaction coordinate calculation

    :param n_tasks: number of CPUs to use
    :param memory: amount of memory to use
    :param runtime: maximum runtime
    :param ressources: ressource specification, if n_cpus, memory and runtime
                       are not given
    """

    def __init__(
        self,
        geometry: Geometry,
        program: Orca,
        lot: LevelOfTheory,
        charge: int = None,
        multiplicity: int = None,
        **kwargs,
    ):
        super().__init__(
            geometry,
            program,
            lot,
            charge=charge,
            multiplicity=multiplicity,
            **kwargs,
        )
        self.job_type = self.job_type + " IRC"
        self._template = JobTemplate(self, self._CMD_TMPL, self._INPUT_TMPLS)

    def parse_result(self, path):
        self._set_freq_result(path)

        irc_filepath_forward = Path(path) / "orca_IRC_F_trj.xyz"
        irc_filepath_backward = Path(path) / "orca_IRC_B_trj.xyz"
        forward_irc = ChainOfStates.from_xyz_file(irc_filepath_forward)
        backward_irc = ChainOfStates.from_xyz_file(irc_filepath_backward)

        self.result = OrcaIRCResult(
            frequencies=self.result.frequencies,
            hessian=self.result.hessian,
            irc_forward=forward_irc,
            irc_backward=backward_irc,
        )
