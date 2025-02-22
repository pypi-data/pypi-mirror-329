# ruff: noqa
'''Workflows dealing with stable species (i.e. optimized geometries)

This module contains investigations that optimize geometries and compute single
point energies and frequency information at different levels of theory.
'''
from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from functools import partial
import logging
from math import inf
from typing import Callable, Protocol, cast
from collections.abc import Iterable

from chemtrayzer.core.qm import QmResourceSpec

from chemtrayzer.core.chemid import Species
from chemtrayzer.core.coords import Geometry
from chemtrayzer.core.database import (
    GeoId,
    GeometricConformerCriterion,
    GeometryDatabase,
    OptimizedAt,
    SpeciesDB,
)
from chemtrayzer.core.lot import LevelOfTheory, QMSoftware
from chemtrayzer.engine import DependencyFailure, Investigation, Result, Failure
from chemtrayzer.jobs.gaussian import (
    Gaussian,
    GaussianEnergyJob,
    GaussianFreqJob,
    GaussianOptJob,
    GaussianOptions,
)
from chemtrayzer.jobs.orca import Orca, OrcaEnergyJob


class OptimizationJobFailure(DependencyFailure):
    '''indicates that the geometry optimization failed'''

class FrequencyJobFailure(DependencyFailure):
    '''indicates that the frequency calculation failed'''

class SpeComputationFailure(DependencyFailure):
    '''indicates that the geometry optimization failed'''

class WrongSpeciesFailure(Failure):
    '''indicates that the optimized geometry belongs to a different species than
    the initial geometry'''

class SpeLotOptions(Protocol):
        energy_lot: LevelOfTheory|None
        energy_resources: QmResourceSpec
        energy_gaussian_options: GaussianOptions
        gaussian: Gaussian|None
        orca: Orca|None = None
        default_software: QMSoftware = QMSoftware.GAUSSIAN

class ComputeSPEMixin:
    """mixin class for investigations that compute an SPE as last step"""

    options: SpeLotOptions
    _spe_geo_id: GeoId
    """id of the geometry for which the SPE should be computed"""
    _spe_db_name: str = "species_db"
    """name of the DB (in the context) in which the geometry with _spe_geo_id
    is stored"""

    def _is_energy_at_lot_in_db(self, geo_id: GeoId,
                                energy_lot: LevelOfTheory) -> bool:
        """:return: True, if energy at given levle of theory already exists
                    for geometry with geo_id, False otherwise
        """
        db = cast(SpeciesDB, self.context['species_db'])

        lots = db.list_LOT_of_energies(geo_id)
        energy_lot_hash = hash(energy_lot.to_json(exclude_non_hash_fields=True,
                                           exclude_default_values=True))

        for lot in lots:
            lot_hash = hash(lot.to_json(exclude_default_values=True,
                                        exclude_non_hash_fields=True))
            if lot_hash == energy_lot_hash:
                return True

        return False

    def compute_spe(self):
        '''submit SPE job if one is requested'''
        db = cast(GeometryDatabase, self.context[self._spe_db_name])

        if self.options.energy_lot is not None:
            if self._is_energy_at_lot_in_db(self._spe_geo_id,
                                            self.options.energy_lot):
                self._logger.info('Geometry with id %d already has energy at '
                                  'requested level of theory',
                                  self._spe_geo_id)
                self.succeed()
                return

            geometry = db.load_geometry(self._spe_geo_id)
            software = self.options.energy_lot.software


            if software == QMSoftware.GAUSSIAN:
                energy_job = GaussianEnergyJob(
                    geometry = geometry,
                    lot = self.options.energy_lot,
                    program = self.options.gaussian,
                    add_opt_options=self.options.energy_gaussian_options
                                                        .opt_options,
                    additional_keywords=self.options.energy_gaussian_options
                                                        .additional_keywords,
                    **self.options.energy_resources.eval(
                                            geometry.atom_types,
                                            p_type='shared')
                    )
            elif software == QMSoftware.ORCA:
                energy_job = OrcaEnergyJob(
                    geometry = geometry,
                    lot = self.options.energy_lot,
                    program=self.options.orca,
                    **self.options.energy_resources.eval(
                                            geometry.atom_types,
                                            p_type='distributed')
                    )
            else:
                raise RuntimeError(f'Unsupported software: {software}')

            self.add_step(self.process_spe_job)
            self.wait_for_and_submit(energy_job)

        else:
            self._logger.info('No SPE computation requested. Finishing '
                              'successfully')
            self.succeed()


    def _process_spe_job(self, spe_job: GaussianEnergyJob|OrcaEnergyJob):
        '''actual functionality of this step such that child classes can choose
        to override process_spe_job to add additional checks.
        '''
        if spe_job.is_successful:
            db = cast(GeometryDatabase, self.context[self._spe_db_name])

            db.save_energy_result(self._spe_geo_id, lot=spe_job.lot,
                                  energy_result=spe_job.result)

        else:
            self.fail(SpeComputationFailure(failed=spe_job))


    def process_spe_job(self, spe_job: GaussianEnergyJob|OrcaEnergyJob):
        '''store electronic energy in the DB'''
        self._process_spe_job(spe_job)

        if not self.is_failed:
            self.succeed()

