# ruff: noqa
'''Investigations dealing with transition state (TS) searching and confirmation.
'''
from __future__ import annotations
import dataclasses
from math import inf
import pathlib
from dataclasses import dataclass, field, fields
from numbers import Number
from typing import Iterable, Union, cast, overload
from chemtrayzer.core.qm import MaxIterationsReached, QmResourceSpec, IRCResult, lowest_multiplicity
from chemtrayzer.engine import Result
import numpy as np

from chemtrayzer.core.chemid import Reaction, Species
from chemtrayzer.core.constants import R, k_B, h
from chemtrayzer.core.coords import ChainOfStates, ConfDiffOptions, Geometry
from chemtrayzer.core.database import GeoId, ReactionDB, SpeciesDB
from chemtrayzer.core.kinetics import ReactionRate
from chemtrayzer.core.lot import LevelOfTheory, QMSoftware
from chemtrayzer.core.thermo import ThermoModel
from chemtrayzer.core.periodic_table import PERIODIC_TABLE as PTOE
from chemtrayzer.qm.species import ComputeSPEMixin, OptimizationJobFailure
from chemtrayzer.engine.investigation import (
    DependencyFailure,
    Investigation,
    InvestigationContext,
    Failure
)
from chemtrayzer.jobs.gaussian import (
    Gaussian,
    GaussianIRCJob,
    GaussianOptJob,
    GaussianOptions,
    GaussianTSOptJob,
    IRCDirection
)
from chemtrayzer.jobs.orca import Orca
from chemtrayzer.qm.species import GeometryInvestigation


class IrcInvesFailure(DependencyFailure):
    '''indicates that the IRC scan failed for a reason that is not that the
    expected reaction was not found

    :param investigaitons: failed IRC investigation'''

class PreOptimizationFailure(DependencyFailure):
    '''indicates that the preoptimization of the TS failed

    :param failed: failed optimization job'''

class WrongReactionFailure(Failure):
    '''indicates that the IRC scan found a different reaction than expected'''

class NotAReactionFailure(Failure):
    '''indicates that prodcuts == reactants, i.e., the identified TS does not
    belong to a reaction'''

class IRCJobFailure(DependencyFailure):
    '''indicates that an IRC computation failed

    :param failed: IRC job'''

class TsOptimizationFailure(DependencyFailure):
    '''indicates that the TS optimization failed

    :param failed: TS optimization job'''

@dataclass
class TSInvestigationResult(Result):
    ts_id: GeoId
    '''id of the transition state geometry that was saved in reaction_db'''
    reaction: Reaction
    '''reaction that the transition state belongs to. In case of failure,
    this is not necessarily the expected reaction and is determined via an
    IRC scan. If no IRC check was requested and the TS could be optimized,
    this is always the expected reaction.'''
    reactant_ids: list[GeoId]|None = None
    '''list of geometry IDs corresponding to all optimized irc endpoint geometries
    from the IRC scan'''
    product_ids: list[GeoId]|None = None
    '''list of geometry IDs corresponding to the optimized product geometries
            from the IRC scan'''


def _default_gaussian_opts(**kwargs):
    """helper function to avoid creating mutable default values"""
    return field(default_factory=lambda: GaussianOptions(**kwargs))

