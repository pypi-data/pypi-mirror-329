from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import dataclasses
from math import inf
from typing import TypeVar, cast
from collections.abc import Callable, Iterable

from chemtrayzer.core.chemid import Reaction
from chemtrayzer.core.coords import (
    ConfFilterOptions,
    ConformerEnsemble,
    Geometry,
)
from chemtrayzer.core.database import (
    GeoId,
    GeometryDatabase,
    ReactionDB,
    SpeciesDB,
)
from chemtrayzer.core.lot import (
    LevelOfTheory,
)
from chemtrayzer.core.qm import QmResourceSpec
from chemtrayzer.engine import Investigation, Result
from chemtrayzer.engine.investigation import (
    DependencyFailure,
)
from chemtrayzer.jobs.crest import Crest, CrestJob
from chemtrayzer.qm.species import GeometryInvestigation
from chemtrayzer.qm.ts import TSInvestigation

T = TypeVar('T')
def _default(callable: Callable[..., T], *args, **kwargs) -> T:
    """helper function to avoid creating mutable default values

    will return a field with a default factory that returns the return value of
    callable and passes it the given arguments"""
    return field(default_factory=lambda: callable(*args, **kwargs))

#######################################################
# CREST investigations
#######################################################

@dataclass
class CrestInvestigationResult(Result):
    all_optimized_ids: list[GeoId]
    """ids of all optimized geometries. May contain duplicates and irrelevant
    conformers."""
    ensemble_ids: list[GeoId]
    """ids of those geometries that belong to the filtered ensemble"""

@dataclass(kw_only=True)
class CrestInvestigationOptionsBase:
    '''basic options for CREST investigations'''

    ### CREST stuff ###
    crest_lot: LevelOfTheory
    """level of theory used for CREST calculation"""
    crest_resources: QmResourceSpec
    """computational resources"""
    crest_add_args: list[str] = _default(list)
    """Optional list of additional command-line arguments to pass to
    the CREST executable, e.g., ['--squick','--prop hess']"""
    crest: Crest
    """CREST programm"""

    ### for sorting/filtering conformers ###
    crest_out_filter: ConfFilterOptions = _default(ConfFilterOptions)
    """options for filtering conformers from CREST output"""
    optimized_filter: ConfFilterOptions = _default(ConfFilterOptions,
                                                temperature=2000,
                                                cum_boltzmann_threshold=0.95)
    """options for filtering conformers after optimization; by default 95% most
    important conformers at 2000K are kept
    """

