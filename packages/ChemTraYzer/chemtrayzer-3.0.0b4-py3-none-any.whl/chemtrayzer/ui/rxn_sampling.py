"""
Command line interface for analyze and runmd commands
"""
from __future__ import annotations

import argparse
import csv
import json
import logging
from abc import ABC
from collections import defaultdict
from collections.abc import Mapping, Sequence
from datetime import timedelta
from pathlib import Path
from typing import Annotated, Any, Literal

import numpy as np
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    NonNegativeFloat,
    NonNegativeInt,
    PositiveInt,
    StringConstraints,
    ValidationError,
    computed_field,
    field_validator,
    model_validator,
)

from chemtrayzer.core.chemid import InchiReadWriteError, Reaction, Species
from chemtrayzer.core.coords import Geometry, InvalidXYZFileError
from chemtrayzer.core.md import (
    BarostatT,
    BoxType,
    MDBox,
    MDIntegrator,
    MDJobFactory,
    MDMetadata,
    ThermostatT,
    TrajectoryParser,
)
from chemtrayzer.core.periodic_table import PERIODIC_TABLE as PTOE
from chemtrayzer.core.periodic_table import Element
from chemtrayzer.engine.cmdtools import (
    CommandLineInterface,
    IllegalConfigError,
)
from chemtrayzer.engine.config import (
    CmdArgsBase,
    ConfigBase,
    WarnOnExtraFields,
)
from chemtrayzer.engine.investigation import (
    InvestigationContext,
)
from chemtrayzer.engine.jobsystem import Memory
from chemtrayzer.io.fileutils import unique_file
from chemtrayzer.jobs.ams import AMSTrajectoryParser
from chemtrayzer.jobs.lammps import (
    Lammps,
    LammpsReaxFFJobFactory,
    LammpsTrajParser,
)
from chemtrayzer.reaction_sampling.reaction_sampling_investigation import (
    AnalyzeOnlyOptions,
    MDReactionSamplingBaseOptions,
    MDReactionSamplingInvestigation,
    RunAndAnalyzeOptions,
)


class ReactionSamplingCmdArgs(CmdArgsBase):

    o_json: Path|None = None
    o_csv: Path = Path('out.csv')

    @field_validator('o_json', 'o_csv', mode='after')
    @classmethod
    def validate_o_json(cls, v: None|Path):
        if v is not None and v.is_dir():
            raise ValueError(f'{v} is a directory. Provide a file path.')
        return v


