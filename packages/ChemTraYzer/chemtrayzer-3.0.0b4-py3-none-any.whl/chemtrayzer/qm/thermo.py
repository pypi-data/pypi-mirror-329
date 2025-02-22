"""Thermochemistry from quantum qechanics.

This module contains the machinery to compute thermochemical properties from
quantum mechanical data
"""
# ruff: noqa
import dataclasses
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from dataclasses import dataclass, field
from math import inf
from typing import Generic, Iterable, Mapping, Type, TypeVar

import numpy as np
from numpy.typing import ArrayLike

from chemtrayzer.core.chemid import Species
from chemtrayzer.core.constants import N_A, R, amu, c_0, h, E_h_p_particle, k_B, rbohr
from chemtrayzer.core.coords import Geometry
from chemtrayzer.core.database import OnlyLowestEnergy, OptimizedAt, SpeciesDB
from chemtrayzer.core.lot import ElectronicStructureProperties, LevelOfTheory
from chemtrayzer.core.thermo import DerivedFromNpTEnsemble, ThermoModel
from chemtrayzer.engine.investigation import DependencyFailure, Investigation, Failure
from chemtrayzer.qm.species import GeometryInvestigation


class RRHO(DerivedFromNpTEnsemble):
    r'''
    ideal gas rigid-rotor harmonic oscillator model for a single molecular
    geometry

    several thermodynamic quantities can be computed by supplying the pressure
    in Pa and the temperature in Kelvin

    :param geometry: molecular geometry of a single molecule [Å]
    :param electronic_energy: electronic energy of the geometry [E_H]
    :param frequencies:       list of frequencies [cm^-1]
    :param multiplicity: spin multiplicity of the system
    :param rot_sym: symmetry number for external rotation
    :param DeltaE0: Correction for the zero point energy that is used in the
                    partition function. This energy is essentially just used in
                    a Boltzmann factor multiplied with the partition function,
                    i.e., :math:`\Delta = \Delta_{RRHO} \cdot \exp\left(-\frac
                    {\Delta E_0}{kT} \right)`. By default, the energy at 0K is
                    used as the zero point in the partition function.
                    Consequently, the Gibbs free energy is computed as
                    G = -RT ln(Delta) + E(0K), where E(0K) has the value of the
                    sum of the vibrational zero point energy and the electronic
                    energy. [J/mol]
    :param c_freq: scaling factor for vibrational frequencies
    :ivar scaled_freq: frequencies multiplied by c_freq
    '''

    _EVAL_THRESH = 1e-12
    '''threshold below which to consider eigenvalues of the moment of inertia
    tensor to be zero'''

    def __init__(self, geometry: Geometry,
            electronic_energy: float,
            frequencies: np.ndarray,
            multiplicity: int = 1,
            rot_sym:      int = 1,
            DeltaE0: float = 0,
            c_freq: float = 1.0) -> None:

        self.geometry    = geometry
        self.DeltaE0 = DeltaE0
        self.scaled_freqs = np.array(frequencies)*c_freq
        self.multiplicity = multiplicity
        self.rot_sym = rot_sym

        # call ZPE() after self.frequencies has been set
        super().__init__(E0=self.ZPE()+electronic_energy*E_h_p_particle)


        eval, evec = self.geometry.moment_of_inertia()
        self.Irank = np.count_nonzero(np.abs(eval)  > self._EVAL_THRESH)
        self.I = eval
        self.m=0.0
        for atom in self.geometry.atom_types:
            self.m+=atom.mass

    def _assert_pressure_is_nonzero(self, p: ArrayLike):
        '''raises a ValueError if any p is zero'''
        p = np.array(p)

        if (p.ndim == 0 and p == 0) or (p.ndim > 0 and any(p == 0)):
            raise ValueError('pressure of zero not allowed for translational partition function')

    def _assert_greater_than_zero(self, q: np.ndarray):
        if (q.ndim == 0 and q <= 0) or (q.ndim > 0 and any(q <= 0)):
            raise AssertionError('The partition function is smaller than zero')


    def _Qelec(self, T) -> float:
        ''' electronic partition function = degeneracy = multiplicity '''
        return self.multiplicity*np.exp(-self.DeltaE0/R/T)

    def _dQelec(self, T) -> float:
        ''' electronic partition function = degeneracy = multiplicity '''
        beta_DeltaE0 = self.DeltaE0/R/T
        return self.multiplicity*np.exp(-beta_DeltaE0)*beta_DeltaE0/T

    def _d2Qelec(self, T) -> float:
        ''' electronic partition function = degeneracy = multiplicity '''
        beta_DeltaE0 = self.DeltaE0/R/T
        return self.multiplicity*(-2*beta_DeltaE0
                                  + beta_DeltaE0**2
                    )/T**2*np.exp(-beta_DeltaE0)

    def _Qtrans(self, p, T) -> ArrayLike:
        ''' classical NpT partition function for an translation of ideal gas, 1 particle (not 1 mol!)
        q = (2pi m k_B T / h^2)^1.5 V
        units: kg J / J^2 s^2 = kg / s^2 / (kg m^2/s^2) = 1 / m^2
        => m^3 / m^3
        '''
        self._assert_pressure_is_nonzero(p)

        V = k_B * T / p
        nominator = 2.0 * np.pi * self.m*amu * k_B * T
        return (np.sqrt(nominator)/h)**3*V

    def _dQtrans(self, p, T) -> ArrayLike:
        ''' temperature derivative of classical NpT partition function '''
        self._assert_pressure_is_nonzero(p)
        q = (np.sqrt(2.0 * np.pi * self.m*amu * k_B)/h)**3*k_B/p
        return q*2.5*T**1.5 # factor rule d/dT q*T**1.5*T

    def _d2Qtrans(self, p, T) -> ArrayLike:
        '''second temperature derivative of classical NpT partition function '''
        self._assert_pressure_is_nonzero(p)
        q = (np.sqrt(2.0 * np.pi * self.m*amu * k_B)/h)**3*k_B/p
        return q*2.5*1.5*np.sqrt(T)

    def _theta_rot(self, I) -> float:
        return h**2/8/np.pi**2/I/k_B

    def _Qrot(self, T) -> ArrayLike:
        '''classical canonical rotational partition function for rigid 3D molecule;
        linear or atomic not yet implemented
        (8pi^2k_B T/h^2)^1.5 sqrt(pi I0 I1 I2)/sigma
        or
        for linear case: T/theta/sigma
        '''
        if self.Irank == 0: # atomic case
            return np.ones_like(T)
        if self.Irank == 2: # linear case
            # one element is zero, the two others the same
            theta = self._theta_rot((self.I[0]+self.I[1]+self.I[2])/2*amu*(rbohr**2))
            return T/theta/self.rot_sym
        if self.Irank == 3:
            theta_0 = self._theta_rot(self.I[0]*amu*(rbohr**2))
            theta_1 = self._theta_rot(self.I[1]*amu*(rbohr**2))
            theta_2 = self._theta_rot(self.I[2]*amu*(rbohr**2))
            return np.sqrt(np.pi*T**3/theta_0/theta_1/theta_2)/self.rot_sym
        raise ValueError("Faulty rotation with "+str(self.I))

    def _dQrot(self, T) -> ArrayLike:
        ''' temperature derivative of classical canonical rotational partition function '''
        if self.Irank == 0: #atomic case
            return np.zeros_like(T)
        if self.Irank == 2: # linear case
            # one element is zero, the two others the same
            theta = self._theta_rot((self.I[0]+self.I[1]+self.I[2])/2*amu*(rbohr**2))
            return 1/theta/self.rot_sym
        if self.Irank == 3:
            theta_0 = self._theta_rot(self.I[0]*amu*(rbohr**2))
            theta_1 = self._theta_rot(self.I[1]*amu*(rbohr**2))
            theta_2 = self._theta_rot(self.I[2]*amu*(rbohr**2))
            return 1.5*np.sqrt(np.pi*T/theta_0/theta_1/theta_2)/self.rot_sym
        raise ValueError("Faulty rotation with "+str(self.I))

    def _d2Qrot(self, T) -> float:
        ''' second temperature derivative of classical canonical rotational partition function '''
        if self.Irank == 0: # point
            return 0.0
        if self.Irank == 2: # linear
            return 0.0 # derivative of constant
        if self.Irank == 3: # potato
            theta_0 = self._theta_rot(self.I[0]*amu*(rbohr**2))
            theta_1 = self._theta_rot(self.I[1]*amu*(rbohr**2))
            theta_2 = self._theta_rot(self.I[2]*amu*(rbohr**2))
            return 1.5*0.5*np.sqrt(np.pi/T/theta_0/theta_1/theta_2)/self.rot_sym
        raise ValueError("Faulty rotation with "+str(self.I))

    def _Qvib(self, T) -> float:
        '''quantum canonical vibrational partition function for set of HOs,
        with respect to E(0K), i.e. zero-of-potential plus ZPE'''
        q = 1
        for freq in self.scaled_freqs: # loop through all modes
            if freq >= 0:
                # convert from per cm to per second
                nu = freq*100*c_0
                theta = h*nu/k_B# vibrational temperature
                qi=1/(1-np.exp(-theta/T))
                q=q*qi
        return q

    def _dQvib(self, T) -> float:
        ''' temperature derivative of canonical HO partition function '''
        result = 0
        for freq in self.scaled_freqs: # loop over all modes
            nu = freq*100*c_0
            theta = h*nu/k_B# vibrational temperature
            qi = 1/(1-np.exp(-theta/T))
            # d/dT (1-exp(-theta/T))^-1 = (-1)*qi^2 * d/dT (1-exp(-theta/T))
            #                                                 -exp(-theta/T) * d/dT (-theta/T)
            #                                                                        -theta * (-1)T^-2
            #          theta*exp(-theta/T)*qi^2 /T^2
            dqi = theta*np.exp(-theta/T)*qi**2/T**2
            result += dqi/qi
        return self._Qvib(T)*result

    def _d2Qvib(self, T) -> float:
        ''' second temperature derivative of canonical HO partition function'''
        sum = 0
        for freq in self.scaled_freqs:
            nu = freq*100*c_0
            theta = h*nu/k_B# vibrational temperature
            qi = 1/(1-np.exp(-theta/T))
            dqi = theta*np.exp(-theta/T)*qi**2/T**2
            # d theta*exp(-theta/T)*qi^2 /T^2
            # = theta*((theta/T^4 - 2/T^3)exp(-theta/T)q_i^2) + 2 dqi^2/qi
            d2qi = theta*((theta/T**4 - 2/T**3)*np.exp(-theta/T)*qi**2) + 2*theta*np.exp(-theta/T)/T**2*qi*dqi
            #   Q =  prod qi
            #  dQ = Q sum dqi/qi
            # d2Q = dQ sum dqi/qi + Q sum d(dqi qi^-1)
            #                             d2qi/qi - (dqi/qi)^2
            sum+=(d2qi/qi - (dqi/qi)**2)
        Q = self._Qvib(T)
        # d2Q = dQ sum dqi/qi + Q sum d(dqi qi^-1)
        #     = dQ^2 / Q  + Q sum d2qi/qi - (dqi/qi)^2
        return (self._dQvib(T)**2/Q + Q*sum)


    def Delta(self, p, T) -> float:
        '''NpT partition function with respect to E(0K), i.e. zero-of-potential plus ZPE'''

        return self._Qtrans(p, T)* \
               self._Qrot(T)*      \
               self._Qvib(T)*      \
               self._Qelec(T)

    # the derivative is multiplied by the partition function itself for
    # numerical reasons
    def dDelta_dT_over_Delta(self, p, T) -> float:
        '''Temperature derivative of NpT partition function multiplied by the
        partition function'''
        # product rule: Q = prod Qi
        #              dQ = sum dQi Q/Qi = Q sum dQi/Qi
        Qelec = self._Qelec(T)
        self._assert_greater_than_zero(Qelec)

        return (self._dQelec(T)/   Qelec   +
                self._dQtrans(p,T)/self._Qtrans(p,T) +
                self._dQrot(T)/    self._Qrot(T)     +
                self._dQvib(T)/    self._Qvib(T))

    def d2Delta_dT2_over_Delta(self, p, T) -> float:
        '''second temperature derivative of NpT partition function multiplied
        by the partition function'''
        # product rule: Q = prod Qi
        #              dQ = sum dQi Q/Qi = Q sum dQi/Qi
        #              d2Q = d ( Q sum dQi/Qi)
        #                  = dQ sum dQi/Qi + Q sum d (dQi/Qi)
        #                  = dQ dQ / Q + Q sum d (dQi/Qi)
        #                  = (dQ)^2 /Q + Q sum d2Qi/Qi - (dQi / Qi)^2
        #                  = Q((dQ/Q)^2 + sum (d2Qi - (dQi)^2 / Qi)/Qi)
        Q = self.Delta(p,T)
        dQ = self.dDelta_dT_over_Delta(p,T)
        d2Q = (dQ)**2
        for (Qi, dQi, d2Qi) in ((self._Qelec(T),    self._dQelec(T),    self._d2Qelec(T)),
                                (self._Qtrans(p,T), self._dQtrans(p,T), self._d2Qtrans(p,T)),
                                (self._Qrot(T),     self._dQrot(T),     self._d2Qrot(T)),
                                (self._Qvib(T),     self._dQvib(T),     self._d2Qvib(T))):
            d2Q += (d2Qi - dQi**2/Qi)/Qi
        return d2Q

    def ZPE(self) -> float:
        '''Harmonic Oscillator Zero-point Energy'''
        myZPE = 0.0
        for freq in self.scaled_freqs:
            nu = freq*100*c_0 # per second
            myZPE+=(h*nu/2) # J
        return myZPE*N_A