class _CrestInvestigation(Investigation[CrestInvestigationResult], ABC):
    '''Submit a CREST job and analyze its results.

    This Investigations tried to find the conformers of the given geometry
    using Crest

    :param geometry: initial geometry
    :param freeze: list of atom ids in geometry which should be frozen in
                   CREST run.
    '''

    def __init__(self, *,
                 geometry: Geometry,
                 freeze: list[int]|None = None,
                 options: CrestInvestigationOptionsBase,
            ):
        super().__init__()
        self._geometry = geometry
        self._freeze = freeze
        self.options = options

        self.add_step(self.submit_crest)

    def submit_crest(self):
        '''submit the crest job using provided geometry and options'''
        job = CrestJob(
                    geometry=self._geometry,
                    crest=self.options.crest,
                    lot=self.options.crest_lot,
                    addTags=self.options.crest_add_args,
                    atom_list=self._freeze,
                    **self.options.crest_resources.eval(
                                self._geometry.atom_types,
                                'shared'),
                    )
        self.wait_for_and_submit(job)
        self.add_step(self.process_crest_results)

    def process_crest_results(self, crest_job: CrestJob):
        '''check if the Crest job is successful and submit optimization
        investigation'''

        if crest_job.is_successful:
            # TODO use rotamers and do filtering yourself
            ensemble = ConformerEnsemble(
                        geos=crest_job.success_result.conformer_geometries,
                        energies=crest_job.success_result.conformer_energies)
            ensemble.filter(opts=self.options.crest_out_filter, copy=False)

            self._crest_geos = ensemble.geos

            n_crest = len(crest_job.success_result.conformer_geometries)
            n_filtered = ensemble.n_conformers
            self._logger.info('CREST found %d conformers. %d/%d conformers are'
                              ' kept after filtering.', n_crest, n_filtered,
                              n_crest)

            self.add_step(self.submit_refinement_investigaitons)
        else:
            self.fail(DependencyFailure(failed=crest_job))

    def submit_refinement_investigaitons(self):
        """submits one investigation for each geometry in self._crest_geos"""
        for geo in self._crest_geos:
            # child class can implement this method to submit the correct
            # investigation
            invest = self._create_refinement_investigation(
                geo=geo,
                options=self.options,
            )
            # TODO submit investigations without SPE first, then, if SPE was
            #      requested, submit with SPE after filtering duplicates

            self.wait_for_and_submit(invest)

        # clear some memory
        del self._crest_geos

        self.add_step(self.process_refinement_investigaitons)

    @abstractmethod
    def _create_refinement_investigation(self, geo: Geometry, options
                                          ) -> Investigation:
        """create and return the refinement investigations"""

    def process_refinement_investigaitons(self,
                                          *invests: Investigation):
        failed_invests = []
        # two investigations may find the same geometry in the database and
        # thus the same geo_id -> use a set to avoid duplicates
        geo_ids = set()

        for invest in invests:
            if invest.is_successful:
                # the child class will take care of extracting the geo_ids
                geo_ids |= set(self._get_geo_ids_from_result(invest))
            else:
                failed_invests.append(invest)

        self.result = CrestInvestigationResult(all_optimized_ids=list(geo_ids),
                                               ensemble_ids=[])

        if len(failed_invests) == 0:
            self.add_step(self.filter_final_ensemble)
        else:
            self._logger.info(
                'Optimization of CREST output failed for %d/%d structures. '
                'Final ensemble will not be filtered and may be '
                'missing important conformers.', len(failed_invests),
                len(invests))
            failure = DependencyFailure(failed=failed_invests)
            self.fail(failure)

    def filter_final_ensemble(self):
        """remove duplicate and irrelevant conformers"""
        db, e_lot = self._get_geo_db_and_lot()
        geos = []
        energies = []

        # TODO this filtering should happen where the thermochemistry is
        #      computed. Ideally, the conformers for thermochemistry are all
        #      taken from the DB again and filtered so that it does not make a
        #      difference if they were freshly computed or already in the DB
        for geo_id in self.success_result.all_optimized_ids:
            geos.append(db.load_geometry(geo_id))
            energies.append(db.load_electronic_energy(geo_id, e_lot))

        ensemble = ConformerEnsemble(geos, energies)

        ensemble.filter(opts=self.options.optimized_filter, copy=False)

        kept_ids = [geo_id
                    for geo, geo_id in zip(geos,
                                        self.success_result.all_optimized_ids)
                    if geo in ensemble.geos]

        self.result.ensemble_ids = kept_ids

        self._logger.info(
            "Optimized %d geometries. After filtering, the ensemble"
            " contains %d conformers.", len(geos), len(kept_ids)
            )

        self.succeed()


    @abstractmethod
    def _get_geo_ids_from_result(self, invest: Investigation) -> list[GeoId]:
        """extract the geo_ids from the results of the refinement"""

    @abstractmethod
    def _get_geo_db_and_lot(self) -> tuple[GeometryDatabase, LevelOfTheory]:
        """:return: database in which the final geometries are stored, and
                    the level of theory at which energies were computed"""

    def _load_ensemble_from_db(self,
                               geo_ids: Iterable[GeoId]) -> ConformerEnsemble:
        db, e_lot = self._get_geo_db_and_lot()
        geos = []
        energies = []

        for geo_id in geo_ids:
            geos.append(db.load_geometry(geo_id))
            energies.append(db.load_electronic_energy(geo_id, e_lot))

        return ConformerEnsemble(geos, energies)

class CrestTsInvestigation(_CrestInvestigation):
    """Runs CREST on an input geometry, filters the output and submits a
    TSInvestigation for each potential conformer

    :param geometry: known TS geometry
    :param active_atoms: atoms that take part in bond-breaking/-forming. Are
                         frozen in CREST run
    :param reaction: reaction under which to store the optimized TS geometries
    :param options: options
    """

    DEPENDENCIES = {
         'species_db': SpeciesDB,
         'reaction_db': ReactionDB,
    }

    # override some type hints
    options: Options
    _freeze: list[int]

    @dataclass(kw_only=True)
    class Options(CrestInvestigationOptionsBase):

        ts_options: TSInvestigation.Options
        """options for the TS investigations that are submitted for each
        potential conformer.

        .. note::

            This investigation was designed for the case that
            `check_irc = False`. While an IRC check for every potential
            conformer is possible, it is not recomended.
        """

    def __init__(self, *,
                 geometry: Geometry,
                 active_atoms: list[int],
                 reaction: Reaction,
                 options: Options,
            ):
        super().__init__(geometry=geometry, freeze=active_atoms,
                         options=options)

        self.reaction = reaction

    def _create_refinement_investigation(self, geo: Geometry,
                                         options: Options):
        return TSInvestigation(
                initial_guess=geo,
                active_atoms=self._freeze,
                expected_reaction=self.reaction,
                options=options.ts_options,
            )

    def _get_geo_ids_from_result(self, invest: TSInvestigation) -> list[GeoId]:
        return [invest.success_result.ts_id]

    def _get_geo_db_and_lot(self) -> tuple[GeometryDatabase, LevelOfTheory]:
        lot = (self.options.ts_options.energy_lot
               if self.options.ts_options.energy_lot is not None
               else self.options.ts_options.opt_lot)

        return self.context["reaction_db"], lot

