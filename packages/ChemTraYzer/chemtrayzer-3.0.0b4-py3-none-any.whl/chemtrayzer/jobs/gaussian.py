"""
This module contains classes to perform calculations with Gaussian.
"""
# flake8: noqa
import dataclasses
import logging
import os
import pathlib
import re
import shutil
from abc import ABC
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import timedelta
from enum import Enum
from string import Template
from typing import Final, Generic, Protocol, TypeVar
from collections.abc import Sequence

import cclib
from chemtrayzer.core import qm
from chemtrayzer.engine import Result
import numpy as np

from chemtrayzer.core.coords import Geometry
from chemtrayzer.core.lot import (
    Dft,
    LevelOfTheory,
    QCMethod,
    QMSoftware,
    SemiEmpiricalMethod,
)
from chemtrayzer.engine.jobsystem import (
    Job,
    Memory,
    Program,
)


class IRCDirection(Enum):
    """direction of an IRC scan"""

    Forward = 0
    Reverse = 1


class Gaussian(Program):
    # lookup tables for Gaussian keywords
    _METHODS = {
        QCMethod.B3LYP_G_D3: "B3LYP",
        QCMethod.B3LYP_G_D3BJ: "B3LYP",
        QCMethod.HF: "HF",
        QCMethod.TPSS_D3: "TPSSTPSS",
        QCMethod.TPSS_D3BJ: "TPSSTPSS",
        QCMethod.PM6: "PM6",
    }
    _BASIS_SETS = {
        "6-21G": "6-21G",
        "6-31G*": "6-31G(d)",
        "6-31++G": "6-31++G",
        "6-31++G*": "6-31++G(d)",
        "6-31++G**": "6-31++G(d,p)",
        "6-311G": "6-311G",
        "6-311+G": "6-31+1G",
        "6-311++G": "6-311++G",
        "6-311+G*": "6-311+G*",
        "6-311+G**": "6-311+G**",
        "6-31+G": "6-31+G",
        "def2-SV": "Def2SV",
        "def2-SV(P)": "Def2SVPP",
        "def2-SVP": "Def2SVP",
        "def2-TZVP": "Def2TZVP",
        "def2-TZVPP": "Def2TZVPP",
        "def2-QZV": "Def2QZV",
        "def2-QZVP": "Def2QZVP",
        "def2-QZVPP": "Def2QZVPP",
        "def2-QZVPPD": "Def2QZVPPD",
        # density fitting basis sets
        "def2-universal-JFIT": "W06",
        "RI_CORRESPONDING_BS": "Fit",
        "RI_GENERATE_BS": "Auto",
    }
    _DISPERSION = {
        QCMethod.B3LYP_G_D3: "EmpiricalDispersion=GD3",
        QCMethod.B3LYP_G_D3BJ: "EmpiricalDispersion=GD3BJ",
        QCMethod.TPSS_D3: "EmpiricalDispersion=GD3",
        QCMethod.TPSS_D3BJ: "EmpiricalDispersion=GD3BJ",
        # When the disperion correction is already included in the functional,
        # no extra keyword needs to be added. However, this dictionary needs to
        # contain an entry to be able to throw an error if an unsupported (or
        # not yet implemented) disperion correction is requested.
        QCMethod.wB97X_D3: "",
    }

    def gen_instruction_str(self, lot: LevelOfTheory) -> str:
        """Generate Gaussian instructions for the route section of the input
        file for a given level of theory."""

        if lot.software is not None and lot.software != QMSoftware.GAUSSIAN:
            raise ValueError(
                "Level of theory requested from this GaussianJob "
                "specifies software that is not Gaussian "
            )

        if lot.method not in self._METHODS:
            raise ValueError(
                f"Method {lot.method} is not available or has not"
                " been implemented for Gaussian."
            )
        if (
            not isinstance(lot.method, SemiEmpiricalMethod)
            and lot.el_struc.basis_set.name not in self._BASIS_SETS
        ):
            raise ValueError(
                f"Basis set {lot.el_struc.basis_set} is not "
                "available or has not been implemented for Gaussian."
            )

        basis_set = (
            ""
            if isinstance(lot.method, SemiEmpiricalMethod)
            else "/" + self._BASIS_SETS.get(lot.el_struc.basis_set.name)
        )

        instruct = self._METHODS[lot.method] + basis_set

        if isinstance(lot.method, Dft):
            if lot.method.density_fit_J is not None:
                if lot.method.density_fit_J.name in self._BASIS_SETS:
                    instruct += (
                        "/" + self._BASIS_SETS[lot.method.density_fit_J.name]
                    )
                else:
                    raise ValueError(
                        f"Auxiliary basis set {lot.method.density_fit_J.name} "
                        "not supported or has not been implemented here."
                    )

            if lot.method in self._DISPERSION:
                instruct += " " + self._DISPERSION[lot.method]

            elif lot.method.dispersion_correction is not None:
                raise ValueError(
                    f"Dispersion correction {lot.method.dispersion_correction}"
                    " not supported or has not been implemented."
                )

        return instruct