class RRHOConformerMix(DerivedFromNpTEnsemble):
    '''
    models each conformer as RRHO. The mixture of conformers is modeled by
    assuming that each conformer provides a set of accessible states, i.e.,
    the partition function is the sum of the conformer's RRHO partition function
    '''

    def __init__(self, conformers: Iterable[RRHO]) -> None:
        # find conformer with smallest zero point energy (electronic +
        # vibrational) to use as reference
        E0_min = inf
        conf_min = None
        for i, conf in enumerate(conformers):
            if conf.E0 < E0_min:
                E0_min = conf.E0
                conf_min = i

        self.conformers = conformers

        super().__init__(E0=E0_min)

    def Delta(self, *, p: ArrayLike, T: ArrayLike) -> ArrayLike:
        return np.sum([conf.Delta(T=T, p=p)*np.exp(-(conf.E0-self.E0)/R/T)
                       for conf in self.conformers],
                      axis=0)

    def _evaluate_conf_prob(self, p: ArrayLike, T: ArrayLike)\
            -> tuple[ArrayLike, ArrayLike, ArrayLike]:
        '''helper function to compute the probabilities p_i of conformer i, the
        partition functions of each conformer Delta_i, and the difference of the
        zero-point energy of each conformer to the lowest zero-point energy
        Delta_E0_i

        :return: Delta_i, delta_E0_i, p_i which are of shape n x m or n where n
                 is the number of conformers and m is the size of the input p/T
                 array. If p and T are sclars, the output has shape n.'''
        size = self._get_output_size(p=p, T=T)

        # conformer partition functions
        Delta_i = np.array([conf.Delta(T=T, p=p) for conf in self.conformers])

        # difference to reference energy of lowest conformer
        delta_E0_i = np.array([conf.E0 for conf in self.conformers])
        delta_E0_i -= np.min(delta_E0_i)

        # If p or T is nonscalar, copy the current values per conformer along
        # the second dimension (temperature/pressure). Then Delta_E0_i/T
        # produces the correct result dimensionwise
        if size is not None:
            delta_E0_i = np.expand_dims(delta_E0_i, axis=1)
            delta_E0_i = np.repeat(delta_E0_i, size, axis=1)
        p_i = Delta_i*np.exp(-delta_E0_i/R/T)/self.Delta(p=p, T=T)

        return Delta_i, delta_E0_i, p_i


    def dDelta_dT_over_Delta(self, *, p: ArrayLike, T: ArrayLike) -> ArrayLike:
        T = np.array(T)
        p = np.array(p)
        Delta_i, delta_E0_i, p_i = self._evaluate_conf_prob(p=p, T=T)

        dDelta_i_over_Delta_i = np.array([conf.dDelta_dT_over_Delta(T=T, p=p)
                       for conf in self.conformers])

        return np.squeeze(np.sum(p_i*delta_E0_i/R/T**2, axis=0)
                + np.sum(p_i*dDelta_i_over_Delta_i, axis=0))

    def d2Delta_dT2_over_Delta(self, *, p: ArrayLike, T: ArrayLike) -> ArrayLike:
        T = np.array(T)
        p = np.array(p)
        _, delta_E0_i, p_i = self._evaluate_conf_prob(p=p, T=T)


        dDelta_i_over_Delta_i = np.array([conf.dDelta_dT_over_Delta(T=T, p=p)
                                          for conf in self.conformers])
        d2Delta_i_over_Delta_i = np.array([conf.d2Delta_dT2_over_Delta(T=T, p=p)
                                           for conf in self.conformers])

        delta_E0_i_R_T2 = delta_E0_i/R/T**2

        return np.squeeze(np.sum(p_i*(2*dDelta_i_over_Delta_i*delta_E0_i_R_T2
                                      + delta_E0_i_R_T2**2
                                      + d2Delta_i_over_Delta_i
                                      - 2*delta_E0_i_R_T2/T), axis=0))