class _MDReactionSamplingCLI(CommandLineInterface, ABC):
    """base class for the CLI commands of the MDReactionSamplingInvestigation
    """

    def add_cmd_args(self, parser: argparse.ArgumentParser):
        super().add_cmd_args(parser)
        parser.add_argument(
            '-ojson', '--output-json',
            type=Path, action='store', dest='o_json',
            help='file in which the reaction paths should be stored. The file'
                 ' will contain a field "species" with the InChIs of the '
                 'discovered species, a field "reactions" with the reactions,'
                 ' a field "reaction_times" with the times of reaction events '
                 'in femto seconds and the (zero-based) id of the observed '
                 'reactions in the list, and a field "nvt_rates" with the rate'
                 ' constant, a lower and upper bound and the number of '
                 'observed events for each reaction. Note: Since not all '
                 'time steps are written to the output file, all reactions '
                 'that occur within the output interval are listed for a '
                 'single time step.')
        parser.add_argument(
            '-ocsv', '--output-csv',
            type=Path, action='store', dest='o_csv',
            metavar='FILE',
            help='Creates two files FILE_events.csv and FILE_reactions.csv '
                 '[default: %(default)s -> out_events.csv, out_reactions.csv].'
                 ' The latter contains the rows reaction_id, reverse_id, '
                 'reactants, products, "k [(cm^3/mol)^(n-1) 1/s]", k_low, '
                 'k_high, number_of_events. The former contains the rows step,'
                 ' and reaction_id. reaction_id contains a unique number for '
                 'each type of reaction (as determined by the products and '
                 'reactants). reverse_id contains the id of the reverse '
                 'reaction, reactants and products contain a list of InChIs '
                 'each. "k [(cm^3/mol)^(n-1) 1/s]", k_low, and k_high contain '
                 'the calculated Arrhenius rate based on the MD simulation, a '
                 'lower bound, and an upper bound, respectively. '
                 'number_of_events contains the total number of observed '
                 'events for this type of reaction. step contains the point '
                 'in the trajectory where the reaction with the given id was '
                 'observed. Note that, the columns step and reaction_id in the'
                 ' _events.csv file are not unique, if multiple reactions were'
                 ' observed between two steps or if a reaction occurred '
                 'multiple times.')

        # since config is already in the parent class, we need to access the
        # action to change the default
        config_action = next(a for a in parser._actions if a.dest == 'config')
        config_action.default = 'config.toml'

    def _result2json_dict(self,
                          result: MDReactionSamplingInvestigation.Result
                          ) -> dict:
        """convert the result of the investigation to a dictionary that can
        then be serialized to a JSON file
        """
        out = {}
        rxns_list: list[Reaction] = []    # reactions in the order of detection
        id_by_rxn = dict()
        rxn_times = defaultdict(list)  # reaction ids (as in rxns_list) by time
        rxn_by_time = (result.reactions_by_time
                       if result.reactions_by_time is not None
                       else {})
        species = list(result.species) if result.species else []
                        # use list to get consistent order

        for time, rxns in rxn_by_time.items():
            for r in rxns:
                if r not in id_by_rxn:
                    id_by_rxn[r] = len(id_by_rxn)
                    rxns_list.append(r)

                rxn_times[time].append(id_by_rxn[r])

        out['species'] = [s.inchi for s in species]
        out['reactions'] = [(list(species.index(s) for s in r.reactants),
                             list(species.index(s) for s in r.products))
                             for r in rxns_list]
        out['reaction_times'] = rxn_times
        if result.nvtrates is not None:
            out['nvt_rates'] = [result.nvtrates[r] for r in rxns_list]

        return out

    def _result2csv_lists(self,
            result: MDReactionSamplingInvestigation.Result)\
            -> tuple[list[tuple[int, int, str, str, float, float, float, int]],
                     list[tuple[int, int]]]:
        """create data structures for writing csv files"""
        if result.reactions is None:
            return [], []

        id_by_rxn = {rxn: i for i, rxn in enumerate(result.reactions)}
        rates = result.nvtrates if result.nvtrates is not None else {}
        rxn_rows = []
        events_rows = []

        for rxn in result.reactions:
            k, k_low, k_high, n = rates.get(rxn, (None, None, None, None))
            # empty string if reverse reaction not detected:
            reverse_id = id_by_rxn.get(rxn.reverse(), "")
            row = (id_by_rxn[rxn],
                   reverse_id,
                   ';'.join(s.inchi for s in rxn.reactants),
                   ';'.join(s.inchi for s in rxn.products),
                   k, k_low, k_high, n)
            rxn_rows.append(row)

        for time, rxns in result.reactions_by_time.items():
            for rxn in rxns:
                events_rows.append((time, id_by_rxn[rxn]))

        return rxn_rows, events_rows

    def postprocessing(self, inves: MDReactionSamplingInvestigation,
                       config: _AnalyzeTrajConfig|_RunMDConfig):
        if inves.is_failed:
            logging.warning('The investigation failed. The output may be '
                            'incomplete!')

        if config.cmd.o_json is not None:
            json_path = unique_file(config.cmd.o_json)
            json_dict = self._result2json_dict(inves.result)

            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_dict, f, indent=2)

        csv_parent = config.cmd.o_csv.parent
        csv_stem = config.cmd.o_csv.stem

        events_filename = Path(f'{csv_stem}_events.csv')
        events_path = csv_parent / events_filename

        reactions_filename = Path(f'{csv_stem}_reactions.csv')
        reactions_path = csv_parent / reactions_filename

        rxn_rows, events_rows = self._result2csv_lists(inves.result)

        with open(events_path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_NONNUMERIC,
                                lineterminator='\n')

            writer.writerow(("step", "reaction_id"))
            writer.writerows(events_rows)

        with open(reactions_path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_NONNUMERIC,
                                lineterminator='\n')

            writer.writerow(("reaction_id", "reverse_id", "reactants",
                             "products", "k [(cm^3/mol)^(n-1) 1/s]", "k_low",
                             "k_high", "number_of_events"))
            writer.writerows(rxn_rows)


###############################################################################
# chemtrayzer analyze
###############################################################################

_ThreeByThree = tuple[tuple[float, float, float],
                      tuple[float, float, float],
                      tuple[float, float, float]]

class _AnalyzeTrajAmsMdSection(WarnOnExtraFields, BaseModel):
    """md section of configuration, if AMS is used"""

    program: Literal['ams']

