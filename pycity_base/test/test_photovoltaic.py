#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Photovoltaic test.
"""

from __future__ import division

import pycity_base.classes.supply.photovoltaic as pv

import pycity_base.classes.timer
import pycity_base.classes.weather
import pycity_base.classes.prices
import pycity_base.classes.environment


class TestPhotovoltaic():
    def test_pv_check_method0_annual_energy(self):
        """
        Test to check annual energy output of PV object instance (´´method==0´´)
        """

        pv_area = 40000  # in m^2
        eta = 0.105  # efficiency
        beta = 30
        gamma = 0

        timer = pycity_base.classes.timer.Timer()

        weather = pycity_base.classes.weather.Weather(timer)

        prices = pycity_base.classes.prices.Prices()

        environment = pycity_base.classes.environment.\
            Environment(timer=timer,
                        weather=weather,
                        prices=prices)

        pv_unit = pv.PV(environment=environment, method=0, area=pv_area, eta_noct=eta, beta=beta, gamma=gamma,
                        radiation_noct=800, alpha_noct=-0.0041, t_cell_noct=46.0)

        pv_pow_array = pv_unit.getPower(currentValues=False, updatePower=True)

        pv_energy_out = sum(pv_pow_array) * timer.time_discretization / (1000 * 3600)  # in kWh

        assert pv_energy_out > 3965000
        assert pv_energy_out < 4200000

    def test_pv_check_method0_annual_energy2(self):
        """
        Test to check annual energy output of PV object instance (´´method==0´´)
        """

        pv_area = 8  # in m^2
        eta = 0.12  # efficiency
        beta = 0
        gamma = -10

        timer = pycity_base.classes.timer.Timer()
        #  Overwrite horizon with total number of timesteps
        timer.timesteps_horizon = timer.timesteps_total
        timer.timesteps_used_horizon = timer.timesteps_total

        weather = pycity_base.classes.weather.Weather(timer)

        prices = pycity_base.classes.prices.Prices()

        environment = pycity_base.classes.environment.\
            Environment(timer=timer,
                        weather=weather,
                        prices=prices)

        pv_unit = pv.PV(environment=environment, method=0, area=pv_area, eta_noct=eta, beta=beta, gamma=gamma)

        pv_pow_array = pv_unit.getPower(currentValues=True, updatePower=True)

        pv_energy_out = sum(pv_pow_array) * timer.time_discretization / (1000 * 3600)  # in kWh

        assert pv_energy_out > 900
        assert pv_energy_out < 950

    def test_pv_check_method1_annual_energy(self):
        """
        Test to check annual energy output of PV object instance (´´method==1´´)
        """

        pv_peak_power = 3785.0  # in kWp
        beta = 30
        gamma = 0

        timer = pycity_base.classes.timer.Timer()

        weather = pycity_base.classes.weather.Weather(timer)

        prices = pycity_base.classes.prices.Prices()

        environment = pycity_base.classes.environment. \
            Environment(timer=timer,
                        weather=weather,
                        prices=prices)

        pv_unit = pv.PV(environment=environment, method=1, peak_power=pv_peak_power, beta=beta, gamma=gamma,
                        radiation_noct=800)

        pv_pow_array = pv_unit.getPower(currentValues=False, updatePower=True)

        pv_energy_out = sum(pv_pow_array) * timer.time_discretization / (1000 * 3600)  # in kWh

        assert pv_energy_out > 3965000
        assert pv_energy_out < 4200000