class CrestGeometryInvestigation(_CrestInvestigation):
    """Runs CREST on an input geometry, filters the output and submits a
    GeometryInvestigation for each potential conformer

    :param geometry: starting geometry
    :param options: options
    """

    DEPENDENCIES = {
         'species_db': SpeciesDB,
    }

    # override some type hints
    options: Options

    @dataclass(kw_only=True)
    class Options(CrestInvestigationOptionsBase):

        geo_options: GeometryInvestigation.Options
        """options for the TS investigations that are submitted for each
        potential conformer.

        .. note::

            This investigation was designed for the case that
            `check_irc = False`. While an IRC check for every potential
            conformer is possible, it is not recomended.
        """

    def __init__(self, *,
                 geometry: Geometry,
                 options: Options,
            ):
        super().__init__(geometry=geometry, freeze=None,
                         options=options)

    def _create_refinement_investigation(self, geo: Geometry,
                                         options: Options):
        return GeometryInvestigation(
                initial_guess=geo,
                options=options.geo_options,
            )

    def _get_geo_ids_from_result(self,
                                 invest: GeometryInvestigation) -> list[GeoId]:
        return [invest.success_result.geo_id]

    def _get_geo_db_and_lot(self) -> tuple[GeometryDatabase, LevelOfTheory]:
        lot = (self.options.geo_options.energy_lot
               if self.options.geo_options.energy_lot is not None
               else self.options.geo_options.opt_lot)

        return self.context["species_db"], lot


#######################################################
# MultiConformer TS investigation
#######################################################

class ConformerInvestigationFailure(DependencyFailure):
    """Indicates that the conformer optimization failed."""

class PartitionFunctionCalculationFailure(DependencyFailure):
    """Indicates that the partition function calculation failed."""

class TSInvestigationFailure(DependencyFailure):
    """Indicates that the transition state investigation failed."""

@dataclass(kw_only=True)
class MultiConfTsInvestigationResult(Result):

    ts_ids: list[GeoId]
    """optimized transition state conformer geometries"""
    reactant_ids: list[GeoId]
    """optimized reactant conformer geometries"""
    product_ids: list[GeoId]
    """optimized product conformer geometries"""

@dataclass(kw_only=True)
class MultiConfTsInvestigationOptions(TSInvestigation.Options,
                             CrestInvestigationOptionsBase):
    check_irc: bool = True          # override docstring & default value
    '''whether or not to perform an IRC scan for the first TS optimization

    .. note:: The IRC of all subsequent TS optimizations will not be
                checked
    '''
    c_freq: float = 1.0
    '''scaling factor for the frequencies'''

