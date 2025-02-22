"""
This module contains classes to perform calculations with Crest.
"""
from __future__ import annotations

import os
from math import isinf
from typing import Literal
from dataclasses import dataclass
from os import PathLike
from pathlib import Path
from scipy.constants import physical_constants, calorie, N_A
from chemtrayzer.core.coords import Geometry, ConfFilterOptions
from chemtrayzer.core.lot import LevelOfTheory, MolecularMechanics, QCMethod
from chemtrayzer.engine.jobsystem import Job, JobTemplate, Program


class ParsingError(Exception):
    """Raised when there is an issue with parsing the output file."""


class Crest(Program):
    LEVEL = {
        QCMethod.GFN_xTB: 'gfn1',
        QCMethod.GFN2_xTB: 'gfn2',
        MolecularMechanics.GFN_FF: 'gfnff'
    }

@dataclass
class CrestConfFilterOptions(ConfFilterOptions):
    energy_threshold:float = (0.05 * calorie / N_A      #default 0.05 kcal/mol
                        / physical_constants['Hartree energy'][0])
    """Energy threshold used for filtering. Crest default value coressponds to
    about 0.05 kcal/mol [Hartree]
    """
    energy_window:float = (6 * calorie / N_A      #default 6 kcal/mol
                     / physical_constants['Hartree energy'][0])
    """Energy window [Hartree] used for filtering conformers.
    Conformers with energies >= E_min + energy_window are filtered out after
    the Boltzmann-weighted filtering. Inf is not allowed.
    By default, crest energy window is 6 kcal/mol
    """
    rmsd_threshold: float = 0.125
    """RMSD threshold for distinguishing conformers. [Angstrom]"""
    rot_threshold: float = 1
    """Rotational constant threshold for distinguishing conformers.
    [percent]"""
    temperature: float = 298.15
    """Temperature [K] used for Boltzmann weighting. The higher the
    temperature, the more conformers are retained.
    """
    cum_boltzmann_threshold: float = 1.0
    """Threshold for cumulative Boltzmann weights.

    Retains the lowest energy conformers such that the sum of their
    Boltzmann weights is just greater than or equal to this threshold.
    The last conformer included is the one that causes the threshold
    to be reached/exceeded. By default, all conformers are retained.
    """
    mass_weighted:Literal[False] = False
    rigid_rotation:Literal[True] = True
    permute:Literal[False] = False

    def __post_init__(self,):
        if self.mass_weighted:
            raise ValueError("Crest does not support mass weighting")
        if not self.rigid_rotation:
            raise ValueError("Crest requires rigid rotation")
        if self.permute:
            raise ValueError("Crest does not support atom permutation")
        if isinf(self.energy_window):
            raise ValueError("Crest does not support infinite energy windows"
                             ". Use a large number instead.")