class ParsingError(Exception):
    """Base class for exceptions raised by log file parsers"""


class GaussianLogParser:
    """Parser for Gaussian log files"""

    # values that cclib uses to convert from Hartree to eV
    _CCLIB_EV_IN_HARTREE = 27.21138505

    @dataclass
    class Result:
        """container to store parsed data"""

        scf_energies: np.ndarray = None
        """SCF energies of HF/DFT run in Hartree in the order that they were
        read;
        contains only a single element for a single point energy calculation"""
        geometries: list[Geometry] = None
        """molecular geometries in Angstroms in the order that they were
        read/computed"""
        freqs: np.ndarray = None
        """harmonic oscillator frequencies"""
        ir_intensities: np.ndarray = None
        """IR intensities belonging to the frequencies"""
        optimization_complete: bool = False
        """True if an optimization was successful"""
        failure_reason: list[str]|None = None
        """Reason(s) for a failure, if one occured"""
        rotational_symmetry_nr: int = None
        """rotational symmetry number"""

    def __init__(self, log_file: str | os.PathLike) -> None:
        self.log_file = log_file

    def parse(self) -> Result:
        """parses the log file and returns its contents as Python objects"""
        try:
            parser = cclib.parser.Gaussian(self.log_file)

            data = parser.parse()
        except FileNotFoundError as err:
            raise ParsingError(
                f'Logfile "{self.log_file}" not found.'
            ) from err
        except Exception as err:
            raise ParsingError(
                f"Error while parsing file {self.log_file}."
            ) from err

        result = GaussianLogParser.Result()

        result.geometries = self._get_geometries(data)
        result.scf_energies = self._get_electronic_energies_in_hartree(data)
        result.freqs = self._get_freqs(data)
        result.ir_intensities = self._get_ir(data)
        result.optimization_complete = self._get_optimization_status(data)
        result.rotational_symmetry_nr = self._get_rot_symm_nr()

        if not result.optimization_complete:
            result.failure_reason = self._figure_out_reason()

        return result

    def _figure_out_reason(self):
        reasons = []

        with open(self.log_file) as f:
            for line in f:
                line = line.strip()
                # The line after "Optimization stopped." contains an
                # explanation, e.g.
                # "     -- Wrong number of Negative eigenvalues: ..."
                if line == "Optimization stopped.":
                    reasons.append("Optimization stopped.")
                    line = next(f)
                    reasons.append(line.split("--")[1].strip())

                # add all lines starting with "Error termination"
                elif line.startswith("Error termination"):
                    reasons.append(line)

                elif line.startswith("The combination of multiplicity"):
                    if re.match(r'^The combination of multiplicity( )*[0-9]+ '
                                r'and( )*[0-9]+ electrons is impossible\.$',
                                line):
                        reasons.append(line)

        return reasons

    def _get_electronic_energies_in_hartree(self, cclib_data) -> float | None:
        try:
            energy = np.array(cclib_data.scfenergies)

            energy /= self._CCLIB_EV_IN_HARTREE

            return energy
        except AttributeError:
            return None

    def _get_geometries(self, cclib_data) -> Geometry | None:
        try:
            atoms = cclib_data.atomnos

            geos = [
                Geometry(atoms, coords) for coords in cclib_data.atomcoords
            ]

            return geos
        except AttributeError:
            return None

    def _get_optimization_status(self, cclib_data) -> bool:
        try:
            if cclib_data.optdone:
                return True
            return False
        except AttributeError:
            return False

    def _get_freqs(self, cclib_data):
        """
        Obtains the frequencies from an Gaussian calculation.
        :param input_file: results.log
        :return: frequencies in 1/cm
        """
        try:
            return np.array(cclib_data.vibfreqs)
        except AttributeError:
            return None

    def _get_ir(self, cclib_data):
        """Obtain IR intensities from cclib data"""
        try:
            return np.array(cclib_data.vibirs)
        except AttributeError:
            return None

    def _get_rot_symm_nr(self):
        symm_nr = None
        with open(self.log_file) as file:
            for line in file:
                line.strip()
                if line.startswith(" Rotational symmetry number"):
                    symm_nr = int(line[27:-2])
                    break

        return symm_nr


