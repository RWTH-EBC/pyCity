#!/usr/bin/env python
# coding=utf-8
"""
Domestic hot water test.
"""

from __future__ import division

import numpy as np
import copy

import pycity_base.classes.demand.domestic_hot_water as dhw
from pycity_base.test.pycity_fixtures import create_environment, create_occupancy


class TestDomesticHotWater(object):
    """
    Test class for pyCity domestic hot water object.
    """

    def test_method1(self, create_environment):
        """
        Test method for IEA annex 42 domestic hot water profile generator

        Parameters
        ----------
        create_environment : object
            Environment object (pytest fixture)
        """
        t_flow = 60
        supply_temperature = 25
        daily_consumption = 50

        dhw_annex42 = dhw.DomesticHotWater(create_environment,
                                           t_flow=t_flow,
                                           thermal=True,
                                           method=1,
                                           daily_consumption=daily_consumption,
                                           supply_temperature=supply_temperature)

        #  Thermal power in W (per 15 minute timestep)
        load_curve = dhw_annex42.get_power(currentValues=False,
                                           returnTemperature=False)

        #  Convert power to energy demand values for dhw (in kWh)
        energy_curve = load_curve * create_environment.timer.time_discretization / (1000 * 3600)

        #  annual energy demand
        annual_dhw_energy_demand = np.sum(energy_curve)

        #  Reference value (in Joule)
        reference_value = 365 * daily_consumption * 4180 * (t_flow - supply_temperature)

        #  Convert to kWh
        reference_value = reference_value / (1000 * 3600)

        print('Reference value in kWh: ', reference_value)
        print('DHW annual energy demand in kWh: ', annual_dhw_energy_demand)

        assert abs(annual_dhw_energy_demand - reference_value) <= 0.01
        assert (dhw_annex42.water is None)

    def test_method2(self, create_environment, create_occupancy):
        """
        Test method for stochastic domestic hot water profile generator

        Parameters
        ----------
        create_environment : object
            Environment object (pytest fixture)
        """
        occupancy_profile = create_occupancy.occupancy

        dhw_stochastical = dhw.DomesticHotWater(create_environment,
                                                t_flow=60,
                                                thermal=True,
                                                method=2,
                                                supply_temperature=20,
                                                occupancy=occupancy_profile)

        #  DHW volume flow curve in liters/hour
        volume_flow_curve = dhw_stochastical.water
        #  Recalc into water volume in liters
        water_volume_per_timestep = volume_flow_curve / 3600 * create_environment.timer.time_discretization
        # Average daily dhw consumption in liters
        av_daily_dhw_volume = np.sum(water_volume_per_timestep) / 365

        #  Check if av_daily_dhw_volume is within sufficient limits
        assert (av_daily_dhw_volume <= 250)
        assert (av_daily_dhw_volume >= 45)
        assert (dhw_stochastical is not None)

    def test_method3(self, create_environment):
        """
        Test method for IEA annex 42 domestic hot water profile generator

        Parameters
        ----------
        create_environment : object
            Environment object (pytest fixture)
        """
        t_flow = 60
        supply_temperature = 25
        daily_consumption = 200

        environment = copy.deepcopy(create_environment)

        environment.timer.time_discretization = 3600

        dhw_annex42 = dhw.DomesticHotWater(create_environment,
                                           t_flow=t_flow,
                                           thermal=True,
                                           method=1,
                                           daily_consumption=daily_consumption,
                                           supply_temperature=supply_temperature)

        daily_consumption = 300

        dhw_annex42 = dhw.DomesticHotWater(create_environment,
                                           t_flow=t_flow,
                                           thermal=False,
                                           method=1,
                                           daily_consumption=daily_consumption,
                                           supply_temperature=supply_temperature)

    def test_multiple_resolutions(self, create_environment, create_occupancy):

        timer = create_environment.timer
        occupancy_profile = create_occupancy.occupancy
        tFlow = 60
        supplyTemperature = 25
        dailyConsumption = 50

        #  Generate electrical demand object
        dhw_1 = dhw.DomesticHotWater(create_environment,
                                     t_flow=tFlow,
                                     thermal=True,
                                     method=1,
                                     daily_consumption=dailyConsumption,
                                     supply_temperature=supplyTemperature)

        timer.time_discretization = int(timer.time_discretization/2)
        dhw_2 = dhw.DomesticHotWater(create_environment,
                                     t_flow=tFlow,
                                     thermal=True,
                                     method=1,
                                     daily_consumption=dailyConsumption,
                                     supply_temperature=supplyTemperature)

        #  Thermal power in W (per 15 minute timestep)
        load_1 = dhw_1.get_power(currentValues=False, returnTemperature=False)
        #  Thermal power in W (per 7.5 minute timestep)
        load_2 = dhw_2.get_power(currentValues=False, returnTemperature=False)

        assert len(load_2) == len(load_1) * 2

        assert np.allclose(load_2[::2], load_1)
        assert np.isclose(np.mean(load_2), np.mean(load_1))

    def test_multiple_resolutions_stochastical(self, create_environment, create_occupancy):
        timer = create_environment.timer
        occupancy_profile = create_occupancy.occupancy

        #  Generate electrical demand object
        dhw_1 = dhw.DomesticHotWater(create_environment,
                                     t_flow=60,
                                     thermal=True,
                                     method=2,
                                     supply_temperature=20,
                                     occupancy=occupancy_profile)

        timer.time_discretization = int(timer.time_discretization / 2)

        dhw_2 = dhw.DomesticHotWater(create_environment,
                                     t_flow=60,
                                     thermal=True,
                                     method=2,
                                     supply_temperature=20,
                                     occupancy=occupancy_profile)

        #  Thermal power in W (per 15 minute timestep)
        load_1 = dhw_1.get_power(currentValues=False, returnTemperature=False)
        #  Thermal power in W (per 7.5 minute timestep)
        load_2 = dhw_2.get_power(currentValues=False, returnTemperature=False)

        assert len(load_2) == len(load_1) * 2

        assert np.isclose(np.mean(load_2), np.mean(load_1), rtol=0.1)