class _AnalyzeTrajLammpsMdSection(WarnOnExtraFields, BaseModel):
    """md section of the configuration, if LAMMPS is used
    """
    class LammpsSection(BaseModel):
        """md.lammps section"""
        atom_type_mapping: None|dict[int, Element] = None
        atom_types: None|list[Element] = None

        @model_validator(mode='after')
        def check_atom_type_mapping_atom_types_exclusive(self):
            if (self.atom_type_mapping is None) == (self.atom_types is None):
                raise ValueError('Either atom_type_mapping or atom_types have'
                                 ' to be supplied (but not both).')
            return self

        @field_validator('atom_type_mapping', mode='before')
        @classmethod
        def validate_atom_type_mapping(cls, m: Any) -> dict[int, Element]:
            if not isinstance(m, Mapping):
                raise ValueError('atom_type_mapping must be a dictionary/map.')

            try:
                return {int(k): PTOE[v] for k, v in m.items()}
            except KeyError as err:
                raise ValueError(f'Unknown element: {err.args[0]}')
            except ValueError:       # k is not an int
                raise ValueError('atom_type_mapping must be a dictionary/map '
                                 'with integer keys and element values.')

        @field_validator('atom_types', mode='before')
        @classmethod
        def validate_atom_types(cls, at: Any) -> list[Element]:
            if not isinstance(at, list):
                raise ValueError('atom_types must be a list of elements.')

            try:
                return [PTOE[e] for e in at]
            except KeyError as err:
                raise ValueError(f'Unknown element: {err.args[0]}')

    program: Literal['lammps']
    number_of_steps: NonNegativeInt
    box_origin: tuple[float, float, float] = (0., 0., 0.)
    box_size: tuple[float, float, float]
    pbc: tuple[bool, bool, bool] = Field(alias='pbc')
    sampling_frequency: NonNegativeInt
    timestep: NonNegativeFloat
    lammps: LammpsSection
    # override types
    thermostat: ThermostatT|None = None
    barostat: BarostatT|None = None

    @computed_field
    @property
    def box_vectors(self) -> _ThreeByThree:
        return ((self.box_size[0], 0., 0.),
                (0., self.box_size[1], 0.),
                (0., 0., self.box_size[2]))

class _AnalyzeTrajCmdArgs(ReactionSamplingCmdArgs):

    trajectory: list[Path]|Path     # after validation: only list[Path]

    @field_validator('trajectory', mode='after')
    @classmethod
    def _validate_trajectory(cls, v: list[Path]|Path) -> list[Path]:
        if isinstance(v, Path):
            # normalize to list
            v = [v]

        if len(v) == 1:
            cls._validate_ams_trajectory(v)
        elif len(v) == 2:
            cls._validate_lammps_trajectory(v)
        else:
            raise ValueError(
                'Expects a single *.rkf file for analyzing an AMS trajectory '
                'or a custom.dmp and a bond.dmp file for analyzing a LAMMPS '
                'trajectory.')

        return v

    @classmethod
    def _validate_lammps_trajectory(cls, v: list[Path]):
        required_files = {'bond.dmp', 'custom.dmp'}

        files = set(p.name for p in v)
        if set(files) != required_files:
            raise ValueError(
                    'LAMMPS output files should be called bond.dmp and '
                    'custom.dump. The order of the files does not matter.')

        for path in v:
            if not path.exists():
                raise ValueError(f'File not found: {path}')

    @classmethod
    def _validate_ams_trajectory(cls, v: list[Path]):
        if not v[0].exists():
            raise ValueError(f'File not found: {v[0].as_posix()}')

        if v[0].suffix != '.rkf':
            raise ValueError('Unsupported file type. Supported types are: '
                             '.rkf')

    @computed_field
    @property
    def traj_type(self) -> Literal['ams', 'lammps']:
        """used to simplify further validation"""
        match len(self.trajectory):
            case 1:
                return 'ams'
            case 2:
                return 'lammps'
            case _:
                # this should never be reached due to previous validation
                raise RuntimeError('Could not determine trajectory type.')

    @computed_field
    @property
    def lammps_trajectory(self) -> tuple[Path, Path]|None:
        """(custom.dmp path, bond.dmp path), or None, if no LAMMPS trajectory
        """
        if self.traj_type == 'lammps':
            if self.trajectory[0].name == 'custom.dmp':
                return (self.trajectory[0], self.trajectory[1])
            else:
                return (self.trajectory[1], self.trajectory[0])
        else:
            return None

    @computed_field
    @property
    def ams_trajectory(self) -> Path|None:
        """ams.rkf path, or None, if no AMS trajectory"""

        if self.traj_type == 'ams':
            return self.trajectory[0]
        else:
            return None