class TSInvestigation(Investigation[TSInvestigationResult],
                      ComputeSPEMixin):
    '''
    This investigation tries to find a TS geometry from an initial guess.
    First, the active atoms are frozen and the rest of the geometry is
    optimized. Then, a transition state optimization is performed which is
    confirmed via an IRC scan. Finally, a GeometryInvestigation is submitted
    for each product and reactant.

    The computed data (geometries, energies, etc.) are written to databases.


    :param initial_guess: geometry close to expected TS
    :param active_atoms: ids of atoms involved in broken or formed bonds
                        (frozen during preoptimization)
    options: options
    expected_reaction: reaction that the TS probably belongs to
                       If IRC check is requested, the investigation fails with
                       a WrongReactionFailure, if the reaction is not
                       compatible with the IRC endpoints.
                       If no IRC check is requested, this is a required
                       argument and the **optimized TS will be stored in the DB
                       as belonging to that reaction!**
    '''

    DEPENDENCIES = {
        'reaction_db': ReactionDB,
        'species_db': SpeciesDB}

    options: Options

    @dataclass(kw_only=True)
    class Options:
        '''options for TSInvestigation'''

        ### preoptimization ###
        preopt_lot: LevelOfTheory
        """level of theory for the constrained preoptimization of TS and
        preoptimization of IRC endpoints"""
        preopt_resources: QmResourceSpec
        """computational resources required for preoptimization"""
        preopt_gaussian_options: GaussianOptions = field(
                                            default_factory=GaussianOptions)
        """"only relevant if Gaussian is used. Advanced usage only. Impact of
        these options may change between versions of ChemTraYzer
        """

        ### optimization ###
        opt_lot: LevelOfTheory
        """level of theory for the TS optimization, IRC scan and endpoint optimization
        """
        opt_resources: QmResourceSpec
        """computational resources required for TS optimization, IRC scan and endpoint optimization"""
        opt_gaussian_options: GaussianOptions = _default_gaussian_opts(
                            opt_options=['maxcyc=200', 'tight', 'noeigen'],
                            additional_keywords='int=(ultrafine) scf=(xqc)')
        """only relevant if Gaussian is used. Advanced usage only. Impact of
        these options may change between versions of ChemTraYzer"""

        ### single point energy calculation ###
        energy_lot: LevelOfTheory|None = None
        """level of theory for the single point energy calculation. If None, no
        single point energy calculation is performed"""
        energy_resources: QmResourceSpec = field(
                                            default_factory=QmResourceSpec)
        """computational resources required for the single point energy
        calculation"""
        energy_gaussian_options: GaussianOptions = _default_gaussian_opts(
                            additional_keywords='int=(ultrafine)')
        """only relevant if Gaussian is used. Advanced usage only. Impact of
        these options may change between versions of ChemTraYzer"""

        ### software settings ###
        orca: Orca|None = None
        '''Orca program to use'''
        gaussian: Gaussian
        '''Gaussian program to use'''
        default_software: QMSoftware = QMSoftware.GAUSSIAN
        '''software to use when no program is specified in the level of
        theory'''

        ### other ###
        db_rmsd_threshold: float = inf
        """RMSD threshold for distinguishing between different conformers when checking the database for existing geometries. [Angstrom]"""
        db_rot_threshold: float = inf
        """Threshold for distinguishing between different conformers when
        checking the database for existing geometries. [percent]"""
        check_irc: bool = False
        '''whether or not to perform an IRC scan'''
        irc_steps_max: int = 20
        '''maximum number of steps for the IRC scan per direaction'''

    def __init__(
            self, *,
            initial_guess: Geometry,
            active_atoms: Iterable[int],
            options: Options,
            expected_reaction: Reaction|None = None,
    ):
        super().__init__()

        if expected_reaction is None and not options.check_irc:
            raise ValueError('If no IRC check is requested, an expected '
                             'reaction must be supplied. Otherwise, the TS '
                             'cannot be stored in the database')

        self.initial_guess = initial_guess
        self.options = options
        self.expected_reaction = expected_reaction
        self.active_atoms = active_atoms
        self._ts_job_id = None  # id of TS job
        self._irc_check_id = None

        self.add_step(self.submit_preoptimization)


    def submit_preoptimization(self):
        job = GaussianOptJob(
                geometry=self.initial_guess,
                lot=self.options.preopt_lot,
                freeze=self.active_atoms,
                compute_frequencies=False,
                program=self.options.gaussian,
                add_opt_options=self.options.preopt_gaussian_options
                                                .opt_options,
                additional_keywords=self.options.preopt_gaussian_options
                                                 .additional_keywords,
                **self.options.preopt_resources.eval(
                                            self.initial_guess.atom_types))

        self.add_step(self.submit_ts_job)
        self.wait_for_and_submit(job)

    def submit_ts_job(self, preopt: GaussianOptJob):
        if preopt.is_successful:
            ts_guess = preopt.success_result.geometries[-1]

            ts_job = GaussianTSOptJob(
                    geometry=ts_guess,
                    lot=self.options.opt_lot,
                    compute_frequencies=True,
                    program=self.options.gaussian,
                    add_opt_options=self.options.opt_gaussian_options
                                                    .opt_options,
                    additional_keywords=self.options.opt_gaussian_options
                                                        .additional_keywords,
                    **self.options.opt_resources.eval(ts_guess.atom_types))

            self.add_step(self.process_ts_job)
            self.wait_for_and_submit(ts_job)
        else:
            self.fail(PreOptimizationFailure(failed=preopt))

    def process_ts_job(self, ts_job: GaussianOptJob):
        if ts_job.is_successful:

            # save to retrieve data later
            self._ts_job_id = cast(int, ts_job.id)

            if self.options.check_irc:
                # all IRCInvestigation options are also TSInvestigation options
                opts = IRCInvestigation.Options(
                    **{field.name: getattr(self.options, field.name)
                       for field in fields(IRCInvestigation.Options)}
                )
                irc_check = IRCInvestigation(
                                ts_job_id=self._ts_job_id,
                                expected_reaction=self.expected_reaction,
                                options=opts)

                self.add_step(self.process_irc_result)
                self._irc_check_id = self.wait_for_and_submit(irc_check)

            else:
                # already checked in __init__ that expected_reaction is given
                ts_id = self._save_ts_to_db(self.expected_reaction)
                self.result = TSInvestigationResult(
                    ts_id = ts_id,
                    reaction = self.expected_reaction,
                )
                if self.options.energy_lot is not None:
                    self.add_step(self.compute_spe)
                else:
                    self.succeed()
        else:
            # TODO try another strategy
            self.fail(TsOptimizationFailure(failed=ts_job))

    def process_irc_result(self, irc_check: IRCInvestigation):
        if (irc_check.is_successful
            or isinstance(irc_check.failed_result.reason,
                          WrongReactionFailure)):

            ts_id = self._save_ts_to_db(irc_check.success_result.reaction)

            self.result = TSInvestigationResult(
                ts_id = ts_id,
                reaction = irc_check.success_result.reaction,
                reactant_ids = irc_check.success_result.reactant_ids,
                product_ids = irc_check.success_result.product_ids,
            )

            if self.options.energy_lot is None:
                if irc_check.is_successful:
                    self.succeed()
                else:
                    self.fail(WrongReactionFailure(
                        f"expected reaction: {self.expected_reaction}\n"
                        "actual reaction (based on IRC check): "
                        f"{self.success_result.reaction}"))

            else:
                self.add_step(self.compute_spe)

        else:
            # TODO reevaluate the inital data and try another strategy
            self._logger.debug('A transition state was found (Job %d),'
                               ' but it could not be confirmed because the IRC'
                               ' scan (Invesitgation %d) failed.',
                               self._ts_job_id, irc_check.id)
            self.fail(IrcInvesFailure(failed=irc_check))

    def _save_ts_to_db(self, reaction: Reaction) -> GeoId:
        """helper function to store TS in DB as belonging to `reaction`"""
        # store TS to DB
        reaction_db = cast(ReactionDB, self.context['reaction_db'])

        ts_job = cast(GaussianOptJob,
                      self.context.jobsystem.get_job_by_id(self._ts_job_id))

        if reaction.id not in reaction_db.list_reactions():
            reaction_db.save_reaction(reaction)

        ts_id = reaction_db.save_ts_opt_result(reaction.id,
                                              opt_result=ts_job.success_result,
                                              lot=ts_job.lot)

        self._logger.debug('Saved TS for reaction %s in database with id %d.',
                           reaction.id, ts_id)

        return ts_id

    def compute_spe(self):
        self._spe_geo_id = self.success_result.ts_id
        self._spe_db_name = "reaction_db"
        super().compute_spe()

    def process_spe_job(self, spe_job):
        '''store electronic energy in the DB'''
        self._process_spe_job(spe_job)

        if not self.is_failed:
            if self._irc_check_id is not None:
                irc_check = self.context.inves_mgr.get_investigation_by_id(
                                                            self._irc_check_id)
                if isinstance(irc_check.result.reason, WrongReactionFailure):
                    self.fail(WrongReactionFailure(
                        f"expected reaction: {self.expected_reaction}\n"
                        "actual reaction (based on IRC check): "
                        f"{self.success_result.reaction}"))
                    return

            self.succeed()


