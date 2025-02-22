"""Chemical reaction kinetics

This module contains classes and functions for working with and representing
reaction kinetics and reaction network.
"""


from abc import ABCMeta, abstractmethod
from numbers import Number
from typing import Union

import numpy as np

class ReactionRate(metaclass=ABCMeta):
    '''base class for all (purely T-dependent) reaction rates
    '''

    @abstractmethod
    def k(self, T: Union[Number, np.ndarray], p: Union[Number, np.ndarray]
          ) -> Union[Number, np.ndarray]:
        '''compute kinetic rate constant

        :param T: temperature [K]
        :param p: pressure [Pa]
        :return: rate constant [cm^3n mol^n s^-1]
                 where n is the number of reactants minus one
                 returns an array, iff the input is an array
        '''


class PressureDependentReactionRate(metaclass=ABCMeta):
    '''base class for all T- and p-dependent reaction rates
    '''

    @abstractmethod
    def k(self, T: Union[Number, np.ndarray],
          p: Union[Number, np.ndarray]) -> Union[Number, np.ndarray]:
        '''compute kinetic rate constant

        :param T: temperature [K]
        :param p: pressure [Pa]
        :return: rate constant [cm^3n mol^n s^-1]
                 where n is the number of reactants minus one
                 returns an array, iff the input is an array
        '''