class _AnalyzeTrajConfig(AnalyzeOnlyOptions, ConfigBase):

    model_config = ConfigDict(arbitrary_types_allowed=True)

    cmd: _AnalyzeTrajCmdArgs
    md: Annotated[_AnalyzeTrajAmsMdSection|_AnalyzeTrajLammpsMdSection,
                  Field(discriminator='program')]
    metadata: MDMetadata | None = Field(default=None,
                                        # give alias, b/c metadata should not
                                        # be a section of the config file, but
                                        #  for simplicity we want to inherit
                                        # from AnalyzeOnlyOptions
                                        validation_alias='__private_md__')

    @model_validator(mode='after')
    def compute_metadata(self):
        if self.md.program == 'ams':
            self.metadata = None
        else:
            box = MDBox(
                box_vectors=np.array(self.md.box_vectors),
                box_origin=self.md.box_origin,
                pbc=self.md.pbc,
                box_type=BoxType.ORTHOGONAL,
            )

            self.metadata = MDMetadata(
                initial_box=box,
                level_of_theory=None,
                number_of_steps=self.md.number_of_steps,
                timestep=self.md.timestep,
                integration_method=None,
                sampling_frequency=self.md.sampling_frequency,
                thermostat=self.md.thermostat,
                barostat=self.md.barostat,
            )

        return self

    @model_validator(mode='after')
    def check_trajectory_and_program(self):
        if self.cmd.traj_type != self.md.program:
            raise ValueError(f'config[md][program] = {self.md.program}, but'
                             ' no suitable trajectory was provided.')
        return self

class AnalyzeTrajCLI(_MDReactionSamplingCLI):
    """CLI for the analysis of a trajectory (CTY 1.0 functionality)"""

    CONFIG_MODEL = _AnalyzeTrajConfig

    def add_cmd_args(self, parser: argparse.ArgumentParser):
        super().add_cmd_args(parser)
        parser.add_argument(
            '-t', '--trajectory',
            type=Path,
            nargs = '+',
            action='store',
            dest='trajectory',
            required=True,
            help='trajectory to analyze. Please supply either one *.rkf file'
                 ' from AMS or a combination of bond.dmp and custom.dmp files'
                 ' from LAMMPS.')

    def _create_traj_parser(self, config: _AnalyzeTrajConfig)\
            -> TrajectoryParser:

        #AMS rkf files
        if isinstance(config.md, _AnalyzeTrajAmsMdSection):
            return AMSTrajectoryParser(config.cmd.ams_trajectory)
        # lammps dump files
        elif isinstance(config.md, _AnalyzeTrajLammpsMdSection):
            custom_dmp, bond_dmp = config.cmd.lammps_trajectory

            traj_parser = LammpsTrajParser(
                    bond_path=bond_dmp,
                    custom_dump_path=custom_dmp,
                    metadata = config.metadata,
                    atom_types=config.md.lammps.atom_types,
                    atom_type_mapping=config.md.lammps.atom_type_mapping)
            return traj_parser
        else:
            # should never be reached
            raise RuntimeError('Input validation failed')

    def create_investigation(self, _: InvestigationContext,
                            config: _AnalyzeTrajConfig)\
                            -> MDReactionSamplingInvestigation:
        self._traj_parser = self._create_traj_parser(config=config)


        try:
            options = AnalyzeOnlyOptions(**dict(config))
        except ValidationError as err:
            raise IllegalConfigError(self._format_pydantic_error(err))

        try:
            return MDReactionSamplingInvestigation(
                            options=options,
                            trajectoryparser=self._traj_parser)
        # when an option does not pass the check, a ValueError is raised
        except ValueError as err:
            raise IllegalConfigError(
                f'Error while checking the configuration: {err.args[0]}'
            ) from err



###############################################################################
# chemtrayzer runmd
###############################################################################

InchiStr = Annotated[str, StringConstraints(pattern=r'^InChI=1S/.*')]