# TM is a type that inherits from ThermoModel
TM = TypeVar('TM', bound=ThermoModel)
class ThermoModelFactory(Generic[TM], metaclass=ABCMeta):
    '''
    abstract class to create factories for creating thermo models from data in
    a SpeciesDB

    :param db: database with frequency, geometry, etc. information
    :param geo_lot: level of theory at which the geometry was optimized and
                    frequencies where computed
    :param energy_lot: level of theory at which the single point energy was
                       computed. If None, geo_lot will be used.
    '''
    def __init__(self, db: SpeciesDB, geo_lot: LevelOfTheory,
                 energy_lot: LevelOfTheory = None) -> None:
        super().__init__()

        self.geo_lot = geo_lot
        self.energy_lot = energy_lot if energy_lot is not None else geo_lot

        self.db = db

    @abstractmethod
    def create(self, species: Species) -> TM:
        '''creates an instance of a thermomodel class'''

class RRHOFactory(ThermoModelFactory[RRHO]):
    '''
    creates an RRHO object with the data from a species database

    Searches the database for that geometry of a given species, which was optimized at geo_lot and has the lowest electronic_energy at energy_lot. Then loads frequencies computed at geo_lot and the SPE computed at energy_lot for that geometry from the database. The multiplicity is taken from geo_lot and the rotational symmetry number is also loaded from the database.

    :param db: database with frequency, geometry, etc. information
    :param geo_lot: level of theory at which the geometry was optimized and
                    frequencies where computed
    :param energy_lot: level of theory at which the single point energy was
                       computed. If None, geo_lot will be used.
    :param c_freq: scaling factors for vibrational frequencies
    '''

    def __init__(self, db: SpeciesDB, geo_lot: LevelOfTheory,
                 energy_lot: LevelOfTheory = None, c_freq: float = 1) -> None:
        super().__init__(db, geo_lot, energy_lot)
        self.c_freq = c_freq

    def create(self, species: Species) -> RRHO:
        ''':return: an RRHO object for the given species
        :raises: InsufficientRRHODataError if the database does not contain all the necessary data'''
        criterion = OptimizedAt(self.geo_lot)>>OnlyLowestEnergy(self.energy_lot)

        try:
            geo_id = self.db.list_geometries(species.id, criterion)[0]
        except IndexError:
            raise InsufficientRRHODataError('Could not find a geometry at the requested levels of theory.')

        data = {
            'electronic_energy': self.db.load_electronic_energy(
                                        geo_id, lot=self.energy_lot),
            'frequencies': self.db.load_frequencies(geo_id, lot=self.geo_lot),
            'rot_sym': self.db.load_rotational_symmetry_nr(geo_id),
            'multiplicity': self.geo_lot.el_struc.multiplicity
        }

        for datum, value in data.items():
            if value is None:
                raise InsufficientRRHODataError(f'Could not find {datum} for '
                                                f'{species.inchi}.')

        return RRHO(geometry=self.db.load_geometry(geo_id), c_freq=self.c_freq,
                    **data)

class InsufficientRRHODataError(Exception):
    '''raised when RRHOFromDbFactory cannot find all the necessary data for the
    requested species'''


