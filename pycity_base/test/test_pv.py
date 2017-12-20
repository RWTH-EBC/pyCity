#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
from __future__ import division

import pycity_base.classes.supply.PV as PV

import pycity_base.classes.Timer
import pycity_base.classes.Weather
import pycity_base.classes.Prices
import pycity_base.classes.Environment

class TestPV():
    def test_pv_check_annual_energy(self):
        """
        Test to check annual energy output of PV object instance
        """

        pv_area = 8  # in m2
        eta = 0.12  #  Efficiency
        beta = 0

        timer = pycity_base.classes.Timer.Timer()

        weather = pycity_base.classes.Weather.Weather(timer)

        prices = pycity_base.classes.Prices.Prices()

        environment = pycity_base.classes.Environment.\
            Environment(timer=timer,
                        weather=weather,
                        prices=prices)

        pv = PV.PV(environment=environment,
                   area=pv_area, eta=eta, beta=beta)

        pv_pow_array = pv.getPower(currentValues=False, updatePower=True)

        pv_energy_out = sum(pv_pow_array) * timer.timeDiscretization / \
                        (1000 * 3600)  # in kWh

        assert pv_energy_out > 900
        assert pv_energy_out < 1000