@dataclass
class GeometryInvestigationResult(Result):
    geo_id: GeoId
    '''Id of found minimum geometry that was stored in species_db or, if the
    geometry already existed, id of the existing geometry in the db.'''

class GeometryInvestigation(Investigation[GeometryInvestigationResult],
                            ComputeSPEMixin):
    '''
    This investigation tries to optimize a geometry to a local minimum based on
    an initial guess, if the respective conformer is not already in the
    database.
    If requested, it computes a single point energy at a different level of
    theory after the optimization.

    This investigation requires the context to offer a
    :class:`chemtrayzer.core.database.SpeciesDB` with the name "species_db".

    :param initial_guess: initial geometry
    :ivar target: species id of the Species belonging to the initial geometry
    '''

    # this investigation expects the context to provide one species database
    # with the name species_db
    DEPENDENCIES = {
        'species_db': SpeciesDB
    }

    options: Options

    # Freeze this object b/c it will be passed around a lot and potentially
    # used for multiple investigations for which it may be changed slightly,
    # e.g., the spin multiplicity. If it is mutable, you can easily end up with
    # a situation where two investigations share the same options object and
    # one changes it in a way that the other one does not expect.
    @dataclass(frozen=True)
    class Options:
        '''Options object used by those investigations which themselves submit
        species investigations. Their options class could simply inherit from
        this one to have all the necessary field'''

        geo_lot: LevelOfTheory
        '''level of theory for geometry optimization and frequency
        calculation'''
        geo_resources: QmResourceSpec = field(
                                            default_factory=QmResourceSpec)
        """Resources for geometry optimization & frequency calculation"""
        geo_gaussian_options: GaussianOptions = field(
                                default_factory=lambda:GaussianOptions(
                                        opt_options=['tight', 'calcfc']))
        """only relevant if Gaussian is used. Advanced usage only. Impact of
        these options may change between versions of ChemTraYzer"""
        compute_freq: bool = True
        """Whether or not frequencies should be computed for the optimized
        structure.
        """
        energy_lot: LevelOfTheory|None = None
        '''level of theory for additional single point energy calculation. By
        default no additional calculation is performed'''
        energy_resources: QmResourceSpec = field(
                                            default_factory=QmResourceSpec)
        '''resources for single point energy calculation'''
        energy_gaussian_options: GaussianOptions  = field(
                                default_factory=lambda:GaussianOptions())
        """only relevant if Gaussian is used. Advanced usage only. Impact of
        these options may change between versions of ChemTraYzer"""
        db_rmsd_threshold: float = inf
        """RMSD threshold for distinguishing between different conformers when checking the database for existing geometries. [Angstrom]"""
        db_rot_threshold: float = inf
        """Threshold for distinguishing between different conformers when
        checking the database for existing geometries. [percent]"""
        gaussian: Gaussian|None = None
        '''Gaussian program to use'''
        orca: Orca|None = None
        '''Orca program to use'''
        default_software: QMSoftware = QMSoftware.GAUSSIAN
        '''software to use when no program is specified in the level of
        theory'''

        def __post_init__(self):
            if self.geo_lot.software is None:
                # level of theory objects and self are frozen
                object.__setattr__(
                    self,
                    'geo_lot',
                    dataclasses.replace(self.geo_lot,
                                        software=self.default_software))
            if (self.energy_lot is not None
                    and self.energy_lot.software is None):
                object.__setattr__(
                    self,
                    'energy_lot',
                    dataclasses.replace(self.energy_lot,
                                        software=self.default_software))

            if self.db_rmsd_threshold == inf and self.db_rot_threshold == inf:
                logging.warning(
                    'No RMSD or rotation threshold provided. If multiple '
                    'conformers are found in the database, the first one will'
                    ' be used by every GeometryInvestigation, even if they '
                    'have different initial geometries.')

            # check, if the requested software is supported/implemented
            if self.geo_lot.software != QMSoftware.GAUSSIAN:
                raise NotImplementedError('Currently only GAUSSIAN is supported'
                                          ' for geometry optimizations. Set '
                                          'geo_lot.software accordingly.')
            if (self.energy_lot is not None
                    and self.energy_lot.software not in [QMSoftware.GAUSSIAN,
                                                         QMSoftware.ORCA]):
                raise NotImplementedError(
                    'Currently only GAUSSIAN and ORCA are supported for '
                    'geometry optimizations.Set energy_lot.software accordingly.')

            # check if all necessary instances of Program are available
            def is_software_requested(software: QMSoftware) -> bool:
                return (self.geo_lot.software == software
                        or self.energy_lot == software)

            if is_software_requested(QMSoftware.GAUSSIAN):
                if self.gaussian is None:
                    raise ValueError('"gaussian" cannot be None')
            if is_software_requested(QMSoftware.ORCA):
                if self.orca is None:
                    raise ValueError('"orca" cannot be None')

    def __init__(self, *,
                 initial_guess: Geometry,
                 options: Options,
            ) -> None:
        super().__init__()
        self.initial_guess = initial_guess
        self.options = options
        self.initial_species: Species = Species.from_geometry(self.initial_guess)
        '''species object generated from initial_guess'''
        self.target = self.initial_species.id

        # add first step to queue
        self.add_step(self.check_database)

    def _filter_geo_ids(self,
                    geo_ids: Iterable[GeoId],
                    keep_if: Callable[[GeoId], bool],) -> list[GeoId]:
        """filter geo_ids

        Sets self.resut.geo_id to the first element in geo_ids, if no id is
        left after filtering b/c it is assumed that this will be the geometry
        with which we continue.

        :return: all geo_ids where keep_if is True
        """
        assert len(geo_ids) > 0

        keep_ids = [
            geo_id for geo_id in geo_ids
            if keep_if(geo_id)
        ]

        if not keep_ids:
            # simply use the first geometry that is available
            self.result = GeometryInvestigationResult(geo_id = geo_ids[0])

        return keep_ids


    def check_database(self):
        '''check if the given conformer/geometry is already in the database at
        the requested level of theory'''
        db = cast(SpeciesDB, self.context['species_db'])

        # helper functions
        def is_frequency_available(geo_id):
            return self.options.geo_lot in db.list_LOT_of_frequencies(geo_id)

        species = self.initial_species

        # accept all geometries of the species and geo_lot if no MOI threshold
        # was set
        if (self.options.db_rmsd_threshold == inf
                and self.options.db_rot_threshold):
            self._logger.debug('No thresholds provided. All geometries of '
                               '%s are considered to be the same', species)
            criterion = OptimizedAt(self.options.geo_lot)
        else:
            criterion = (OptimizedAt(self.options.geo_lot)
                         & GeometricConformerCriterion(
                                self.initial_guess,
                                rmsd_threshold=self.options.db_rmsd_threshold,
                                rot_threshold=self.options.db_rot_threshold,
                        ))

        same_geos = db.list_geometries(species.id, criterion=criterion)

        if not same_geos:
            self._logger.info('No suitable conformer found for %s at given '
                              'level of theory. Optimizing geometry...',
                               species)
            self.add_step(self.optimize_geometry)
            return
        else:
            self._logger.info('Found %d suitable conformers for %s.',
                              len(same_geos), species)

        if self.options.compute_freq:
            same_geos = self._filter_geo_ids(
                geo_ids=same_geos,
                keep_if=is_frequency_available,
            )

            if not same_geos:
                self._logger.info(
                    'No frequencies available for those conformers. '
                    'Computing frequencies for geometry %d',
                    self.result.geo_id)
                self.add_step(self.compute_freqs)
                return
            else:
                self._logger.info('Frequencies available for %d of those '
                                  'conformers.',
                                  len(same_geos))

        if self.options.energy_lot is not None:
            same_geos = self._filter_geo_ids(
                geo_ids=same_geos,
                keep_if=partial(self._is_energy_at_lot_in_db,
                                energy_lot=self.options.energy_lot),
            )

            if not same_geos:
                self._logger.info(
                    'No electronic energies avaiable at requested level of'
                    ' theory. Computing energy for geometry %d',
                    self.result.geo_id)
                self.add_step(self.compute_spe)
                return
            else:
                self._logger.info('Electronic energy at requested level of '
                                  'theory available for geometry %d. '
                                  'Using this geometry and finishing.',
                                  same_geos[0])

        self.result = GeometryInvestigationResult(
                                            geo_id=same_geos[0])
        self.succeed()


    def optimize_geometry(self):
        '''submit geometry optimization job'''
        opt_job = GaussianOptJob(
                    self.initial_guess,
                    self.options.geo_lot,
                    program=self.options.gaussian,
                    add_opt_options=self.options.geo_gaussian_options
                                                        .opt_options,
                    additional_keywords=self.options.geo_gaussian_options
                                                        .additional_keywords,
                    compute_frequencies=self.options.compute_freq,
                    **self.options.geo_resources.eval(
                                            self.initial_guess.atom_types,
                                            p_type='shared')
                )

        self.add_step(self.process_geo_opt_job)
        self.wait_for_and_submit(opt_job)

    def compute_freqs(self):
        '''submit Gaussian freq job'''
        geo = self.context['species_db'].load_geometry(self.result.geo_id)

        job = GaussianFreqJob(
            geometry=geo,
            lot=self.options.geo_lot,
            program=self.options.gaussian,
            add_opt_options=self.options.geo_gaussian_options
                                                .opt_options,
            additional_keywords=self.options.geo_gaussian_options
                                                .additional_keywords,
            **self.options.geo_resources.eval(
                                    self.initial_guess.atom_types,
                                    p_type='shared')
        )

        self.wait_for_and_submit(job)
        self.add_step(self.process_freq_job)

    def process_freq_job(self, freq_job: GaussianFreqJob):
        '''store frequency information in the database'''
        if freq_job.is_successful:
            db = cast(SpeciesDB, self.context['species_db'])

            db.save_freq_result(geo_id=self.result.geo_id,
                                freq_result=freq_job.success_result,
                                lot=freq_job.lot)
            self._logger.info('Frequencies for geometry %d were store in'
                              ' database.', self.result.geo_id)

            if self.options.energy_lot is not None:
                if self._is_energy_at_lot_in_db(self.result.geo_id,
                                                self.options.energy_lot):
                    self.succeed()
                else:
                    self.add_step(self.compute_spe)
            else:
                self.succeed()
        else:
            self.fail(FrequencyJobFailure(failed=freq_job))

    def process_geo_opt_job(self, geo_job: GaussianOptJob):
        '''check the optimized geometry and store it in the database'''
        if geo_job.is_successful:
            db : SpeciesDB = self.context['species_db']

            optimized = geo_job.success_result.geometries[-1]

            after_opt = Species.from_geometry(optimized)

            geo_id = db.save_opt_result(after_opt.id,
                                    opt_result=geo_job.success_result,
                                    lot=geo_job.lot,
                                    )
            self._logger.info('Geometry for species %s was stored with '
                                'id %s.', after_opt, geo_id)

            self.result = GeometryInvestigationResult(geo_id = geo_id)


            if after_opt is None or self.initial_species == after_opt:
                self.add_step(self.compute_spe)

            else: # optimized to a different species from initial geometry guess
                self.fail(WrongSpeciesFailure(
                    f'Initial geometry belonged to {self.initial_species}.'
                    f'Geometry after optimization is {after_opt}.'))
                # save the geometry anyway but don't compute energy information

        else:
            self.fail(OptimizationJobFailure(failed=geo_job))


    def compute_spe(self):
        self._spe_geo_id = self.result.geo_id
        self._spe_db_name = "species_db"
        return super().compute_spe()