class _RunMdCmdArgs(ReactionSamplingCmdArgs):

    model_config = ConfigDict(arbitrary_types_allowed=True)

    geometry: Path|None = None
    """pre-filled initial box"""
    composition: list[tuple[InchiStr|Path, PositiveInt]]|None = None
    """number of structure/species to put into the simulation box for each
    structure/species (only if initial_geometry is not provided)
    """

    @model_validator(mode='after')
    def check_geometry_composition_exclusive(self) -> _RunMdCmdArgs:
        if (self.geometry is None) == (self.composition is None):
            raise ValueError('Provide either an initial geometry or the '
                             'composition for the initial box.')
        return self

    @field_validator('geometry', mode='after')
    @classmethod
    def check_file_exists(cls, geo: Path|None) -> Path|None:
        if geo is not None:
            if not geo.exists():
                raise ValueError(f'File not found: {geo}')

        return geo

    @field_validator('composition', mode='before')
    @classmethod
    def make_list_of_tuple(cls, v: Any):
        if isinstance(v, Sequence):
            if all(isinstance(val, Sequence) and len(val)==2 for val in v):
                return v

        return [(mol, count) for mol, count in zip(*[iter(v)]*2, strict=True)]

    @field_validator('composition', mode='after')
    @classmethod
    def check_composition(cls, lst: list) -> list:

        for mol, _ in lst:
            if isinstance(mol, Path):
                if not mol.exists():
                    raise ValueError(f'File not found: {mol}')

        return lst

class _RunMdResources(BaseModel):
    """Mixin class to let user define job resources for MD job"""

    n_tasks: PositiveInt = 1
    runtime: timedelta
    memory: Memory

    @field_validator('memory', mode='before')
    @classmethod
    def validate_memory(cls, val: Any) -> Memory:
        if isinstance(val, (Memory, dict)):
            return val

        if not isinstance(val, str):
            raise ValueError('memory must be an integer followed by a unit.')

        # raises ValueError, if it does not work
        return Memory.from_str(val)

class _RunMdMetadata(BaseModel):
    """Mixin class containing options to set up a simulation"""

    number_of_steps: NonNegativeInt
    sampling_frequency: NonNegativeInt
    timestep: NonNegativeFloat
    integration_method: MDIntegrator
    thermostat: ThermostatT|None = None
    barostat: BarostatT|None = None
    box_origin: tuple[float, float, float] = (0., 0., 0.)
    box_size: tuple[float, float, float]
    pbc: tuple[bool, bool, bool] = (True, True, True)

    @computed_field
    @property
    def box_vectors(self) -> _ThreeByThree:
        return ((self.box_size[0], 0., 0.),
                (0., self.box_size[1], 0.),
                (0., 0., self.box_size[2]))

class _RunMdAmsMdSection(WarnOnExtraFields, _RunMdMetadata):
    """md section of configuration, if AMS is used"""

    class AmsSection(WarnOnExtraFields, _RunMdResources):
        """md.ams section"""

        force_field: str
        """ReaxFF force field to use."""
        amshome: Path
        """AMS home directory"""
        scmlicense: Path
        """Path to software license file"""
        scm_opengl_software: Literal["0", "1"]

    program: Literal['ams']
    ams: AmsSection


class _RunMdLammpsMdSection(WarnOnExtraFields, _RunMdMetadata):
    """md section of the configuration, if LAMMPS is used
    """
    class LammpsSection(_RunMdResources):
        """md.lammps section"""

        executable: Path
        """path to the LAMMPS executable"""
        reaxff: Path
        """path to ReaxFF force field file"""

        @field_validator('reaxff')
        @classmethod
        def validate_reaxff_file_exists(cls, val: Path) -> Path:
            if not val.exists():
                raise ValueError(f'{val} not found.')

            return val

    program: Literal['lammps']
    lammps: LammpsSection

class _PackmolSection(BaseModel):

    executable: Path
    """path to packmol executable"""