class GaussianFChkParser:
    """parser for Gaussian's formatted checkpoint files"""

    def __init__(self, fchk_file: str | os.PathLike) -> None:
        self.fchk_file = fchk_file

    @dataclass
    class Result:
        hessian: np.ndarray
        """Hessian matrix in atomic units"""
        gradient: np.ndarray
        """Cartesian gradient in atomic units"""

    def parse(self) -> Result:
        data = self._read_fields(
            ["Cartesian Gradient", "Cartesian Force Constants"]
        )

        return GaussianFChkParser.Result(
            hessian=self._create_full_hessian(
                data["Cartesian Force Constants"]
            ),
            gradient=np.array(data["Cartesian Gradient"]),
        )

    def _read_fields(self, fields: list[str]):
        """reads the requested fields from a gaussian formatted chk file
        :return: dictionary containing the field names as key and the data as
                 values"""
        DATA_TYPES = {"I": int, "R": float, "C": str, "L": bool}

        data = {}

        try:
            with open(self.fchk_file, "r") as f:
                # skip first two lines
                f.readline()
                f.readline()

                for line in f:
                    # skip empy lines (should only be at the end)
                    if line == "":
                        continue
                    # first 40 charachters contain field description
                    field = line[:40].strip()

                    skip = field not in fields

                    # then there are 3 spaces and a character denoting the type
                    try:
                        data_t = DATA_TYPES[line[43]]
                    except KeyError:
                        raise ParsingError(
                            Template(
                                "Unexpected data type in " "line:\n${line}"
                            ).substitute(line=line)
                        )

                    # for vector types, the next five characters are "   N="
                    if line[47:49] == "N=":
                        # counts down how many elements have been read
                        n = int(line[49:61])

                        # read N values from subsequent lines
                        if data_t is str:
                            if not skip:
                                data[field] = ""
                            while n > 0:
                                line = f.readline()
                                if not skip:
                                    data[field] += line
                                   # strings are written in batches of 12 chars
                                n -= len(line) / 12
                        else:
                            if not skip:
                                data[field] = []
                            while n > 0:
                                line = f.readline()
                                line_data = [
                                    data_t(word) for word in line.split()
                                ]

                                if not skip:
                                    data[field].extend(line_data)
                                n -= len(line_data)

                    # for scalar types, the next five characters are spaces
                    elif line[47:49] == "  ":
                        if not skip:
                            data[field] = data_t(line[49:])
                    else:
                        raise ParsingError("Unexpected fchk format")

            for field in fields:
                if field not in data:
                    raise ParsingError(
                        f'Requested field "{field}" not found in' " fchk file"
                    )

            return data
        except ParsingError as err:
            # add path to parsing error
            raise ParsingError(
                f"Error reading file {self.fchk_file}: {str(err)}"
            )
        except Exception as err:
            raise ParsingError(f"Error reading file {self.fchk_file}") from err

    def _create_full_hessian(self, compact_hessian) -> np.ndarray:
        hess_size = int(np.sqrt(2 * len(compact_hessian) + 0.25) - 0.5)

        if hess_size == 0:
            raise ParsingError("Error reading hessian")

        full_hessian = np.zeros((hess_size, hess_size))
        m = 0
        for i in range(hess_size):
            for j in range(i + 1):
                full_hessian[i, j] = compact_hessian[m]
                full_hessian[j, i] = compact_hessian[m]
                m += 1
        return np.array(full_hessian)

@dataclass
class GaussianOptions:
    """special data structure for providing keywords to Gaussian.

    Needed to ensure, that the keywords are put at the correct position in the
    input file.

    .. note:: Be very careful with this and check the generated output files!
    """

    opt_options: list[str] = field(default_factory=list)
    """Options for Gaussian's OPT keyword. "TS", "ModRedundant", and "nofreeze"
    may be added automatically depeding on the type of job."""
    irc_options: list[str] = field(default_factory=list)
    """options for the IRC keyword. "forward", "reverse", "stepsize",
    "maxpoints", "rcfc", "restart", ... are set automatically and should not
    be specified."""
    additional_keywords: str = ""
    """appended to the end of the route section"""