@dataclass(kw_only=True)
class IRCInvestigationResult(IRCResult, Result):
    """Result of an IRCInvestigation"""
    reaction: Reaction
    product_ids: list[GeoId]
    reactant_ids: list[GeoId]

class IRCInvestigation(Investigation[IRCInvestigationResult]):
    """Perform IRC check on a Gaussian TS optimization job.

    :param ts_job_id: id of the TS optimization job
    :param expected_reaction: expected reaction to compare IRC endpoints to
    :param options: options for the investigation
    """

    DEPENDENCIES = {
        'reaction_db': ReactionDB,
        'species_db': SpeciesDB}

    @dataclass(kw_only=True)
    class Options:
        '''options for IRCInvestigation'''

        ### IRC settings ###
        irc_steps_max: int = 20
        '''maximum number of steps for the IRC scan'''

        ### preoptimization ###
        preopt_lot: LevelOfTheory
        """level of theory for the constrained preoptimization"""
        preopt_resources: QmResourceSpec
        """computational resources required for constrained preoptimization"""
        preopt_gaussian_options: GaussianOptions = field(
                                            default_factory=GaussianOptions)
        """"only relevant if Gaussian is used. Advanced usage only. Impact of
        these options may change between versions of ChemTraYzer
        """

        ### optimization ###
        opt_lot: LevelOfTheory
        """level of theory for the IRC scan and endpoint optimization
        """
        opt_resources: QmResourceSpec
        """computational resources required for the IRC scan and endpoint optimization"""
        opt_gaussian_options: GaussianOptions = _default_gaussian_opts(
                            opt_options=['maxcyc=200', 'tight', 'noeigen'],
                            additional_keywords='int=(ultrafine) scf=(xqc)')
        """only relevant if Gaussian is used. Advanced usage only. Impact of
        these options may change between versions of ChemTraYzer"""

        ### single point energy calculation ###
        energy_lot: LevelOfTheory|None = None
        """level of theory for the single point energy calculation. If None, no
        single point energy calculation is performed"""
        energy_resources: QmResourceSpec = field(
                                    default_factory=lambda:QmResourceSpec())
        """computational resources required for the single point energy
        calculation"""
        energy_gaussian_options: GaussianOptions  = _default_gaussian_opts(
                            additional_keywords='int=(ultrafine)')
        """only relevant if Gaussian is used. Advanced usage only. Impact of
        these options may change between versions of ChemTraYzer"""

        ### software settings ###
        gaussian: Gaussian
        '''Gaussian program to use'''
        orca: Orca|None = None
        """Orca program to use"""
        default_software: QMSoftware = QMSoftware.GAUSSIAN
        '''software to use when no program is specified in the level of
        theory'''

        ### other ###
        db_rmsd_threshold: float = inf
        """RMSD threshold for distinguishing between different conformers when checking the database for existing geometries. [Angstrom]"""
        db_rot_threshold: float = inf
        """Threshold for distinguishing between different conformers when
        checking the database for existing geometries. [percent]"""


    def __init__(self, *,
                 ts_job_id: int,
                 expected_reaction: Reaction|None = None,
                 options: Options,
                 ):
        super().__init__()

        self.ts_job_id = ts_job_id
        self.expected_reaction = expected_reaction
        self.options = options

        self.irc_jobs = []
        self.opt_jobs = []
        self.add_step(self.follow_IRC)

    def _get_ts_job(self) -> GaussianTSOptJob:
        """helper fucntion to get TS Job from jobsystem"""
        ts_job = self.context.jobsystem.get_job_by_id(self.ts_job_id)

        # raise an exception instead of setting the job state to failed, b/c
        # this is a programming error and really should not happen
        if not isinstance(ts_job, GaussianTSOptJob):
            raise ValueError('ts_job_id must belong to a GaussianTSOptJob.')
        if not ts_job.is_successful:
            raise ValueError('Cannot perform IRC scan, because TS '
                             'optimization failed.')

        return ts_job

    def _submit_IRC_scan(self, dir: IRCDirection, geo: Geometry,
                         old_chk_file) -> int:
        """helper function to create ans submit IRC job"""

        irc_job = GaussianIRCJob(
                        lot=self.options.opt_lot,
                        program=self.options.gaussian,
                        n_steps=self.options.irc_steps_max,
                        direction=dir,
                        geometry=geo,
                        get_freqs_from_chk=old_chk_file is not None,
                        old_chk_file=old_chk_file,
                        add_opt_options=self.options
                                .opt_gaussian_options.irc_options,
                        additional_keywords=self.options
                                .opt_gaussian_options.additional_keywords,
                        **self.options.opt_resources.eval(geo.atom_types))

        id = self.wait_for_and_submit(irc_job)

        self.irc_jobs.append(id)

        return id

    def follow_IRC(self):
        ts_job = self._get_ts_job()

        # if frequency information for the TS was computed, the Hessian can be
        # used by the IRC scan
        if ts_job.compute_frequencies:
            chk_file = pathlib.Path(self.context.jobsystem.get_job_dir(
                self.ts_job_id)) / ts_job.CHK_FILE
        else:
            chk_file = None

        ts_geo = ts_job.success_result.geometries[-1]
        self.add_step(self.optimize_geometry)
        self._submit_IRC_scan(IRCDirection.Forward, ts_geo, chk_file)
        self._submit_IRC_scan(IRCDirection.Reverse, ts_geo, chk_file)

    def optimize_geometry(self, forward_job: GaussianIRCJob,
                          reverse_job: GaussianIRCJob):
        """optimize the endpoint geometries of the IRC scan without a separate
        SPE calculation"""
        irc_jobs = (forward_job, reverse_job)

        # check for job failure
        failed_jobs = [job
                       for job in irc_jobs
                       if not job.is_successful]

        if failed_jobs:
            # TODO try alternative strategy, e.g. adjust step size
            self.fail(IRCJobFailure(failed=failed_jobs))
        else:  # everything successful
            for irc_job in irc_jobs:
                opts = GeometryInvestigation.Options(
                    geo_lot=self.options.preopt_lot,
                    geo_resources=self.options.preopt_resources,
                    geo_gaussian_options=self.options.preopt_gaussian_options,
                    # No SPE calculation at first!
                    energy_lot=None,
                    db_rmsd_threshold=self.options.db_rmsd_threshold,
                    db_rot_threshold=self.options.db_rot_threshold,
                    gaussian=self.options.gaussian,
                    orca=self.options.orca,
                    default_software=self.options.default_software,
                    compute_freq=False,
                )
                inves = GeometryInvestigation(
                    initial_guess=irc_job.success_result.endpoint_geometry,
                    options=opts)

                self.wait_for_and_submit(inves)

            self.add_step(self.process_first_geo_inves)

    def _extract_fragments_from_investigation(self,
            inves: GeometryInvestigation) -> dict[Species, Geometry]|None:
        """helper function to get the geometry and species from the furhter optimized endpoints.

        If the optimization failed due to reaching the maximum number of
        iterations and the last geometry consists of more than one fragment,
        e.g., is a bimolecular well, the geometries of the last iteration step
        are extracted and returned.

        :return: dictionary of fragment geometries of endpoint or None,
                 if no geometries could be extracted
        """

        if inves.is_successful:
            db = cast(SpeciesDB, self.context['species_db'])

            well_geos = db.load_geometry(inves.success_result.geo_id
                                         ).split_fragments()
            return {Species.from_geometry(geo): geo
                                for geo in well_geos}
        elif isinstance(inves.failed_result.reason, OptimizationJobFailure):
            if isinstance(inves.failed_result.reason.causes[0],
                          MaxIterationsReached):
                _, job_id = inves.failed_result.reason.failed_ids[0]
                opt_job = self.context.jobsystem.get_job_by_id(job_id)


                if hasattr(opt_job.result, 'geometries'):
                    last_geo = cast(Geometry, opt_job.result.geometries[-1])

                    well_geos = last_geo.split_fragments()

                    if len(well_geos) > 1:
                        self._logger.info(
                            'IRC endpoint optimization reached the maximum '
                            'number of iterations. The last geometry consists '
                            'of multiple fragments. Continuing with the last '
                            'geometry and optimizing fragments separately.')
                        return {Species.from_geometry(geo): geo
                                for geo in well_geos}

        return None

    def process_first_geo_inves(self, forward_inves: GeometryInvestigation,
                            reverse_inves: GeometryInvestigation):
        """process the first two GeometryInvestigations of the IRC scan"""
        failed = []

        # get (partially) optimized endpoint geometry (fragments), even if the
        # optimization reached the maximum number of iterations
        self._forward_geos = self._extract_fragments_from_investigation(
                                    forward_inves)
        self._reverse_geos = self._extract_fragments_from_investigation(
                                    reverse_inves)

        if self._forward_geos is None:
            failed.append(forward_inves)
        if self._reverse_geos is None:
            failed.append(reverse_inves)

        if failed:
            self.fail(DependencyFailure(
                        msg="IRC endpoints could not be optimized.",
                        failed=failed))
        else:
            self.add_step(self.check_reaction)

    def check_reaction(self):
        reaction = Reaction(
            products=self._reverse_geos.keys(),
            reactants=self._forward_geos.keys())

        # TODO check CRG for changed bonds instead -> H2O + OH <=> OH + H2O
        #       currently also raises NotAReactionFailure
        # compare the products and reactants in reaction object b/c
        # they are sorted canonically
        if reaction.reactants == reaction.products:
            self.fail(NotAReactionFailure(
                            'TS does not belong to a reaction'))
        else:
            if (self.expected_reaction is not None
                    and self.expected_reaction == reaction):
                self._reactant_geos = self._forward_geos
                self._product_geos = self._reverse_geos
            elif (self.expected_reaction is not None
                    and self.expected_reaction == reaction.reverse()):
                self._reactant_geos = self._reverse_geos
                self._product_geos = self._forward_geos
                reaction = reaction.reverse()
            else:   # either no expected reaction, or different reaction
                    # found -> arbitrary assignment
                self._reactant_geos = self._forward_geos
                self._product_geos = self._reverse_geos

            self.result = IRCInvestigationResult(
                                reactant_ids=[],
                                product_ids=[],
                                reaction=reaction)

            self.add_step(self.optimize_fragments)

        del self._forward_geos
        del self._reverse_geos

    def optimize_fragments(self):
        # iterate over reactants first, then products -> important later
        for geos_dicts in [self._reactant_geos, self._product_geos]:
            for species, geo in geos_dicts.items():
                # if the reaction is bimolecular, we cannot use the total
                # spin multiplicity for each fragment
                if len(geos_dicts)>1:
                    new_spin_mult = lowest_multiplicity(
                                [PTOE[elem]
                                for elem, count in species.composition.items()
                                for _ in range(count)])
                    opt_lot = _change_spin(self.options.opt_lot,
                                            new_spin_mult)
                    energy_lot = _change_spin(self.options.energy_lot,
                                                new_spin_mult)
                else:
                    opt_lot = self.options.opt_lot
                    energy_lot = self.options.energy_lot

                # This time, we also want to compute the SPE
                # For unimolecular reactions where no SPE is requested, the
                # GeometryInvestigation will simply find the already
                # optimized endpoint geometries in the database and return
                # those
                opts = GeometryInvestigation.Options(
                    geo_lot=opt_lot,
                    geo_resources=self.options.opt_resources,
                    geo_gaussian_options=self.options.opt_gaussian_options,
                    energy_lot=energy_lot,
                    energy_resources=self.options.energy_resources,
                    energy_gaussian_options=self.options
                                                .energy_gaussian_options,
                    db_rmsd_threshold=self.options.db_rmsd_threshold,
                    db_rot_threshold=self.options.db_rot_threshold,
                    gaussian=self.options.gaussian,
                    orca=self.options.orca,
                    default_software=self.options.default_software,
                )
                inves = GeometryInvestigation(initial_guess=geo,
                                                options=opts)
                self.wait_for_and_submit(inves)

        # geometries already in DB -> no need to store
        del self._product_geos
        del self._reactant_geos

        self.add_step(self.process_second_geo_inves)

    def process_second_geo_inves(self, *invests: GeometryInvestigation):
        """process the second two GeometryInvestigations of the IRC scan"""
        failed = [inves for inves in invests if inves.is_failed]

        if not failed:
            n_reactants = len(self.success_result.reaction.reactants)

            for invest in invests[:n_reactants]:
                self.success_result.reactant_ids.append(
                                    invest.success_result.geo_id)
            for invest in invests[n_reactants:]:
                self.success_result.product_ids.append(
                                    invest.success_result.geo_id)

            actual_reaction = self.success_result.reaction

            if (self.expected_reaction is None or
                    self.expected_reaction == actual_reaction):
                self.succeed()
            else:
                self.fail(WrongReactionFailure('IRC scan found a different '
                                               'reaction than expected.'))
        else:
            self.fail(DependencyFailure(
                msg="Final endpoint optimization and SPE calculation failed",
                failed=failed))

