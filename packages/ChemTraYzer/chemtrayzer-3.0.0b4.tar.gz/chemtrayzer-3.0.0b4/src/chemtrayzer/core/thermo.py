# ruff: noqa
"""Thermodynamics

This module contains thermochemistry classes and functions.
"""

from __future__ import annotations

from chemtrayzer.core.constants import R


from abc import ABCMeta, abstractmethod
from typing import Union

import numpy as np
from numpy.typing import ArrayLike

class ThermoModel(metaclass=ABCMeta):
    '''
    abstract class providing state variables. Those must be implemented in
    children to evaluate specific equations of state.

    When deriving from this class, the helper class
    :class:`BaseThermoModelTest<chemtrayzer.core.testing.BaseThermoModelTest>`
    is a good starting point for setting up the test code fore the derived
    class.
    '''

    @abstractmethod
    def H(self, *, p: ArrayLike=None, T: ArrayLike=None) -> ArrayLike:
        '''
        :param p: pressure [Pa]
        :param T: temperature [K]
        :return: molar enthalpy [J/mol]
        :rtype: numpy array. If the input is scalar, the array is
                zero-dimensional and can be treated as a scalar
        '''

    @abstractmethod
    def U(self, *, p: ArrayLike=None, T: ArrayLike=None) -> ArrayLike:
        '''
        :param p: pressure [Pa]
        :param T: temperature [K]
        :return: molar internal energy [J/mol]
        :rtype: numpy array. If the input is scalar, the array is
                zero-dimensional and can be treated as a scalar
        '''

    @abstractmethod
    def G(self, *, p: ArrayLike=None, T: ArrayLike=None) -> ArrayLike:
        '''
        :param p: pressure [Pa]
        :param T: temperature [K]
        :return: molar Gibbs free energy [J/mol]
        :rtype: numpy array. If the input is scalar, the array is
                zero-dimensional and can be treated as a scalar
        '''

    @abstractmethod
    def A(self, *, p: ArrayLike=None, T: ArrayLike=None) -> ArrayLike:
        '''
        :param p: pressure [Pa]
        :param T: temperature [K]
        :return: molar Helmholtz free energy [J/mol]
        :rtype: numpy array. If the input is scalar, the array is
                zero-dimensional and can be treated as a scalar
        '''

    @abstractmethod
    def S(self, *, p: ArrayLike=None, T: ArrayLike=None) -> ArrayLike:
        '''
        :param p: pressure [Pa]
        :param T: temperature [K]
        :return: molar entropy in [J/(mol K)]
        :rtype: numpy array. If the input is scalar, the array is
                zero-dimensional and can be treated as a scalar
        '''

    @abstractmethod
    def c_p(self, *, p: ArrayLike=None, T: ArrayLike=None) -> ArrayLike:
        '''
        :param p: pressure [Pa]
        :param T: temperature [K]
        :return: isobaric heat capacity [J/(mol K)]
        :rtype: numpy array. If the input is scalar, the array is
                zero-dimensional and can be treated as a scalar
        '''

    @abstractmethod
    def c_v(self, *, p: ArrayLike=None, T: ArrayLike=None) -> ArrayLike:
        '''
        :param p: pressure [Pa]
        :param T: temperature [K]
        :return: isochoric heat capacity [J/(mol K)]
        :rtype: numpy array. If the input is scalar, the array is
                zero-dimensional and can be treated as a scalar
        '''

    @classmethod
    def _get_output_size(cls, p: ArrayLike, T: ArrayLike)\
            -> Union[int, None]:
        '''Checks if p and T are either scalar or 1D arrays. If both are arrays,
        then this functions also asserts that they have the same size.

        :return: size of the input array(s) or None, if p and T are scalar'''
        T = np.array(T)
        p = np.array(T)

        if T.ndim == 1 and p.ndim == 0:
            return T.size
        elif T.ndim == 1 and p.ndim == 1:
            assert p.size == T.size, ('p and T must have the same size or '
                                      'one must be scalar.')
            return T.size
        elif T.ndim == 0 and p.ndim == 1:
            return p.size
        elif T.ndim == 0 and p.ndim == 0:
            return None
        else:
            raise AssertionError('p and T must be scalar or 1D arrays')