S = TypeVar('S', bound=Result)
class GaussianJob(Job[S], ABC, Generic[S]):
    """base class for all Gaussian jobs

    :param n_cpus: number of CPUs to use
    :param memory: amount of memory to use
    :param runtime: maximum runtime
    """

    def __init__(
        self,
        *,
        geometry: Geometry,
        program: Gaussian,
        lot: LevelOfTheory,
        memory: Memory,
        runtime: timedelta,
        n_cpus: int,
        **kwargs,
    ) -> None:
        # very conservative check to avoid that result['energy'], which is
        # currently always the SCF energy, is interpreted
        # as the total electronic energy (e.g. including CC correction)
        # TODO improve parser and parse_result() to deal with different levels
        # of theory and return the expected energy
        if not isinstance(lot.method, (Dft, SemiEmpiricalMethod)):
            raise NotImplementedError(
                "The Gaussian parser object does "
                "currently not support reading MP2 or CC"
                " energies, i.e., job results could not "
                "be read. So no job will be submitted."
            )
        # the lot has to be set to Gaussian to avoid wrong labels in the DB
        lot = dataclasses.replace(lot, software=QMSoftware.GAUSSIAN)

        self.lot = lot

        super().__init__(n_tasks=1, n_cpus=n_cpus, memory=memory,
                         runtime=runtime, **kwargs)


class GaussianJobError(Exception):
    """Base class for exceptions raised by GaussianJob objects"""

    def __init__(self, job: GaussianJob, msg: str, *args: object) -> None:
        # prepend job id for better debugging
        if job.id is not None:
            msg = f"Job {job.id}:" + msg

        super().__init__(msg, *args)

class _GaussianJobP(Protocol):
    """Protocol for GaussianJob objects that are used to generate input files
    """

    CHK_FILE: Final[str]
    geometry: Geometry
    lot: LevelOfTheory
    program: Gaussian
    n_cpus: int
    memory: Memory
    keywords: dict[str, list[str]]

