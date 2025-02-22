import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Union
import os
from collections.abc import Iterable
import numpy as np
from numpy import inf

from chemtrayzer.core.chemid import Species, Reaction
from chemtrayzer.core.coords import Geometry
from chemtrayzer.engine.jobsystem import Job, Program, JobTemplate


class ParsingError(Exception):
    """Raised when there is an issue with parsing the output file."""


class MESS(Program):
    """MESS program instance."""


@dataclass
class Well:
    """
    Represents a potential well in the MESS input.
    :param:species (Species): The species associated with the well.
    :param:geometry (Geometry): The molecular geometry of the species.
    :param:energy (float): The zero-point energy of the well in Au.
    :param:frequencies (np.ndarray): The vibrational frequencies of the
     species.
    :param:name (str, optional): The name of the well.
    """
    species: Species
    geometry: Geometry
    energy: float
    frequencies: np.ndarray
    name: str = field(init=False)
    rot_sym: int = 1


@dataclass
class BimolecularFragments:
    """
    Represents a collection of wells forming a bimolecular fragment.
    :param:wells (Iterable[Well]): The wells that constitute the bimolecular
     fragments.
    :param:energy (float): The combined energy of the fragment, initialized in
     __post_init__ in Au.
    :param:name (str, optional): The name of the fragment.
    """
    wells: Iterable[Well]
    energy: float = field(init=False)
    name: str = field(init=False)

    def __post_init__(self):
        self.energy = sum(well.energy for well in self.wells)


@dataclass
class Barrier:
    """
    Represents a transition state barrier between wells in the reaction
     mechanism.
    :param:connected_wells (List[Well]): The wells that this barrier connects.
    :param:species (Species): The species associated with the transition state.
    :param:frequencies (np.ndarray): The vibrational frequencies of the
     transition
     state.
    :param:energy (float): The energy of the barrier in Au.
    :param:geometry (Geometry): The molecular geometry of the transition state.
    :param:tunneling (Optional[dict], optional): Contains tunneling parameters
     if
     applicable.
    :param:name (str, optional): The name of the barrier.
    """
    connected_wells: list[Well | BimolecularFragments]
    frequencies: np.ndarray
    energy: float
    geometry: Geometry
    tunneling: Optional[dict] = None
    name: str = field(default=None)
    rot_sym: int = 1


