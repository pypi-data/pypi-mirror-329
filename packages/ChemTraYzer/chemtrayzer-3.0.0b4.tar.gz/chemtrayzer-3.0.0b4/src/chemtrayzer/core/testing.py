"""Utility functions for testing classes derived from core classes"""

from dataclasses import dataclass

from numpy.typing import ArrayLike
import numpy as np
import pytest

from chemtrayzer.core.thermo import ThermoModel


@dataclass
class ThermoTestData:
    '''container for data to test ThermoModel classes'''
    model: ThermoModel
    '''instance for which to compare computed vs. expected values'''
    T: ArrayLike
    '''one or more input temperatures'''
    p: ArrayLike
    '''one or more input pressures'''
    expected: ArrayLike
    '''expected output. Depending on the test, this is H, c_v, G, ...'''
    rtol: float = None
    '''relative numerical tolerance'''

class BaseThermoModelTest:
    '''base class that can be used for all test cases of concrete implementations of thermo model.

    To use this class, you just need to inherit from it and implement a set of fixtures that define input and expected output values.

    .. code:

        class TestMyThermoModel(BaseThermoModelTest):

            @pytest.fixture
            def dH_dT_data(self) -> BaseTestThermoModel.TestData:
                # here, expected_value can be None
                ...

            @pytest.fixture
            def dG_dT_data(self) -> BaseTestThermoModel.TestData:
                # here, expected_value can be None
                ...

            @pytest.fixture
            def H_data(self) -> BaseTestThermoModel.TestData:
                # here, we need to define all fields of TestData. "expected_value" should contain the expected enthalpies within chemical accuracy.
                ...

            # also define c_p_data, c_v_data, S_data, and G_data
            ...

    '''

    def test_c_p_eq_dH_dT(self, dH_dT_data: ThermoTestData):
        '''tests wether the numerical derivative of H w.r.t. T is equal to c_p'''
        model = dH_dT_data.model

        T = dH_dT_data.T #np.linspace(200, 3000, 10)
        p = dH_dT_data.p
        dT = 1e-5       # = sqrt(1e-16)*1000K

        c_p_actual = np.array([model.c_p(p=p, T=t) for t in T])

        H_T_plus_dt = np.array([model.H(p=p, T=t+dT) for t in T])
        H_of_T = np.array([model.H(p=p, T=t) for t in T])
        c_p_numerical = (H_T_plus_dt - H_of_T)/dT

        # rtol=1e-4, b/c of the numerical derivative
        np.testing.assert_allclose(c_p_actual, c_p_numerical, rtol=1e-4)

    def test_S_eq_dG_dT(self, dG_dT_data: ThermoTestData):
        '''check whether the numerical derivative dG/dT at constant p is
        approximately equal to -S'''
        model = dG_dT_data.model

        T = dG_dT_data.T
        p = dG_dT_data.p
        dT = 1e-5       # = sqrt(1e-16)*1000K

        S_actual = np.array([model.S(p=p, T=t) for t in T])

        G_T_plus_dt = np.array([model.G(p=p, T=t+dT) for t in T])
        G_of_T = np.array([model.G(p=p, T=t) for t in T])
        S_numerical = -(G_T_plus_dt - G_of_T)/dT

        # rtol=1e-4, b/c of the numerical derivative
        np.testing.assert_allclose(S_actual, S_numerical, rtol=1e-4)

    def test_c_v(self, c_v_data: ThermoTestData):
        c_v = c_v_data.model.c_v(p=c_v_data.p, T=c_v_data.T)

        assert c_v == pytest.approx(c_v_data.expected, rel=c_v_data.rtol)

    def test_c_p(self, c_p_data: ThermoTestData):
        c_p = c_p_data.model.c_p(p=c_p_data.p, T=c_p_data.T)

        assert c_p == pytest.approx(c_p_data.expected, rel=c_p_data.rtol)

    def test_H(self, H_data: ThermoTestData):
        H = H_data.model.H(p=H_data.p, T=H_data.T)

        # use "chemical accuracy" of 4kJ/mol
        assert H == pytest.approx(H_data.expected, abs=4e3, rel=H_data.rtol)

    def test_G(self, G_data: ThermoTestData):
        G = G_data.model.G(p=G_data.p, T=G_data.T)

        # use "chemical accuracy" of 4kJ/mol
        assert G == pytest.approx(G_data.expected, abs=4e3, rel=G_data.rtol)

    def test_U(self, U_data: ThermoTestData):
        U = U_data.model.U(p=U_data.p, T=U_data.T)

        # use "chemical accuracy" of 4kJ/mol
        assert U == pytest.approx(U_data.expected, abs=4e3, rel=U_data.rtol)

    def test_S(self, S_data: ThermoTestData):
        S = S_data.model.S(p=S_data.p, T=S_data.T)

        assert S == pytest.approx(S_data.expected, rel=S_data.rtol)
