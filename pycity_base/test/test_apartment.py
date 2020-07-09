#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Apartment test.
"""

from __future__ import division

import numpy as np

import pycity_base.classes.demand.apartment as apartment
from pycity_base.test.pycity_fixtures import create_environment, create_demands, \
    create_apartment


class TestApartment(object):

    def test_init(self, create_environment):
        #  Generate apartment object
        test_apartment = apartment.Apartment(create_environment)

        #  Return all demands
        el_load_curve = test_apartment.get_total_el_power()
        th_load_curves = test_apartment.get_total_th_space_heating_power()

        assert np.sum(el_load_curve) == 0
        assert np.sum(th_load_curves[0]) == 0
        assert np.sum(th_load_curves[1]) == 0

    def test_addEntity(self, create_environment, create_demands):

        heat_demand = create_demands[0]

        #  Generate apartment object
        test_apartment = apartment.Apartment(create_environment)

        #  Add entity
        test_apartment.addEntity(heat_demand)

        #  Return heat power (in W)
        heat_load_curve = test_apartment.get_total_th_space_heating_power(currentValues=False, returnTemperature=False)

        #  Convert to energy values (in kWh)
        th_energy_demand_values = heat_load_curve * create_environment.timer.time_discretization / (1000*3600)

        assert abs(np.sum(th_energy_demand_values) - 100*150) <= 0.001 * 100 * 150

    def test_addMultipleEntities(self, create_environment, create_demands):
        el_demand = create_demands[1]

        dhw_annex42 = create_demands[2]

        #  Generate apartment object
        test_apartment = apartment.Apartment(create_environment)
        #  Add multiple entities
        test_apartment.addMultipleEntities([el_demand, dhw_annex42])

        #  Return electrical power (in W)
        el_load_curve = test_apartment.get_total_el_power(currentValues=False)

        #  Convert to energy values (in kWh)
        el_energy_demand_values = el_load_curve * create_environment.timer.time_discretization / (1000*3600)

        assert abs(np.sum(el_energy_demand_values) - 3000) <= 0.001 * 3000

        #  Return thermal power
        dhw_heat_load_curve = test_apartment.get_total_th_space_heating_power(currentValues=False,
                                                                              returnTemperature=False)
        #  Convert to energy values (in kWh)
        th_energy_demand_values = dhw_heat_load_curve * create_environment.timer.time_discretization / (1000*3600)

        daily_consumption = 70
        t_flow = 70
        supply_temp = 25

        #  Annual energyy demand value (in kWh)
        dhw_annual_demand = np.sum(th_energy_demand_values)
        #  Reference value in kWh
        reference_value = daily_consumption * 365 * 4180 * (t_flow - supply_temp) / (1000 * 3600)

        assert abs(np.sum(dhw_annual_demand) - reference_value) <= 0.001 * reference_value

    def test_get_demands(self, create_apartment):
        space_heat_power = create_apartment.get_power_curves(getElectrical=False,
                                                             getDomesticHotWater=False,
                                                             getSpaceHeating=True,
                                                             getSpaceCooling=False,
                                                             currentValues=False)[0]
        space_cool_power = create_apartment.get_power_curves(getElectrical=False,
                                                             getDomesticHotWater=False,
                                                             getSpaceHeating=False,
                                                             getSpaceCooling=True,
                                                             currentValues=False)[0]
        el_power = create_apartment.get_power_curves(getElectrical=True,
                                                     getDomesticHotWater=False,
                                                     getSpaceHeating=False,
                                                     getSpaceCooling=False,
                                                     currentValues=False)[0]
        dhw_power = create_apartment.get_power_curves(getElectrical=False,
                                                      getDomesticHotWater=True,
                                                      getSpaceHeating=False,
                                                      getSpaceCooling=False,
                                                      currentValues=False)[0]

        #  Convert to energy values (in kWh)
        th_energy_heating_demand_values = space_heat_power * create_apartment.environment.timer.\
            time_discretization / (1000*3600)

        assert abs(np.sum(th_energy_heating_demand_values) - 100*150) <= 0.001 * 100 * 150

        #  Convert to energy values (in kWh)
        th_energy_cooling_demand_values = space_heat_power * create_apartment.environment.timer.\
            time_discretization / (1000*3600)

        assert abs(np.sum(th_energy_cooling_demand_values) - 100 * 150) <= 0.001 * 100 * 150

        #  Convert to energy values (in kWh)
        el_energy_demand_values = el_power * create_apartment.environment.timer.time_discretization / (1000*3600)

        assert abs(np.sum(el_energy_demand_values) - 3000) <= 0.01 * 3000

        daily_consumption = 70
        t_flow = 70
        supply_temp = 25

        #  Convert to energy values (in kWh)
        th_energy_demand_values = dhw_power * create_apartment.environment.timer.time_discretization / (1000*3600)

        #  Annual energyy demand value (in kWh)
        dhw_annual_demand = np.sum(th_energy_demand_values)
        #  Reference value in kWh
        reference_value = daily_consumption * 365 * 4180 * (t_flow - supply_temp) / (1000 * 3600)

        assert abs(np.sum(dhw_annual_demand) - reference_value) <= 0.001 * reference_value

    def test_get_max_nb_occupants(self, create_apartment):
        create_apartment.get_max_nb_occupants()