class _GaussianInputGenerator:
    """Generates Gaussian input files"""

    _GJF_TMPL = Template(
        "%chk=${chk_file}\n"
        "%mem=${memory}B\n"
        "%nprocshared=${n_cpus}\n"
        "#P ${model_chemistry}${keywords} formcheck\n"
        "\n"
        "Gaussian input file generated from chemtrayzer\n"
        "\n"
        "${charge} ${multiplicity}\n"
        "${input_geometry}\n"
        "${additional_sections}\n"
        )

    def gen_gjf_str(self, job: _GaussianJobP,
                 additional_sections: str = "",
                 input_geometry: bool = True) -> str:
        return self._GJF_TMPL.substitute(
            {
                "chk_file": job.CHK_FILE,
                "memory": job.memory,
                "n_cpus": job.n_cpus,
                "model_chemistry": job.program.gen_instruction_str(job.lot),
                "keywords": self._keyword_str(job),
                "charge": job.lot.el_struc.charge,
                "multiplicity": job.lot.el_struc.multiplicity,
                "input_geometry": self._input_geometry_str(job.geometry)
                                  if input_geometry
                                  else "",
                "additional_sections": additional_sections,
            }
        )

    def write_gjf(self, job: _GaussianJobP, path: str,
                  additional_sections: str = "",
                  input_geometry: bool = True) -> None:
        """write the input file to the specified path"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.gen_gjf_str(job, additional_sections, input_geometry))

    def _keyword_str(self, job: _GaussianJobP) -> str:
        kw_str = ''

        for kw, vals in job.keywords.items():
            if vals:
                if kw == "IOp":
                    kw_str += f" {kw}({','.join(vals)})"
                else:
                    kw_str += f" {kw}=({','.join(vals)})"
            else:
                kw_str += f" {kw}"

        return kw_str

    def _input_geometry_str(self, geo: Geometry):
        """
        creates geometry string needed for Gaussian input file
        :return: str
        """
        geo_str = ""

        for type, coords in zip(geo.atom_types, geo.coords):
            geo_str += (
                f"{type:s} {coords[0]:.8f} {coords[1]:.8f}"
                f" {coords[2]:.8f}\n"
            )

        return geo_str


@dataclass
class GaussianEnergyResult(Result, qm.EnergyResult):
    """container to store parsed data"""

class GaussianEnergyJob(GaussianJob[GaussianEnergyResult]):
    r"""
    A parser to Gaussian that is used for energy calculations.
    Gaussian documentation:
    https://gaussian.com/man/

    :param geometry: geometry for energy calculations
    :param lot: level of theory at which to compute the single point energy
    :ivar result: energy calculation
    :param n_cpus: number of CPUs to use
    :param memory: amount of memory to use
    :param runtime: maximum runtime
    """

    CHK_FILE = "geo"

    def __init__(
        self,
        geometry: Geometry,
        lot: LevelOfTheory,
        *,
        program: Gaussian,
        n_cpus: int,
        memory: Memory,
        runtime: timedelta,
        additional_keywords: str = "",
        **kwargs,
    ) -> None:
        super().__init__(
            geometry=geometry, program=program, lot=lot,
            n_cpus=n_cpus, memory=memory, runtime=runtime,
            **kwargs
        )
        self.geometry = geometry
        self.program = program
        self.keywords = {}
        if additional_keywords != "":
             # if value is an empty list, the whole string will simply be added
             self.keywords[additional_keywords] = []

    def gen_input(self, path):
        _GaussianInputGenerator().write_gjf(self, path/'geo.gjf')

    @property
    def command(self):
        return f"{self.program.executable} < geo.gjf > results.log"

    def parse_result(self, path):
        try:
            parser = GaussianLogParser(os.path.join(path, "results.log"))
            data = parser.parse()

            if data.scf_energies is None:
                self.fail("Energy could not be read from log.")
            else:
                self.result = GaussianEnergyResult(
                                    energy=data.scf_energies[-1])
                self.succeed()

        except ParsingError as e:
            self.fail(e)


@dataclass
class GaussianFreqResult(Result, qm.FreqResult):
    """Result class for Frequency calculations with Gaussian"""


class GaussianFreqJob(GaussianJob[GaussianFreqResult], qm.FreqSubmittable):
    """
    """
    CHK_FILE = "geo"

    def __init__(self, /, geometry:Geometry, lot:LevelOfTheory, program:Gaussian, additional_keywords = "", *args, **kwargs):
        super().__init__(
            geometry=geometry, lot=lot, program=program, *args, **kwargs)
        self.geometry = geometry
        self.program = program
        self.keywords = {}
        if additional_keywords != "":
             # if value is an empty list, the whole string will simply be added
             self.keywords[additional_keywords] = []
        if not "freq" in self.keywords:
            self.keywords["freq"] = []

    def gen_input(self, path):
        _GaussianInputGenerator().write_gjf(self, path/'geo.gjf')

    @property
    def command(self):
        return f"${self.program.executable} < geo.gjf > results.log"

    def parse_result(self, path):
        try:

            parser = GaussianLogParser(os.path.join(path, "results.log"))
            log_data = parser.parse()

            result_dict = {
                "energies": log_data.scf_energies,
                "geometries": log_data.geometries,
            }

            if (result_dict["energies"] is None
                or result_dict["geometries"] is None):
                raise ParsingError(f"Error while parsing log file.")

            if log_data.scf_energies is None:
                self.fail("Energy could not be read from log.")
            else:
                energy = log_data.scf_energies[-1]
            if log_data.freqs is None:
                self.fail("Frequencies could not be read from log")
            else:
                frequencies = log_data.freqs

            #formatted checkpoint file always has the name Test.FChkF
            fchk_parser = GaussianFChkParser(os.path.join(path, "Test.FChk"))
            fchk_data = fchk_parser.parse()

            hessian = fchk_data.hessian

            if fchk_data.gradient is not None:
                gradient = fchk_data.gradient

            self.result = GaussianFreqResult(energy=energy,
                                             frequencies=frequencies,
                                             hessian=hessian,
                                             gradient=gradient)

            if self.is_failed is False:
                self.succeed()
        except ParsingError as e:
            self.fail(e)


class _GaussianOptJobBase(GaussianJob[S], Generic[S]):
    r"""Base class for Gaussian jobs that perform geometry optimizations

    :param geometry: initial geometry for the optimization
    :param lot: level of theory for the computation
    :param program: Gaussian object containg the path to the executable
    :param freeze: list of atoms that should be frozen during optimization
                   (using zero-based index)
    :param compute_frequencies: boolean indicating whether frequencies should
                                be computed
    :param add_opt_options: options for Gaussian's "opt" keyword (in addition
                            to "ts"). "nofreeze" is automatically added if
                            freeze is None
    :param maxiter: maximal number of iterations
    :param \*\*kwargs: standard arguments to configure a Job (e.g. n_cpus)
    """

    CHK_FILE = "opt.chk"
    """path to the check point file relative to the job's directory"""

    def __init__(
        self,
        geometry: Geometry,
        lot: LevelOfTheory,
        *,
        freeze: Iterable[int]|None = None,
        compute_frequencies=True,
        transition_state: bool = False,
        add_opt_options: Sequence[str] = ("tight","calcfc"),
        additional_keywords: str = "",
        program: Gaussian,
        maxiter = None,
        **kwargs,
    ) -> None:
        super().__init__(
            geometry=geometry, program=program, lot=lot, **kwargs
        )
        self._check_lot(lot)

        self.geometry = geometry
        self.compute_frequencies = compute_frequencies
        self.transition_state = transition_state
        self.program = program
        self.freeze = freeze
        self.maxiter = maxiter

        self.keywords = {
            "opt": [opt.lower() for opt in add_opt_options],
        }

        if additional_keywords != "":
            self.keywords[additional_keywords] = []

        if compute_frequencies:
            self.keywords["freq"] = []

        if maxiter is not None:
            self.keywords['opt'].append(f"maxcycle={maxiter}")
            self.keywords['IOp'] = [f"1/152={maxiter}"]

        if transition_state:
            # the noeigen keyword tells Gaussian not to check the number of
            # negative eigenstates during the optimization
            self.keywords['opt'].append("ts")

            if not any("calcfc" in opt or "calcall" in opt
                   for opt in self.keywords['opt']):
                # TS needs force constants
                self.keywords['opt'].append("calcfc")
        if freeze is None:
            self.keywords['opt'].append("nofreeze")
        else:
            self.keywords['opt'].append("ModRedundant")

    def _check_lot(self, lot: LevelOfTheory):
        """check if the level of theory is supported"""
        if not isinstance(lot.method, (Dft, SemiEmpiricalMethod)):
            raise NotImplementedError(
                "The Gaussian parser object does "
                "currently not support reading MP2 or CC"
                " energies, i.e., job results could not "
                "be read. So no job will be submitted."
            )

    def _gen_frozen_atom_str(self, freeze: Iterable[int]):
        """freeze: list of zero-based atom indeces to freeze"""
        if freeze is None:
            return "\n"
        else:
            # Gaussian uses one-based indeces -> +1
            frozen_strs = [f"{atom_id+1} F\n" for atom_id in freeze]
            return "".join(frozen_strs) + "\n"

    def gen_input(self, path):
        frozen_atoms_str = self._gen_frozen_atom_str(self.freeze)
        _GaussianInputGenerator().write_gjf(
                        self,
                        path/'opt.gjf',
                        additional_sections=frozen_atoms_str)

    @property
    def command(self):
        return f"{self.program.executable} < opt.gjf > results.log"

    def parse_result(self, path):
        # extract data from log file
        try:
            log_parser = GaussianLogParser(os.path.join(path, "results.log"))
            log_data = log_parser.parse()
        except ParsingError as err:
            self.fail(err)
            return

        result_dict = {
            "energies": log_data.scf_energies,
            "geometries": log_data.geometries,
        }

        if not log_data.optimization_complete:
            # if we have None values, the GaussianOptResult object won't work
            if not any(v is None for v in result_dict.values()):
                # store geometries up to failed iteration
                self.result = GaussianOptResult(**result_dict)

            reasons = log_data.failure_reason
            if ("Optimization stopped." in reasons
                    and any(line.startswith("Number of steps exceeded,")
                            for line in reasons)):
                self.fail(qm.MaxIterationsReached(
                                        "\n".join(log_data.failure_reason)))
            elif any(line.startswith("The combination of multiplicity")
                     for line in reasons):
                self.fail(qm.ImpossibleMultiplicityFailure(
                                        "\n".join(log_data.failure_reason)))
            else:
                self.fail("\n".join(log_data.failure_reason))

        else:
            # optimization was read as complete, but the result is incomplete
            if  any(v is None for v in result_dict.values()):
                self.fail('Optimization complete, but results could not be '
                          'read')
                return

            if self.compute_frequencies:
                try:
                    fchk_parser = GaussianFChkParser(
                        os.path.join(path, "Test.FChk")
                    )
                    fchk_data = fchk_parser.parse()

                    if fchk_data.hessian is None or log_data.freqs is None:
                        self.fail(
                            "Could not read frequencies from "
                            f"fchk file {path}"
                        )
                        return

                except ParsingError as e:
                    self.fail(e)
                    return

                result_dict['final'] = qm.FreqResult(
                    frequencies = log_data.freqs,
                    ir_intensities =log_data.ir_intensities,
                    hessian = fchk_data.hessian,
                    gradient = fchk_data.gradient,
                    rotational_symmetry_nr = log_data.rotational_symmetry_nr,
                )

                if self.transition_state:
                    n_imag_freqs = np.count_nonzero(log_data.freqs < 0.0)

                    if n_imag_freqs != 1:
                        self.result = GaussianOptResult(**result_dict)
                        self.fail(
                            "Unexpected number of imaginary "
                            "frequencies. Expected: 1, Actual: "
                            f"{n_imag_freqs:d}."
                        )
                        return

            self.result = GaussianOptResult(**result_dict)
            self.succeed()