class NEBTSInvestigation(Investigation):
    '''
    Investigation to find the transition state of a reaction using the nudged elastic band method.
    :param initial_cos: ChainOfStates object containing the initial reaction path.
    :type initial_cos: ChainOfStates
    :param lot: LevelOfTheory object containing the level of theory information.
    :type lot: LevelOfTheory
    '''

    @dataclass
    class Result(Investigation.Result):
        energy: float = None
        ts: Geometry = None
        mep: ChainOfStates = None

    def __init__(self, *, initial_cos: ChainOfStates,
                 lot: LevelOfTheory,
                 context: InvestigationContext,
                 orca: Orca = None,
                 ) -> None:
        super().__init__(context)

        self.initial_cos = initial_cos
        self.orca = orca
        self.lot = lot
        self.result = NEBTSInvestigation.Result()

        self.add_step(self.submit_orca_job)

    def submit_orca_job(self):
        nebts_job = OrcaNEBTSJob(self.initial_cos, program=self.orca, lot=self.lot)

        self.wait_for_and_submit(nebts_job)
        self.add_step(self.harvest_result)

    def harvest_result(self, nebts_job):
        self.result.energy = nebts_job.result['energy']
        self.result.ts = nebts_job.result['ts']
        self.result.mep = nebts_job.result['mep']
        self.succeed()
        self._logger.debug('NEBTS investigation successfully finished.')