class _RunMDConfig(MDReactionSamplingBaseOptions, ConfigBase):

    model_config = ConfigDict(arbitrary_types_allowed=True)

    cmd: _RunMdCmdArgs
    md: Annotated[_RunMdAmsMdSection|_RunMdLammpsMdSection,
                  Field(discriminator='program')]
    packmol: _PackmolSection|None = None
    metadata: MDMetadata | None = Field(default=None,
                                        # give alias, b/c metadata should not
                                        # be a section of the config file, but
                                        #  for simplicity we want to inherit
                                        # from AnalyzeOnlyOptions
                                        validation_alias='__private_md__')

    @model_validator(mode='after')
    def compute_metadata(self):
        box = MDBox(
            box_vectors=np.array(self.md.box_vectors),
            box_origin=self.md.box_origin,
            pbc=self.md.pbc,
            box_type=BoxType.ORTHOGONAL,
        )

        self.metadata = MDMetadata(
            initial_box=box,
            level_of_theory=None,
            number_of_steps=self.md.number_of_steps,
            timestep=self.md.timestep,
            integration_method=self.md.integration_method,
            sampling_frequency=self.md.sampling_frequency,
            thermostat=self.md.thermostat,
            barostat=self.md.barostat,
        )

        return self

    # do not use computed_field, b/c we do not want to serialize this
    @property
    def initial_geometry(self) -> Geometry|None:
        if self.cmd.geometry is not None:
            return self._create_geo_from_xyz(self.cmd.geometry)

        return None

    @property
    def initial_composition(self) -> list[tuple[Species|Geometry, int]]|None:
        if self.cmd.composition is not None:
            validated = []
            for mol, count in self.cmd.composition:
                if isinstance(mol, str) and mol.startswith('InChI'):
                    try:
                        mol = Species.from_inchi(mol)
                    except InchiReadWriteError as err:
                        raise ValueError(
                            f'Invalid InChI: {mol}'
                        ) from err
                else:
                    mol = self._create_geo_from_xyz(mol)

                validated.append((mol, count))

            return validated

        return None

    @property
    def packmol_path(self) -> Path|None:
        if self.packmol is not None:
            return self.packmol.executable
        else:
            return None

    @classmethod
    def _create_geo_from_xyz(cls, path: Path|str) -> Geometry:
        try:
            path = Path(path)
            return Geometry.from_xyz_file(path)
        except FileNotFoundError:
            raise ValueError(f'File not found: {path}')
        except InvalidXYZFileError as err:
            raise ValueError(f'Invalid XYZ file "{path}": {err}')
        except Exception:
            raise ValueError(f'Error while reading the XYZ file "{path}":'
                             ' {err}')

class RunMDCLI(_MDReactionSamplingCLI):

    CONFIG_MODEL = _RunMDConfig

    def add_cmd_args(self, parser: argparse.ArgumentParser):
        super().add_cmd_args(parser)
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '-g', '--geometry',
            type=str,
            nargs=1,
            action='store',
            metavar='FILE',
            dest='geometry',
            help='Initial geometry of the box. (*.xyz)')
        group.add_argument(
            '-c', '--composition',
            type=str,
            action='store',
            nargs='*',
            metavar='MOL1 COUNT1',
            dest='composition',
            help='Initial composition of the box. For each molecular structure'
                 ' the count of molecules that should be put into the box must'
                 ' be given. The structure can be defined by an InChI or an '
                 '*.xyz file, e.g. -c "InChI=1S/O2/c1-2" 10 ./pentane.xyz 1.'
                 ' When using this argument, add -- at the end of the list to'
                 ' avoid reading in the workspace path as additional molecule.'
        )

    def __create_mdjob_factory(self, config: _RunMDConfig) -> MDJobFactory:
        if config.md.program == 'lammps':
            return LammpsReaxFFJobFactory(
                        reaxff_path=config.md.lammps.reaxff,
                        lammps=Lammps(
                            executable=str(config.md.lammps.executable)),
                        n_cpus=1,
                        runtime=config.md.lammps.runtime,
                        n_tasks=config.md.lammps.n_tasks,
                        memory=config.md.lammps.memory,
                        )
        elif config.md.program == 'ams':
            raise NotImplementedError('AMS is not yet supported.')
            # TODO implement
        else:
            raise IllegalConfigError(
                f'Unknown MD program: {config.md.program}. '
                'Allowed strings are: "lammps", "ams"'
            )

    def create_investigation(self, _: InvestigationContext,
                            config: _RunMDConfig)\
                            -> MDReactionSamplingInvestigation:
        md_factory = self.__create_mdjob_factory(config)

        # recreate object to get rid clutter (e.g. cmd args) and to perform
        # validation on metadata and to compute properties
        try:
            opts_dict = dict(config)
            # cannot use computed_filed, b/c the CLI would try to serialize
            # them which would not work
            opts_dict.update(dict(
                initial_geometry=config.initial_geometry,
                initial_composition=config.initial_composition,
                packmol_path=config.packmol_path
            ))
            # append
            options = RunAndAnalyzeOptions(**opts_dict)
        except ValidationError as err:
            raise IllegalConfigError(self._format_pydantic_error(err))
        except ValueError as err:
            raise IllegalConfigError() from err

        try:
            return MDReactionSamplingInvestigation(
                            options=options,
                            mdjobfactory=md_factory)
        # the investigation also performs some checks on the configuration
        # in its constructor
        except ValueError as err:
            raise IllegalConfigError(
                f'Error while checking the configuration: {err.args[0]}'
            ) from err
