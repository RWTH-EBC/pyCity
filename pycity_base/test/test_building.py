#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Building test.
"""

from __future__ import division

import numpy as np

import pycity_base.classes.demand.apartment as apart
import pycity_base.classes.building as build
import pycity_base.classes.supply.building_energy_system as bes
import pycity_base.classes.heating_curve as hcurve

import pycity_base.classes.demand.apartment as Apartment
from pycity_base.test.pycity_fixtures import create_environment, create_demands, \
    create_apartment, create_building, create_occupancy


class TestBuilding():

    def test_init_building(self, create_environment):

        build.Building(environment=create_environment)

    def test_add_entity(self, create_environment,
                        create_apartment):
        building = build.Building(environment=create_environment)

        building.addEntity(entity=create_apartment)

        bes_unit = bes.BES(environment=create_environment)

        building.addEntity(entity=bes_unit)

        heatingcurve = hcurve.HeatingCurve(environment=create_environment)

        building.addEntity(entity=heatingcurve)

        building.getFlowTemperature()

    def test_get_power_curves(self, create_building):
        create_building.get_power_curves(currentValues=True)
        create_building.get_power_curves(currentValues=False)

    def test_get_space_heating_power_curve(self, create_building):
        create_building.get_space_heating_power_curve(currentValues=False)
        create_building.get_space_heating_power_curve(currentValues=True)

    def test_get_electric_power_curve(self, create_building):
        create_building.get_electric_power_curve(currentValues=False)
        create_building.get_electric_power_curve(currentValues=True)

    def test_get_dhw_power_curve(self, create_building):
        create_building.get_dhw_power_curve(currentValues=False)
        create_building.get_dhw_power_curve(currentValues=True)

    def test_get_occupancy_profile(self, create_occupancy, create_environment):
        building = build.Building(environment=create_environment)

        assert building.get_number_of_apartments() is None
        assert building.get_number_of_occupants() is None
        assert building.get_net_floor_area_of_building() is None

        apartment = apart.Apartment(environment=create_environment)
        apartment2 = apart.Apartment(environment=create_environment)

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

    def test_get_power_no_load(self, create_environment):
        building = build.Building(environment=create_environment)

        bes_unit = bes.BES(environment=create_environment)

        building.addEntity(entity=bes_unit)

        assert all(building.get_space_heating_power_curve(currentValues=False) == 0)
        assert all(building.get_space_heating_power_curve(currentValues=True) == 0)
        assert all(building.get_space_cooling_power_curve(currentValues=False) == 0)
        assert all(building.get_space_cooling_power_curve(currentValues=True) == 0)
        assert all(building.get_electric_power_curve(currentValues=False) == 0)
        assert all(building.get_electric_power_curve(currentValues=True) == 0)
        assert all(building.get_dhw_power_curve(currentValues=False) == 0)
        assert all(building.get_dhw_power_curve(currentValues=True) == 0)