class TstRate(ReactionRate):
    '''reaction rate from transition state theory (TST) for an ideal gas.


    :param reactants: thermodynamic data for all reactants
    :param ts: thermodynamic data for the activated complex (excluding the mode
               along the IRC)
    '''

    def __init__(self, reactants: Iterable[ThermoModel], ts: ThermoModel,
                 p_ref = 1e5) \
            -> None:
        super().__init__()

        self.reactants = reactants
        self.ts = ts
        self.p_ref = p_ref

    def k(self, T: Union[Number, np.ndarray]) -> Union[Number, np.ndarray]:
        '''compute kinetic rate constant

        :param T: temperature [K]
        :return: rate constant [cm^3n mol^n s^-1]
                 where n is the number of reactants minus one
                 returns an array, iff the input is an array
        '''
        n_reactants = len(self.reactants)

        # scalar inner function is called in a loop if input is vectorized
        def _k(T: Number) -> Number:
            G_reactants = 0
            for r in self.reactants:
                G_reactants += r.G(T=T, p=self.p_ref)

            G_ts = self.ts.G(T=T, p=self.p_ref)

            dG_ts = G_ts - G_reactants

            # here, we assume an ideal gas
            c_0 = self.p_ref/(R*T) * 1e-6 # [mol cm^-3]

            return k_B*T/h/c_0**(n_reactants-1)*np.exp(-dG_ts/(R*T))


        if np.isscalar(T):
            return _k(T)
        else:
            return np.array([_k(t) for t in T])

@overload
def _change_spin(lot: LevelOfTheory, mult: int) -> LevelOfTheory:
    ...

@overload
def _change_spin(lot: None, mult: int) -> None:
    ...

def _change_spin(lot, mult: int):
    '''change the spin multiplicity of the electronic structure properties'''
    if lot is None:
        return None
    el_struc = lot.el_struc
    return dataclasses.replace(lot,
                               el_struc=dataclasses.replace(el_struc,
                                                            multiplicity=mult))
