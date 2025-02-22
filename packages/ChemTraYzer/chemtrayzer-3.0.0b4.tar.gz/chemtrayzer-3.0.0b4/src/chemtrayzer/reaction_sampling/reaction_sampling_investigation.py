from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
import time
from typing import  TypeVar

import numpy as np
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    NonNegativeFloat,
    PositiveFloat,
    PositiveInt,
    field_validator,
    model_validator,
)

from chemtrayzer.core.chemid import  Reaction, Species
from chemtrayzer.core.coords import Geometry, TSGeometry
from chemtrayzer.core.md import (
    PSTAT_NOT_SET,
    BoxType,
    MDJob,
    MDJobFactory,
    MDMetadata,
    TrajectoryParser,
)
from chemtrayzer.engine.investigation import (
    Investigation,
)
from chemtrayzer.jobs.packmol import PackmolJob, PackmolJobFactory
from chemtrayzer.reaction_sampling.reaction_detection import (
    NVTRateConstants,
    ReactionDetector,
)


class MDReactionSamplingBaseOptions(BaseModel):
    """Options for :class:`MDReactionSamplingInvestigation`"""

    metadata: MDMetadata|None
    """molecular dynamics simulation metadata"""
    bond_initial_threshold: PositiveFloat = 0.5
    """In the first frame, bonds with bond orders below are regarded as
    non-existent.
    """
    bond_breaking_threshold: PositiveFloat = 0.3
    """Bonds are regarded as breaking, if their bond order drops below this
    value.
    """
    bond_forming_threshold: PositiveFloat = 0.8
    """Bonds are regarded as forming, if their bond order rises above this
    value.
    """
    molecule_stable_time: PositiveFloat = 3
    """For recrossing. Minimum lifetime in fs to mark molecules as stable.
    Stable molecules can serve as reactants and products, unstable molecules
    are regarded as intermediates.
    """
    reaction_path_margin: PositiveInt = 20
    """For reaction paths. Number of geometries to save as reaction path before
    and after a reaction event.
    """
    calculate_nvt_rate_coeffs: bool = True
    """toggle the computation of canonical ensemble rate coefficients (NVT)"""
    confidence: float = Field(default=0.9, gt=0, lt=1)
    """confidence interval for the rate coefficient error bounds (0...1)"""
    start: NonNegativeFloat = 0.0
    """time of the trajectory to start the rate coefficient analysis from"""

    @field_validator('metadata')
    @classmethod
    def check_metadata(cls, metadata: MDMetadata|None) -> MDMetadata|None:
        if metadata is not None:
            if metadata.initial_box is None:
                raise ValueError('Simulation box information must be provided')
            if metadata.initial_box.box_type not in (BoxType.ORTHOGONAL,
                                                     BoxType.ORTHOGONALSLAB):
                raise ValueError('Box must be orthogonal.')

            if (metadata.barostat != PSTAT_NOT_SET
                and metadata.barostat is not None):
                raise ValueError('Barostats are currently not supported.')

        return metadata

    @model_validator(mode='after')
    def check_thresholds(self):
        if (self.bond_breaking_threshold >= self.bond_initial_threshold
            or self.bond_initial_threshold >= self.bond_forming_threshold):
            raise ValueError('bond_breaking_threshold < bond_initial_threshold'
                             ' < bond_forming_threshold')

        return self


class AnalyzeOnlyOptions(MDReactionSamplingBaseOptions):
    """Options for :class:`MDReactionSamplingInvestigation` for only analyzing
    a given trajectory
    """

    metadata: MDMetadata|None = None
    """MD metadata that cannot be read from the trajectory"""

class RunAndAnalyzeOptions(MDReactionSamplingBaseOptions):
    """Options for :class:`MDReactionSamplingInvestigation` for running an MD
    simulation and analyzing it
    """

    model_config = ConfigDict(arbitrary_types_allowed=True) # for Geometry

    initial_geometry: Geometry|None = None
    """pre-filled initial box"""
    initial_composition: list[tuple[Species|Geometry, int]]|None = None
    """number of structure/species to put into the simulation box for each
       structure/species (only if initial_geometry is not provided)
    """
    packmol_path: Path|None = None
    """path to packmol exe"""
    metadata: MDMetadata
    """MD metadata to use when setting up the simulation"""

    @model_validator(mode='after')
    def check_initial_comp_and_packmol_if_no_initial_geometry(self):
        if self.initial_geometry is None:
            if self.packmol_path is None:
                raise ValueError('Must provide packmol path, if no initial '
                                'geometry is provided.')
            if self.initial_composition is None:
                raise ValueError('Must provide initial composition, if no '
                                 'initial geometry is provided.')
            if self.metadata.initial_box is None:
                raise ValueError('Must provide initial box details, if no '
                                 'initial geometry is provided.')

        return self