class MultiConfTsInvesitgation(Investigation[MultiConfTsInvestigationResult]):
    """
    Investigation that checks, optimizes, and analyzes both transition states
    and stable geometries, performing necessary validations and multiconformer
    searches with thorough database interactions.
    """

    DEPENDENCIES = {
        'reaction_db': ReactionDB,
        'species_db': SpeciesDB
    }


    def __init__(self,
                 initial_ts_guess: Geometry,
                 active_atoms: Iterable[int],
                 expected_reaction: Reaction|None,
                 options:MultiConfTsInvestigationOptions,
                ):
        super().__init__()
        self.initial_ts_guess = initial_ts_guess
        self.active_atoms = list(active_atoms)
        self.expected_reaction = expected_reaction
        self.options = options

        self.add_step(self.optimize_ts)

    def optimize_ts(self):
        """submit TS investigation"""
        # TODO: these thresholds are also used for the preoptimization of IRC
        #       endpoints where VdW complexes are not yet split into fragments
        #       -> Once we check for VdW complexes in the reaction path, we
        #       actually want to apply thresholds for the DB check in the
        #       preoptimization or even remove the DB check entirely
        # Do not check the database for specific conformers of the IRC
        # endpoints as we will later perform a conformer search on the
        # optimized endpoints anyway.
        opts = dataclasses.replace(self.options,
                                   db_rmsd_threshold=inf,
                                   db_rot_threshold=inf,
                )

        ts_invest = TSInvestigation(
            initial_guess=self.initial_ts_guess,
            active_atoms=self.active_atoms,
            expected_reaction=self.expected_reaction,
            options=opts,
        )

        self.add_step(self.submit_conformer_invest)
        self.wait_for_and_submit(ts_invest)

    def submit_conformer_invest(self, ts_invest: TSInvestigation):
        """submits a CREST investigation
        """
        if ts_invest.is_successful:
            # TODO if only WrongReactionFailure -> get correct active atoms and
            #       proceed, if reaction is still relevant
            db = cast(ReactionDB, self.context['reaction_db'])
            ts_geo = db.load_geometry(ts_invest.success_result.ts_id)

            # since our Options class inherits from TSInvestigaiton options,
            # we can simply copy all fields
            ts_opts = TSInvestigation.Options(
                **{field.name: getattr(self.options, field.name)
                   for field in dataclasses.fields(TSInvestigation.Options)})
            # we don't want to check the IRC for the conformer optimizations
            ts_opts.check_irc = False
            opts = CrestTsInvestigation.Options(
                ts_options=ts_opts,
                **{field.name: getattr(self.options, field.name)
                   for field in dataclasses.fields(
                                                CrestInvestigationOptionsBase)}
            )

            ts_conformer_investigation = CrestTsInvestigation(
                geometry=ts_geo,
                active_atoms=self.active_atoms,
                reaction=ts_invest.success_result.reaction,
                options=opts,
            )

            self.add_step(self.process_conformer_invests)
            self.wait_for_and_submit(ts_conformer_investigation)

            if ts_invest.options.check_irc:
                db = cast(SpeciesDB, self.context['species_db'])

                self._n_reactants = len(ts_invest.success_result.reactant_ids)
                # first submit reactants, then products
                geo_ids = (ts_invest.success_result.reactant_ids
                           + ts_invest.success_result.product_ids)
                for geo_id in geo_ids:
                    geo = db.load_geometry(geo_id)

                    # the IRC check may have chosen a different spin
                    #  multiplicity for bimolecular reactions
                    geo_lot = db.load_LOT_of_geometry(geo_id)
                    m = geo_lot.el_struc.multiplicity

                    geo_lot = dataclasses.replace(
                                    self.options.opt_lot,
                                    el_struc=dataclasses.replace(
                                                self.options.opt_lot.el_struc,
                                                multiplicity=m)
                                )
                    if self.options.energy_lot is not None:
                        energy_lot = dataclasses.replace(
                                        self.options.energy_lot,
                                        el_struc=dataclasses.replace(
                                            self.options.energy_lot.el_struc,
                                            multiplicity=m)
                                    )
                    else:
                        energy_lot = None

                    opts = CrestGeometryInvestigation.Options(
                            geo_options=GeometryInvestigation.Options(
                                # geo_lot and opt_lot have different names
                                # -> need to copy the fields manually
                                geo_lot=geo_lot,
                                geo_resources=self.options.opt_resources,
                                geo_gaussian_options=self.options
                                                        .opt_gaussian_options,
                                energy_lot=energy_lot,
                                energy_resources=self.options.energy_resources,
                                energy_gaussian_options=self.options
                                                      .energy_gaussian_options,
                                db_rmsd_threshold=self
                                                    .options.db_rmsd_threshold,
                                db_rot_threshold=self.options.db_rot_threshold,
                                gaussian=self.options.gaussian,
                                orca=self.options.orca,
                                default_software=self.options.default_software,
                            ),
                            **{field.name: getattr(self.options, field.name)
                            for field in dataclasses.fields(
                                                    CrestInvestigationOptionsBase)}
                        )


                    inves = CrestGeometryInvestigation(
                        geometry=geo,
                        options=opts,
                    )
                    self.wait_for_and_submit(inves)

        else:
            self.fail(TSInvestigationFailure(failed=ts_invest))

    def process_conformer_invests(self, ts_invest: CrestTsInvestigation,
                                  *geo_invests: CrestGeometryInvestigation):
        """
        Process the results of the TS conformer investigations and calculate
        RRHO partition functions.
        """
        failed = [invest
                  for invest in [ts_invest, *geo_invests]
                  if invest.is_failed]

        # TODO implememnt check based on imanginary normal modes to check
        #      those TS for which we did not check the IRC

        if failed:
            if ts_invest.is_failed:
                self._logger.info('Determination of TS conformers failed.')

            self.fail(DependencyFailure(failed=failed))
        else:
            react_ids = [react_invest.success_result.all_optimized_ids
                        for react_invest in geo_invests[:self._n_reactants]]
            prod_ids = [prod_invest.success_result.all_optimized_ids
                        for prod_invest in geo_invests[self._n_reactants:]]

            self.result = MultiConfTsInvestigationResult(
                ts_ids=ts_invest.success_result.all_optimized_ids,
                reactant_ids=react_ids,
                product_ids=prod_ids,
            )
            self.succeed()


