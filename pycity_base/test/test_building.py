#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
from __future__ import division

import pycity_base.classes.demand.Apartment as Apart
import pycity_base.classes.Building as Build
import pycity_base.classes.supply.BES as BES
import pycity_base.classes.HeatingCurve as Hcurve

import pycity_base.classes.demand.Apartment as Apartment
from pycity_base.test.pycity_fixtures import create_environment, create_demands, \
    create_apartment, create_building, create_occupancy


class Test_Building():

    def test_init_building(self, create_environment):

        Build.Building(environment=create_environment)

    def test_add_entity(self, create_environment,
                        create_apartment):
        building = Build.Building(environment=create_environment)

        building.addEntity(entity=create_apartment)

        bes = BES.BES(environment=create_environment)

        building.addEntity(entity=bes)

        hcurve = Hcurve.HeatingCurve(environment=create_environment)

        building.addEntity(entity=hcurve)

        building.getFlowTemperature()

    def test_get_power_curves(self, create_building):
        create_building.get_power_curves(current_values=True)
        create_building.get_power_curves(current_values=False)

    def test_get_space_heating_power_curve(self, create_building):
        create_building.get_space_heating_power_curve(current_values=False)
        create_building.get_space_heating_power_curve(current_values=True)

    def test_get_electric_power_curve(self, create_building):
        create_building.get_electric_power_curve(current_values=False)
        create_building.get_electric_power_curve(current_values=True)

    def test_get_dhw_power_curve(self, create_building):
        create_building.get_dhw_power_curve(current_values=False)
        create_building.get_dhw_power_curve(current_values=True)

    def test_get_occupancy_profile(self, create_occupancy, create_environment):
        building = Build.Building(environment=create_environment)

        assert building.get_number_of_apartments() == None
        assert building.get_number_of_occupants() == None
        assert building.get_net_floor_area_of_building() == None

        apartment = Apart.Apartment(environment=create_environment)
        apartment2 = Apart.Apartment(environment=create_environment)

        apartment.addEntity(entity=create_occupancy)
        apartment2.addEntity(entity=create_occupancy)

        apartment.net_floor_area = 20
        apartment2.net_floor_area = 30

        building.addEntity(entity=apartment)
        building.addEntity(entity=apartment2)

        building.get_occupancy_profile()

        assert building.get_number_of_apartments() == 2
        assert building.get_number_of_occupants() == 2
        assert building.get_net_floor_area_of_building() == 50