class GaussianOptResult(qm.OptResult, Result): ...

class GaussianOptJob(_GaussianOptJobBase[GaussianOptResult]):
    """Job to optimize the geometry of a molecule with Gaussian

    :param geometry: initial geometry for the optimization
    :param lot: level of theory for the computation
    :param program: Gaussian object containg the path to the executable
    :param freeze: list of atoms that should be frozen during optimization
                   (using zero-based index)
    :param compute_frequencies: boolean indicating whether frequencies should
                                be computed
    :param add_opt_options: options for Gaussian's "opt" keyword (in addition
                            to "ts"). "nofreeze" is automatically added if
                            freeze is None
    :param n_cpus: number of CPUs to use
    :param memory: amount of memory to use
    :param runtime: maximum runtime
    """

    def __init__(self, geometry: Geometry, lot: LevelOfTheory, *,
                 n_cpus: int,
                 memory: Memory,
                 runtime: timedelta,
                 freeze: Iterable[int]|None = None,
                 compute_frequencies=True,
                 add_opt_options: Sequence[str] = ("tight","calcfc"),
                 additional_keywords: str = "",
                 program: Gaussian,
                 **kwargs) -> None:
        super().__init__(geometry, lot, freeze=freeze,
                         compute_frequencies=compute_frequencies,
                         transition_state=False,
                         add_opt_options=add_opt_options,
                         additional_keywords = additional_keywords,
                         program=program,
                         n_cpus=n_cpus,
                         memory=memory,
                         runtime=runtime,
                         **kwargs)