class CrestJob(Job):
    r"""
    A parser to CREST that is used for finding conformers.
    CREST documentation:
    https://xtb-docs.readthedocs.io/en/latest/crest.html


    :param geometry: Geometry object representing the molecular structure for
    the calculations.
    :param crest: Crest program instance used to run the conformer search.
    :param lot: Level of theory for the energy calculation (gfn1, gfn2, gfnff).
    :param atom_list: Optional list of atom indices to freeze during the
    conformer search. Defaults to None.
    :param conf_filter_options: Options to be used for filtering conformers.
                            Does not support mass weighted and permutation.
                            Requires rigid rotation.
    :param addTags: Optional list of additional command-line tags to pass to
    the CREST executable, e.g.
                    ['--quick', '--squick', '--mquick','--prop hess'].
                    Defaults to None.
                    "--noreftopo" is automatically added.
    :param \*\*kwargs: Standard arguments to configure a Job (e.g., n_cpus,
     memory, runtime).

    """  # noqa: W291


    @dataclass
    class Result(Job.Result):
        """result of a CREST job"""
        conformer_geometries: list[Geometry]
        '''All conformer geometries'''
        conformer_energies: list[float]
        '''Absolute energies (in Hartree) of all conformers in ascending
         order.'''
        rotamer_geometries: list[Geometry]
        '''All rotamer geometries'''
        rotamer_energies: list[float]
        '''Absolute energies (in Hartree) of all conformers in ascending
         order.'''

    _CMD_TMPL = ('${executable} geo.xyz --T ${n_cpus} --chrg ${charge} --uhf'
                 ' ${n_unpaired} ${lot_str} --noreftopo')
    _CMD_TMPL_TS = ('${executable} geo.xyz --constrain ${atom_list} '
                    '\n${executable} geo.xyz --cinp .xcontrol.sample --T '
                    '${n_cpus} --chrg ${charge} --uhf ${n_unpaired} ${lot_str}'
                    ' --noreftopo') \

    def __init__(self, geometry: Geometry, crest: Crest, lot: LevelOfTheory,
        add_cli_args: list = None, atom_list: list = None,
        conf_filter_options:CrestConfFilterOptions = CrestConfFilterOptions(),
        **kwargs) -> None:
        if 'n_tasks' in kwargs:
            raise ValueError("n_tasks must not be set. "
                             "Crest is shared-memory parallelized")
        super().__init__(n_tasks=1, **kwargs)

        self.conf_filter_options = conf_filter_options
        add_cli_args = add_cli_args if add_cli_args else []

        if value := self.conf_filter_options.energy_window:
            value *= N_A #  per particle to per mol
            value *= physical_constants['Hartree energy'][0] #hartree to jules
            value /= calorie #jules to cal
            add_cli_args.append(f"--ewin {value:.6f}") #kcal/mol

        if value := self.conf_filter_options.energy_threshold:
            value *= N_A # per mol to per particle
            value *= physical_constants['Hartree energy'][0] #hartree to jules
            value /= calorie #jules to cal
            add_cli_args.append(f"--ethr {value:.6f}") #kcal/mol

        if value := self.conf_filter_options.rmsd_threshold:
            add_cli_args.append(f"--rthr {value:.6f}") #angstrom

        if value := self.conf_filter_options.rot_threshold:
            add_cli_args.append(f"--bthr {value:.6f}") #%

        if value := self.conf_filter_options.temperature:
            add_cli_args.append(f"--temp {value:.6f}") #K

        if value := self.conf_filter_options.cum_boltzmann_threshold:
            add_cli_args.append(f"--pthr {value:.6f}") #bolzmann population

        self.output_file = "results.out"
        self.charge = lot.el_struc.charge
        self.multiplicity = lot.el_struc.multiplicity
        self.n_unpaired = self.multiplicity - 1
        self.geometry = geometry
        self.executable = crest.executable
        self.lot = lot
        #Crest uses 1-based atom indices
        self.atom_list = ','.join([str(i+1) for i in
                                   (atom_list if atom_list is not None else
                                    '')])
        self.lot_str = Crest.LEVEL[lot.method]
        self.add_cli_args = ' '.join([str(i)
                                      for i in (add_cli_args
                                                if add_cli_args is not
                                                           None else
                                           '')])
        self._CMD_TMPL = (self._CMD_TMPL + ' ' + self.add_cli_args
                          + f"> {self.output_file}")
        self._CMD_TMPL_TS = (self._CMD_TMPL_TS + ' ' + self.add_cli_args
                             + f"> {self.output_file}")
        self._template = JobTemplate(self, self._CMD_TMPL, {})
        self._template_TS = JobTemplate(self, self._CMD_TMPL_TS, {})

    def gen_input(self, input_path: PathLike):
        self.geometry.to_xyz(Path(os.path.join(input_path, 'geo.xyz')))

    @property
    def command(self):
        if self.atom_list == '':
            return self._template.command
        else:
            return self._template_TS.command

    def parse_result(self, path):

        # If the job has not failed, proceed with parsing results
        try:
            # Parse conformer geometries and energies
            rot_path = path / 'crest_rotamers.xyz'
            conf_path = path / 'crest_conformers.xyz'
            rot_geo, rot_e_str = Geometry.multiple_from_xyz_file(rot_path,
                                                         comment=True)
            conf_geo, conf_e_str = Geometry.multiple_from_xyz_file(conf_path,
                                                               comment=True)
            rot_e = [float(e.split()[0]) for e in rot_e_str]
            conf_e = [float(e) for e in conf_e_str]

            self.result = self.Result(
                conformer_geometries=conf_geo,
                conformer_energies=conf_e,
                rotamer_geometries=rot_geo,
                rotamer_energies=rot_e
            )
        except FileNotFoundError:
            return self.fail(ParsingError("Outputs could not be parsed."))

        # Path to the output file (assumed to be 'results.out').
        # Checking if the job terminated normally according to the output file.
        output_file_path = Path(path) / "results.out"
        try:
            with open(output_file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                if self.atom_list:
                    for i, line in enumerate(lines):
                        if line.strip() == "> $constrain":
                            # Look for the "atoms:" line after "> $constrain"
                            atoms_line = lines[i + 1]
                            if atoms_line.startswith(">   atoms:"):
                                break
                            else:
                                return self.fail(ValueError(
                                    "No 'atoms:' line found after"
                                    " '> $constrain' in the file"))
                            break
                    else:
                        return self.fail(ValueError(
                            "No '> $constrain' line found in the file"))

                    # Extract the atom numbers from the line
                    file_atoms = atoms_line.split(":")[1].strip().split(",")
                    file_atoms = [int(atom) for atom in file_atoms]
                    atom_list_int = [int(atom) for atom in
                                     self.atom_list.split(",")]
                    if file_atoms != atom_list_int:
                        return self.fail(
                            ValueError("The atom list in the output file does"
                                       " not match the input atom list."))

            # Attempt to check if the file exists by trying to open it

                if not lines or lines[-1].strip() != ("CREST terminated"
                                                      " normally."):
                    return self.fail("The CREST job did not terminate"
                                     " normally. "
                                     "Missing "
                                     "'CREST terminated normally.'"
                                     " in the output"
                                     " file.")
                else:
                    self.succeed()
        except FileNotFoundError:
            return self.fail(FileNotFoundError(
                f"The output file {output_file_path} does not exist."))
