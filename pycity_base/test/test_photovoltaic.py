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
    def test_pv_check_annual_energy(self):
        """
        Test to check annual energy output of PV object instance
        """

        pv_area = 8  # in m^2
        eta = 0.12  # efficiency
        beta = 0

        timer = pycity_base.classes.timer.Timer()

        weather = pycity_base.classes.weather.Weather(timer)

        prices = pycity_base.classes.prices.Prices()

        environment = pycity_base.classes.environment.\
            Environment(timer=timer,
                        weather=weather,
                        prices=prices)

        pv_unit = pv.PV(environment=environment, area=pv_area, eta=eta, beta=beta)

        pv_pow_array = pv_unit.getPower(currentValues=False, updatePower=True)

        pv_energy_out = sum(pv_pow_array) * timer.time_discretization / \
                        (1000 * 3600)  # in kWh

        assert pv_energy_out > 900
        assert pv_energy_out < 1000

    def test_pv_check_annual_energy2(self):
        """
        Test to check annual energy output of PV object instance
        """

        pv_area = 8  # in m^2
        eta = 0.12  # efficiency
        beta = 0

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

        pv_unit = pv.PV(environment=environment, area=pv_area, eta=eta, beta=beta)

        pv_pow_array = pv_unit.getPower(currentValues=True, updatePower=True)

        pv_energy_out = sum(pv_pow_array) * timer.time_discretization / \
                        (1000 * 3600)  # in kWh

        assert pv_energy_out > 900
        assert pv_energy_out < 1000