class GaussianTSOptResult(qm.TSOptResult, Result): ...

class GaussianTSOptJob(_GaussianOptJobBase[GaussianTSOptResult]):
    """Job to optimize the geometry of a transition state with Gaussian

    :param geometry: initial geometry for the optimization
    :param lot: level of theory for the computation
    :param program: Gaussian object containg the path to the executable
    :param freeze: list of atoms that should be frozen during optimization
                   (using zero-based index)
    :param compute_frequencies: boolean indicating whether frequencies should
                                be computed
    :param add_opt_options: options for Gaussian's "opt" keyword (in addition
                            to "ts"). "nofreeze" is automatically added if
                            freeze is None
    :param n_cpus: number of CPUs to use
    :param memory: amount of memory to use
    :param runtime: maximum runtime
    """


    def __init__(self,
                 geometry: Geometry,
                 lot: LevelOfTheory, *,
                 freeze: Iterable[int]|None = None,
                 compute_frequencies=True,
                 add_opt_options: Sequence[str] = ("tight","calcfc","noeigen"),
                 additional_keywords: str = "",
                 program: Gaussian, **kwargs) -> None:
        super().__init__(geometry, lot, freeze=freeze,
                         compute_frequencies=compute_frequencies,
                         transition_state=True,
                         additional_keywords = additional_keywords,
                         add_opt_options=add_opt_options,
                         program=program,
                         **kwargs)


@dataclass
class GaussianIRCResult(Result):
    endpoint_energy: float
    """scf energy of the endpoint of the IRC path [E_H]"""
    endpoint_geometry: Geometry
    """geometry of the endpoint of the IRC path [Angstrom]"""