class MDReactionSamplingInvestigation(Investigation):
    """
    A workflow similar to CTY version 1.0. An MD trajectory is created unless
    provided, and analyzed to find reactions and NVT rate coefficients.
    This investigation either takes a trajectory parser and analyzes the
    contained trajectory, or takes a MDJob factory to produce the trajectory.
    In case of providing the MDJob factory, Options.metadata must be set too
    and there must be an initial box geometry, either via
    Options.initial_geometry or by providing .packmolpath and
    .initial_composition in Options.

    :param options: Various options for running and analyzing the MD simulation
    :param trajectoryparser: A parser object that provides the MD trajectory.
                             If mdjobfactory is set to None, a trajectory
                             parser is mandatory.
    :param mdjobfactory: An MDJobFactory object that provides an MDJob.
                         If MDJobFactory is given, options.metadata is
                         mandatory, and any trajectoryparser will be ignored.
    """
    OptionsT = TypeVar('OptionsT', AnalyzeOnlyOptions, RunAndAnalyzeOptions)

    # type hint: more specific than Investigation.Result
    result: Result
    options: MDReactionSamplingInvestigation.OptionsT

    @dataclass
    class Result(Investigation.Result):
        species: set[Species] = None
        """set of detected species"""
        reactions: set[Reaction] = None
        """set of detected reactions"""
        geometries: Mapping[Reaction| Species, Geometry] = None
        """Geometries of species and transistion states in a dictionary with
        species and reactions as keys"""
        reaction_paths: Mapping[Reaction, list[TSGeometry]] = None
        """Geometries of reaction paths in a dictionary with reactions as keys
        """
        reactions_by_time: Mapping[float, list[Reaction]] = None
        """dictionary of reactions sorted by time of occurence"""
        nvtrates: Mapping[Reaction, tuple[float, float, float, int]] = None
        """rate constant, lower bound, upper bound and number of occurrences
        for each reaction [(cm^3/mol)^(n-1) 1/s] (see Kröger et al. J. Chem.
        Theory Comput. 2017 https://doi.org/10.1021/acs.jctc.7b00524)"""

    def __init__(self,
                 options: OptionsT,
                 trajectoryparser: TrajectoryParser|None = None,
                 mdjobfactory: MDJobFactory|None = None):
        super().__init__()


        # arguments
        self.trajectoryparser = trajectoryparser
        self.mdjobfactory = mdjobfactory
        self.options: MDReactionSamplingInvestigation.OptionsT = options

        # temporary variables
        self._initial_composition: Mapping[Species, int] = None
        self.timestep = None
        self.volume = None
        self.initial_geometry = None
        self.reactions_by_time = None

        # results
        self.result = self.Result()

        # start
        self._check_options()

    def _check_options(self):
        """
        decide whether to run an MD or take a finished trajectory based on the
        provided options
        """
        # decision whether to run MD or just take a finished trajectory
        # when running a MD, either the initial geometry is given or the info
        # how to create it via a PackmolJob.

        if (self.mdjobfactory is None) == (self.trajectoryparser is None):
            raise ValueError('Provide trajectoryparser or mdjobfactory, but '
                             'not both')

        if self.mdjobfactory is None:  # trajectoryparser provided
            # assume that only a trajectory should be analyzed
            if not isinstance(self.options, AnalyzeOnlyOptions):
                raise ValueError('AnalyzeOnlyOptions must be provided when '
                                 'no MDJobFactory is given.')

            # next step is reaction sampling using self.trajectoryparser
            self.add_step(self.reaction_sampling)

        else:  # mdjobfactory is set
            if not isinstance(self.options, RunAndAnalyzeOptions):
                raise ValueError('RunAndAnalyzeOptions must be provided when '
                                 'an MDJobFactory is given.')

            if self.options.initial_geometry is None:
                self.add_step(self.make_packmoljob)
            else:
                self.add_step(self.run_md)


    def make_packmoljob(self):
        """
        Run the packmoljob, if requested.
        """
        species_geometries = [
            Geometry.from_inchi(mol.inchi)
                if isinstance(mol, Species)
                else mol    # assume geometry, if not species
            for mol, count in self.options.initial_composition]

        box_vecs = self.options.metadata.initial_box.box_vectors
        box_origin = self.options.metadata.initial_box.box_origin

        assert self.options.metadata.initial_box.box_type == BoxType.ORTHOGONAL

        # box is defined by two corners diagonal to each other. The first one
        # is the origin, the second one is the origin shifted by the box
        # vectors
        near_corner = (np.array(box_origin)
                        if box_origin is not None
                        else np.zeros(3))
        far_corner = near_corner + np.sum(box_vecs, axis=1)
        box_dim = (*near_corner, *far_corner)

        packmoljobfactory = PackmolJobFactory(self.options.packmol_path)
        packmoljob = packmoljobfactory.create(
            'packmol',
            species_geometries,
            [count for _, count in self.options.initial_composition],
            box_dim,
        )
        self.add_step(self.run_md)
        self.wait_for_and_submit(packmoljob)

    def run_md(self, packmoljob: PackmolJob = None):
        """
        Run the MD simulation.

        :param packmoljob: optional, if a new simulation was requested, the
                           packmoljob will be passed here.
        """
        self.initial_geometry = self.options.initial_geometry
        # if a box job has run, use it to create an MD job
        if packmoljob is not None:
            if packmoljob.is_failed:
                self.fail('the MD box job was not successful')
            self.initial_geometry = packmoljob.result.box

        mdjob = self.mdjobfactory.create(
            metadata=self.options.metadata,
            initial_geometry=self.initial_geometry,
            name='main_md_simulation',
        )

        self.add_step(self.reaction_sampling)
        self.wait_for_and_submit(mdjob)

    def reaction_sampling(self, mdjob: MDJob = None):
        """
        Do the analysis of the trajectory. Detect reactions and species,
        extract geometries for species and reactions.

        :param mdjob: optional, if the investigation started an MDJob it will
                      be passed here.
        """
        # TODO do not hardcode -> maybe as option?
        n_consecutive = 5000  # number of framse that are analyzed at once

        # if an MD job has run, take the trajectory parser from there
        if mdjob is not None:
            if mdjob.is_failed:
                self.fail('the MD job was not successful')
            self.trajectoryparser = mdjob.result


        # detect reactions and extract geometries
        detector = ReactionDetector(
                    bond_initial_threshold=self.options.bond_initial_threshold,
                    bond_breaking_threshold=self.options.bond_breaking_threshold,
                    bond_forming_threshold=self.options.bond_forming_threshold,
                    molecule_stable_time=self.options.molecule_stable_time,
                    reaction_path_margin=self.options.reaction_path_margin,
                    parser=self.trajectoryparser)

        prev_frame_nr = -1
        first_iteration = True
        while detector.current_frame_number > prev_frame_nr:
            prev_frame_nr = detector.current_frame_number

            t0 = time.time_ns()
            # only analyze few frames at once to save RAM
            detector.detect(n_consecutive)
            dt = (time.time_ns() - t0)*1e-9
            self._logger.debug(
                f'Analyzed {n_consecutive:d} frames in {dt:.4f} s. Current '
                f'frame: {detector.current_frame_number}')

            if first_iteration:
                if (detector.metadata.barostat != PSTAT_NOT_SET
                    and self.options.calculate_nvt_rate_coeffs):
                    raise ValueError(
                            'MD rate coefficients cannot be calculated, if a '
                            'barostat was used.')

                self.volume = detector.metadata.initial_box.volume
                self.timestep = detector.metadata.timestep
                self._initial_composition = detector.initial_composition
                first_iteration = False


        # if the detection failed, exit and leave all results at None
        if not detector.reactive_events:
            self.fail('The reaction detection could not find any species.')

        self.reactive_events = detector.reactive_events

        self._populate_results_from_reactive_events()

        # decide whether to calculate NVT rate coefficients
        if self.options.calculate_nvt_rate_coeffs:
            self.add_step(self.mdrates)
        else:
            # finished
            self.succeed()

    def _populate_results_from_reactive_events(self):
        """Populate the result object with data from reactive events."""
        self.result.reactive_events = self.reactive_events

        # Initialize all collections
        reactions_by_time = defaultdict(list)
        species = set()
        reactions = set()
        reaction_paths = defaultdict(list)
        geometries = defaultdict(list)

        # Process all data in a single loop over reactive events
        for event in self.reactive_events:
            # Handle reactions by time
            reactions_by_time[event.reaction_time].append(event.reaction)

            # Handle species
            species.update(event.reaction.reactants)
            species.update(event.reaction.products)

            # Handle reactions
            reactions.add(event.reaction)

            # Handle reaction paths
            reaction_paths[event.reaction] = event.geometries

            # Handle geometries
            for spec, mol_geometries in event.product_geometries.items():
                geometries[spec].extend(mol_geometries)
            geometries[event.reaction].append(event.ts_geo)

        # Assign results
        self.reactions_by_time = reactions_by_time
        self.result.reactions_by_time = reactions_by_time
        self.result.species = species
        self.result.reactions = reactions
        self.result.reaction_paths = reaction_paths
        self.result.geometries = geometries

    def mdrates(self):
        """
        Estimate Arrhenius parameters for the detected reactions.
        """
        # compute and save rate coefficients
        nvtrates = NVTRateConstants(self._initial_composition,
                                    self.reactions_by_time,
                                    self.timestep,
                                    self.volume,
                                    self.options.confidence,
                                    self.options.start)
        nvtrates.compute()
        self.result.nvtrates = nvtrates.compact_result()

        # jump to end
        self.succeed()