class MESSJob(Job):
    """Represents a MESS job for master equation calculations."""
    _CMD_TMPL = '${executable} mess.inp'

    @dataclass
    class Options:
        """
        Defines global options for a MESS job.
        :param:executable (str): MESS program instance used to run a Master
        equation simulation.
        :param:temperature_list (list[float]): The list of temperatures in
         Kelvin.
        :param:pressure_list (list[float]): The list of pressures in atm.
        :param:energy_step_over_temperature (float): Energy step over
         temperature
         ratio.
        :param:excess_energy_over_temperature (float): Excess energy over
         temperature ratio.
        :param:model_energy_limit (float): The model energy limit in kcal/mol.
        :param:calculation_method (str): The method used for calculations.
        :param:energy_relaxation_model (str): The energy relaxation model type.
        :param:energy_relaxation_factor (float): The energy relaxation factor
         in 1/cm.
        :param:energy_relaxation_power (float): The power of the energy
         relaxation model.
        :param:energy_relaxation_exponent_cutoff (float): Cutoff exponent for
         relaxation.
        :param:lj_parameters (dict[str, dict[str, float]]): Lennard-Jones
         parameters for bath gas and complex.
        :param:command (str): The command to execute the MESS job.
        """
        mess: MESS
        temperature_list: list[float]
        pressure_list: list[float]
        energy_step_over_temperature: float = 0.2
        excess_energy_over_temperature: float = 30.0
        model_energy_limit: float = 400.0
        calculation_method: str = "direct"

        # Energy Relaxation Model
        energy_relaxation_model: str = "Exponential"
        energy_relaxation_factor: float = 100.0  # in 1/cm
        energy_relaxation_power: float = 0.85
        energy_relaxation_exponent_cutoff: float = 15.0

        # Explicit Lennard-Jones parameters for bath gas and complex
        # with default zero values
        lj_parameters: dict[str, dict[str, float]] = field(
            default_factory=lambda: {
                "bath_gas": {"epsilon": 0.0, "sigma": 0.0, "mass": 0.0},
                "complex": {"epsilon": 0.0, "sigma": 0.0, "mass": 0.0},
            }
        )

        def __post_init__(self):
            """Validate LJ parameters."""
            # Ensure both required LJ parameter sets exist
            required_sets = {"bath_gas", "complex"}
            if set(self.lj_parameters.keys()) != required_sets:
                raise ValueError(
                    f"LJ parameters must contain exactly {required_sets},"
                    f" but got {self.lj_parameters.keys()}")

            # Ensure each set has the required properties
            required_fields = {"epsilon", "sigma", "mass"}
            for key, params in self.lj_parameters.items():
                if set(params.keys()) != required_fields:
                    raise ValueError(
                        f"LJ parameters for '{key}' must contain"
                        f" {required_fields}, but got {params.keys()}")

    @dataclass
    class Result(Job.Result):
        """
        Stores the results of a MESS job.
        :param:rate_constants dict[str, dict[str, list[tuple(float,float)]]]:
         Dictionary of rate constants for different reactions, dependent on
         pressure and temperature, e.g.
         
         parsed_results =
         {"[C]#O.[H].[H]>>[CH] + [OH]":
         [(0.1, 300.0, 75.7), (0.1, 500.0, 24600.0),
         (1, 300.0, 620.0), (1, 500.0, 221000.0),
        (inf, 300.0, 1e-20), (inf, 500.0, 3e-20)]}
         
        with pressures 0.1 bar, 1 bar, and inf (high-pressure limit),
        temperature [K] and rate constant [1/s], [cm^3/s] etc. at 2nd and
        3rd position in tuples
        """
        pT_rate_constants: dict[Reaction, list[tuple[float, float, float]]]
        high_pressure_limit_rate_constants: dict[Reaction, list[tuple[float,
                                                 float]]]
        total_well_fleeting_rate_constants: dict[Species | tuple[Species],
                                                 list[tuple[float, float,
                                                      float]]]

    @property
    def command(self):
        return self._template.command

    def __init__(self, options: 'MESSJob.Options', wells:
                 list[Well | BimolecularFragments],
                 barriers: list[Barrier] = None, **kwargs):
        """Initializes a MESS job with the specified options.

        :param: options (MESSJob.Options): The options object defining job
        parameters.
         :param:wells (list[Well]): list of wells in the reaction system.
        :param:barriers (list[Barrier], optional): List of barriers in the
         system.

        """
        super().__init__(**kwargs)
        self.options = options
        self.wells = wells
        self.barriers = barriers
        self.result = None
        self.executable = options.mess.executable
        self._template = JobTemplate(self, self._CMD_TMPL, {})
        self.species_dict = {}

    def well_string(self, well: Well, indentation="") -> str:
        """Generates the MESS input for a well."""
        input_str = f"{indentation}" + (f"Well {well.name} #"
                                        f" {well.species.smiles}\n")
        input_str += f"{indentation}" + "    Species\n"
        input_str += f"{indentation}" + "      RRHO\n"
        input_str += f"{indentation}" + (f"         Geometry[angstrom] "
                                         f"{well.geometry.n_atoms}\n")
        for atom, coord in zip(well.geometry.atom_types, well.geometry.coords):
            input_str += f"{indentation}" + (f"           {str(atom)}"
                                             f" {coord[0]:.6f} {coord[1]:.6f}"
                                             f" {coord[2]:.6f}\n")
        input_str += f"{indentation}" + "         Core RigidRotor\n"
        input_str += f"{indentation}" + (f"             SymmetryFactor"
                                         f" {well.rot_sym}\n")
        input_str += f"{indentation}" + "         End\n"
        input_str += f"{indentation}" + (f"         Frequencies[1/cm] "
                                         f" {len(well.frequencies)}\n")
        input_str += f"{indentation}" + "         "
        for i, freq in enumerate(well.frequencies):
            if i % 7 == 0 and i != 0:
                input_str += "\n         " + f"{indentation}"
            input_str += f"{freq}     "
        input_str += "\n"
        input_str += f"{indentation}" + (f"         ZeroEnergy[au]"
                                         f" {well.energy:.4f}\n")
        input_str += f"{indentation}" + "      End\n"
        input_str += f"{indentation}" + "End\n\n"
        return input_str

    def bimolecular_fragment_string(self, bimolecular_fragment:
                                    BimolecularFragments) -> str:
        """Generates the MESS input for a bimolecular fragment."""
        input_str = f"Bimolecular {bimolecular_fragment.name}\n"
        indentation = "  "
        for well in bimolecular_fragment.wells:
            well.name = ""
            well_str = self.well_string(well, indentation=indentation)
            # In the well string, replace "Well" with "Fragment" for
            # bimolecular
            well_str = well_str.replace("None", "")
            well_str = well_str.replace("#", "")
            well_str = well_str.replace("  Well", "  Fragment")
            well_str = well_str.replace("  Species\n", "")
            well_str = well_str.replace(
                f"ZeroEnergy[au] {well.energy:.4f}",
                "ZeroEnergy[au] 0")
            well_str = well_str.rsplit("End", 1)[0]  # Remove the
            # last
            # occurence
            # of string "End"
            input_str += well_str
            # ground_energy += well.energy
        input_str += indentation + (f"GroundEnergy[au]"
                                    f" {bimolecular_fragment.energy:.4f}\n")
        input_str += "End\n\n"

        return input_str

    def barrier_string(self, barrier: Barrier) -> str:
        """Generates the MESS input for a barrier."""
        barrier_str = (f"Barrier {barrier.name}"
                       f" {barrier.connected_wells[0].name}"
                       f" {barrier.connected_wells[1].name}\n")
        barrier_str += "      RRHO\n"
        barrier_str += ("         Geometry[angstrom]"
                        f" {barrier.geometry.n_atoms}\n")
        for atom, coord in zip(barrier.geometry.atom_types,
                               barrier.geometry.coords):
            barrier_str += (f"           {str(atom)}"
                            f" {coord[0]:.6f} {coord[1]:.6f}"
                            f" {coord[2]:.6f}\n")
        barrier_str += "         Core RigidRotor\n"
        barrier_str += f"           SymmetryFactor {barrier.rot_sym}\n"
        barrier_str += "         End\n"
        barrier_str += ("         Frequencies[1/cm]"
                        f" {len(barrier.frequencies)}\n")
        barrier_str += "         "
        for i, freq in enumerate(barrier.frequencies):
            if i % 7 == 0 and i != 0:
                barrier_str += "\n         "
            barrier_str += f"{freq}     "
        barrier_str += "\n"
        barrier_str += f"         ZeroEnergy[au] {barrier.energy:.4f}\n"
        if barrier.tunneling:
            barrier_str += "         Tunneling  Eckart\n"
            barrier_str += ("           ImaginaryFrequency[1/cm]"
                            "            "
                            f"{np.abs(barrier.tunneling['imag_freq'])}\n")
            welldp_0 = ((barrier.energy - barrier.connected_wells[0].energy)
                        * 630)
            welldp_1 = ((barrier.energy - barrier.connected_wells[1].energy)
                        * 630)
            barrier_str += ("           WellDepth[kcal/mol] "
                            f"{welldp_0}"
                            "\n")
            barrier_str += ("           WellDepth[kcal/mol] "
                            f"{welldp_1}"
                            "\n")
        barrier_str += "      End\n"
        barrier_str += "End\n\n"
        return barrier_str

    def gen_input(self, input_path) -> str:
        """Generates the MESS input as a string with all required keywords."""

        input_str = "!Mess input file generated by chemtrayzer\n"
        input_str += "TemperatureList[K] " + " ".join(
            map(str, self.options.temperature_list)) + "\n"
        input_str += "PressureList[atm] " + " ".join(
            map(str, self.options.pressure_list)) + "\n"
        input_str += ("EnergyStepOverTemperature"
                      f" {self.options.energy_step_over_temperature}\n")
        input_str += ("ExcessEnergyOverTemperature"
                      f" {self.options.excess_energy_over_temperature}\n")
        input_str += ("ModelEnergyLimit[kcal/mol]"
                      f" {self.options.model_energy_limit}\n")
        input_str += f"CalculationMethod {self.options.calculation_method}\n"
        input_str += "RateOutput results.out\n\n"
        input_str += "\nModel\n"
        input_str += "  EnergyRelaxation\n"
        input_str += f"    {self.options.energy_relaxation_model}\n"
        input_str += ("      Factor[1/cm]"
                      f" {self.options.energy_relaxation_factor}\n")
        input_str += f"      Power {self.options.energy_relaxation_power}\n"
        input_str += ("      ExponentCutoff"
                      f" {self.options.energy_relaxation_exponent_cutoff}\n")
        input_str += "    End\n"
        input_str += "  CollisionFrequency\n"
        input_str += "    LennardJones\n"
        input_str += ("      Epsilons[1/cm]"
                      f" {self.options.lj_parameters['bath_gas']['epsilon']}"
                      f" {self.options.lj_parameters['complex']['epsilon']}\n")
        input_str += ("      Sigmas[angstrom] "
                      f"{self.options.lj_parameters['bath_gas']['sigma']} "
                      f"{self.options.lj_parameters['complex']['sigma']}\n")
        input_str += ("      Masses[amu] "
                      f"{self.options.lj_parameters['bath_gas']['mass']} "
                      f"{self.options.lj_parameters['complex']['mass']}\n")
        input_str += "  End\n\n"
        self.species_dict = {}
        well_energy_list = []
        for well in self.wells:
            well_energy_list.append(well.energy)
            well.energy -= min(well_energy_list)
        for i, well in enumerate(self.wells):
            well.name = f"W{i}"
            if isinstance(well, Well):
                input_str += self.well_string(well)
                self.species_dict.update({well.name: well.species})
            elif isinstance(well, BimolecularFragments):
                input_str += self.bimolecular_fragment_string(well)
                self.species_dict.update({well.name: [well.wells[0].species,
                                                      well.wells[1].species]})
        for i, barrier in enumerate(self.barriers):
            barrier.energy -= min(well_energy_list)
            barrier.name = f"B{i}"
            input_str += self.barrier_string(barrier)

        input_str += "End\n"
        with open(Path(os.path.join(input_path, 'mess.inp')), 'w') as f:
            f.write(input_str)
        return input_str

    def parse_result(self, path):
        def gen_reaction_obj_input(well: Union[list[Species], Species]):
            if isinstance(well, list):
                return well
            else:
                return [well]

        file_path = Path(path) / "results.out"
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            raise self.fail(FileNotFoundError(
                f"The output file {file_path} does not exist or is empty."))
        if 'Temperature-Pressure Rate Tables:\n' not in lines:
            return self.fail(ParsingError("No 2D rate constants array (T-,p-"
                                          "dependent) detected in results.out")
                             )

        result = {}
        hpl_result = {}
        pt_result = {}
        total_well_fleeting_result = {}
        reaction = None
        temperatures = []
        data_section = False

        try:
            for line in lines:
                line = line.strip()

                if line.startswith("Temperature-Pressure Rate Tables:"):
                    data_section = True
                    continue

                if data_section:
                    if "->" in line:  # Reaction identifier
                        current_reaction = line.strip()
                        reactants = current_reaction.split("->")
                        if self.species_dict:
                            if (reactants[0] in list(self.species_dict.keys())
                                    and reactants[1] in list(self.species_dict.
                                                             keys())):
                                reaction = Reaction(gen_reaction_obj_input(
                                    self.species_dict[reactants[0]]),
                                    gen_reaction_obj_input(
                                        self.species_dict[reactants[
                                            1]]))
                            # for escape rates
                            elif not reactants[1].strip():
                                reaction = self.species_dict[reactants[0]]
                                if isinstance(reaction, list):
                                    reaction = tuple(reaction)
                        else:
                            reaction = (
                                f"{reactants[0]}"
                                f"->{reactants[1]}")
                        result[reaction] = []
                        temperatures = []
                        continue

                    split_line = re.split(r'\s+', line)

                    if 'P\T' in line:  # Extract temperatures
                        try:
                            temperatures = list(map(float, split_line[1:]))
                        except ValueError:
                            raise self.fail(ValueError(
                                "Error parsing"
                                " temperatures from the table header."))
                        continue

                    if temperatures and len(
                            split_line) > 1:  # Extract
                        # pressures and rate constants
                        pressure = split_line[0]
                        if pressure == 'O-O':
                            pressure = inf
                        else:
                            pressure = float(pressure)
                        rate_constants = []
                        for value in split_line[1:]:
                            try:
                                rate_constants.append(float(value))
                            except ValueError:
                                rate_constants.append(
                                    None)  # Use None for missing values
                        pressure_array = [pressure] * len(rate_constants)
                        # Store data in dictionary
                        result[reaction] += list(zip(pressure_array,
                                                     temperatures,
                                                     rate_constants))
            for react, data in result.items():
                if isinstance(react, Reaction):
                    pt_result[react] = []
                    hpl_result[react] = []
                    for pTk_combi in data:
                        if pTk_combi[0] != inf:
                            pt_result[react] += [pTk_combi]
                        else:
                            hpl_result[react] += [(pTk_combi[1], pTk_combi[2])]
                if isinstance(react, Species | tuple):
                    total_well_fleeting_result[react] = result[react]
            self.result = self.Result(
                high_pressure_limit_rate_constants=hpl_result,
                total_well_fleeting_rate_constants=total_well_fleeting_result,
                pT_rate_constants=pt_result)

            log_path = path / 'mess.log'
            with open(log_path, "r", encoding="utf-8") as log:
                loglines = log.readlines()
                if (not loglines or loglines[-1].split(',') !=
                        'rate calculation done'):
                    self.fail("The MESS job did not terminate normally. "
                              "Missing termination message in mess.log.")
                else:
                    self.succeed()

        except ValueError:
            raise self.fail(ValueError("No data was parsed from the  file."))