class GaussianIRCJob(GaussianJob[GaussianIRCResult]):
    r"""
    Gaussian job for IRC scans

    :param geometry: initial geometry for the optimization
    :param lot: level of theory for the computation
    :param program: Gaussian object containg the path to the executable
    :param step_size: step size along the reaction path [0.01 Bohr]
    :param n_steps: number of points along the reaction path
    :param get_freqs_from_chk: boolean indicating whether the frequencies
                                should be read from the checkpoint file or
                                recalculated
    :param restart: boolean indicating if the IRC path should be restarted from
                    a checkpoint file. In this case, n_steps has to be
                    increased compared to the previous number
    :param old_chk_file: checkpoint file of a TS search or a previous IRC scan
                         to read frequencies or geometry infromation from
    :param result: frequencies, hessian
    :type result: GaussianIRCJob.Result
    :param \*\*kwargs: standard arguments to configure a Job (e.g. n_cpus)
    :carg CHK_FILE: path to the check point file relative to the job's
                    directory
    """

    # TODO docstring

    CHK_FILE = "irc.chk"

    def __init__(
        self,
        *,
        lot: LevelOfTheory,
        program: Gaussian,
        direction: IRCDirection,
        geometry: Geometry|None = None,
        step_size: int = 10,
        n_steps: int = 10,
        add_irc_opts: Sequence[str] = ('lqa', ),
        additional_keywords: str = "",
        get_freqs_from_chk: bool = False,
        restart: bool = False,
        old_chk_file: os.PathLike|None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            geometry=geometry, program=program, lot=lot, **kwargs
        )

        if (restart or get_freqs_from_chk) and old_chk_file is None:
            raise ValueError(
                "Must specify a checkpoint file when restarting or"
                "when reading frequencies from a checkpoint file"
            )
        if restart and geometry is not None:
            logger = logging.getLogger(__name__)
            logger.warning(
                "Restarted GaussianIRCJob received a geometry as "
                "argument. This geometry will be read from the checkpoint file"
                " and the provided geometry will be ignored."
            )
            geometry = None

        self._old_chk = old_chk_file

        self.lot = lot
        self.geometry = geometry
        self.direction = direction
        self.program = program

        # fill fields necessary to fill template
        self.chk_file = self.CHK_FILE

        self.keywords = {
            "irc": list(add_irc_opts),
            "iop(1/7=10)": []
        }

        if additional_keywords != "":
            self.keywords[additional_keywords] = []

        self._add_irc_opts(
            direction, step_size, n_steps, get_freqs_from_chk, restart
        )

    def _add_irc_opts(
        self,
        direction: IRCDirection,
        step_size: int,
        n_steps: int,
        get_freqs_from_chk: bool,
        restart: bool,
    ):
        if direction == IRCDirection.Forward:
            self.keywords['irc'].append("forward")
        elif direction == IRCDirection.Reverse:
            self.keywords['irc'].append("reverse")
        else:
            raise ValueError("Illegal direction")

        self.keywords['irc'].append(f"stepsize={step_size:d}")
        self.keywords['irc'].append(f"maxpoints={n_steps:d}")
        if get_freqs_from_chk:
            self.keywords['irc'].append("rcfc")
        else:
            self.keywords['irc'].append("CalcFC")
        if restart:
            self.keywords['irc'].append("restart")

    def gen_input(self, path):
        # copy checkpoint file to potentially read frequencies or for restart
        if self._old_chk is not None:
            chk_path = pathlib.Path(path) / self.chk_file
            shutil.copyfile(self._old_chk, chk_path)

        _GaussianInputGenerator().write_gjf(
            self, path/'irc.gjf',
            input_geometry=self.geometry is not None
        )

    @property
    def command(self):
        return f"{self.program.executable} < irc.gjf > results.log"

    def parse_result(self, path):
        try:
            log_file = os.path.join(path, "results.log")
            log_parser = GaussianLogParser(log_file)
            log_data = log_parser.parse()

            if log_data.scf_energies is None or log_data.geometries is None:
                self.fail(f"Could not read {log_file}")
            else:
                self.result = GaussianIRCResult(
                    endpoint_energy=log_data.scf_energies[-1],
                    endpoint_geometry=log_data.geometries[-1],
                )

                self.succeed()
        except ParsingError as e:
            self.fail(e)