class DerivedFromNpTEnsemble(ThermoModel, metaclass=ABCMeta):
    '''helper class that implements themodynamic variable derived from the
    isobaric isothermal partition function and its derivatives

    :param E0: difference between the zero-point that should be used for the
               energy and the zero-point used for the parition function Delta,
               i.e., G = -RT ln(Delta) + E0'''

    def __init__(self, E0: float) -> None:
        super().__init__()

        self.E0 = E0

    def _assert_pressure_is_nonzero(self, p: ArrayLike):
        '''raises a ValueError if any p is zero'''
        p = np.array(p)

        if (p.ndim == 0 and p == 0) or (p.ndim > 0 and any(p == 0)):
            raise ValueError('pressure of zero not allowed for translational partition function')

    def _assert_greater_than_zero(self, q: np.ndarray):
        if (q.ndim == 0 and q <= 0) or (q.ndim > 0 and any(q <= 0)):
            raise AssertionError('The partition function is smaller than zero')

    @abstractmethod
    def Delta(self, *, p: ArrayLike, T: ArrayLike) -> ArrayLike:
        '''isobaric-isothermal partition function'''

    @abstractmethod
    def dDelta_dT_over_Delta(self, *, p: ArrayLike, T: ArrayLike) -> ArrayLike:
        '''temperature derivative isobaric-isothermal partition function
        divided by the partition function itself'''
        # computing dDelta/dT*1/Delta directly instead of just dDelta/dT helps
        # improve numerical accuracy at some points in the code

    @abstractmethod
    def d2Delta_dT2_over_Delta(self, *, p: ArrayLike, T: ArrayLike)-> ArrayLike:
        '''second derivative of the isobaric-isothermal partition function
        divided by the partition function'''

    def U(self, *, p: ArrayLike = None, T: ArrayLike = None) -> ArrayLike:
        T = np.array(T)
        p = np.array(p)
        return self.H(p=p,T=T)-R*T

    def H(self, *, p: ArrayLike = None, T: ArrayLike = None) -> ArrayLike:
        T = np.array(T)
        p = np.array(p)
        return self.G(p=p,T=T) + T*self.S(p=p,T=T)

    def G(self, *, p: ArrayLike = None, T: ArrayLike = None) -> ArrayLike:
        T = np.array(T)
        p = np.array(p)
        Delta = self.Delta(p=p,T=T)

        self._assert_greater_than_zero(Delta)

        return (-1)*R*T*np.log(Delta) + self.E0

    def S(self, *, p: ArrayLike = None, T: ArrayLike = None) -> ArrayLike:
        T = np.array(T)
        p = np.array(p)

        Delta  = self.Delta(p=p, T=T)
        dDelta = self.dDelta_dT_over_Delta(p=p, T=T)

        self._assert_greater_than_zero(Delta)

        # d/dT ln Q(T) = dQ/dT d ln Q/dQ = dQ/dT / Q
        return R*(T*dDelta + np.log(Delta))

    def c_p(self, *, p: ArrayLike = None, T: ArrayLike = None) -> ArrayLike:
        T = np.array(T)
        p = np.array(p)

        dDelta = self.dDelta_dT_over_Delta(p=p, T=T)
        d2Delta = self.d2Delta_dT2_over_Delta(p=p, T=T)

        return 2*R*T*dDelta \
               + R*T**2*(d2Delta - (dDelta)**2)

    def A(self, *, p: ArrayLike = None, T: ArrayLike = None) -> ArrayLike:
        T = np.array(T)
        p = np.array(p)
        return self.G(p=p,T=T)-R*T

    def c_v(self, *, p: ArrayLike = None, T: ArrayLike = None) -> ArrayLike:
        T = np.array(T)
        p = np.array(p)
        return self.c_p(p=p, T=T) - R
