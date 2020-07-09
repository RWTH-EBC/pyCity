#!/usr/bin/env python
# coding=utf-8
"""
Pytest script for CityDistrict class of pycity
"""

import numpy as np
import shapely.geometry.point as point

import pycity_base.classes.city_district as citydist

from pycity_base.test.pycity_fixtures import create_environment, \
    create_building, create_apartment, create_demands, \
    create_empty_citydist, create_citydist


class TestCityDistrict(object):

    def test_init(self):
        """
        Test initialization of citydistrict object
        """
        city_object = citydist.CityDistrict(environment=create_environment)

        assert city_object.kind == 'citydistrict'

    def test_add_entity_building(self, create_empty_citydist, create_building):
        #  Create empty citydistrict
        city = create_empty_citydist

        #  Create building
        building = create_building
        position_1 = point.Point(0, 0)

        #  Add entity
        node_nb = city.addEntity(entity=building, position=position_1)

        assert city.node[node_nb]['entity'].kind == 'building'
        assert city.node[node_nb]['position'] == position_1
        #  Check uesgraphs attribute
        assert len(city.nodelist_building) == 1

    def test_add_multiple_entities(self, create_empty_citydist, create_building):
        #  Create empty citydistrict
        city = create_empty_citydist

        #  Create building
        building = create_building
        position_1 = point.Point(0, 0)
        position_2 = point.Point(0, 10)
        pos_list = [position_1, position_2]

        #  Add entity
        city.addMultipleEntities(entities=[building, building], positions=
                                 pos_list)

        assert len(city.nodelist_building) == 2

    def test_get_nb_of_entities(self, create_citydist):
        assert create_citydist.get_nb_of_entities(entity_name='building') == 3

    def test_get_node_numbers_of_entities(self, create_citydist):
        assert create_citydist.get_node_numbers_of_entities(entity_name='building') == [1001, 1002, 1003]

    def get_nb_of_building_entities(self, create_citydist):

        assert create_citydist.get_nb_of_building_entities() == 3

    def test_get_list_build_entity_node_ids(self, create_citydist):
        assert create_citydist.get_list_build_entity_node_ids() == [1001,
                                                                    1002,
                                                                    1003]

    def test_get_demands(self, create_citydist):

        demand_tuple = create_citydist.get_power_curves()

        #  Convert power values in W to energy values in kWh
        el_demand = np.sum(demand_tuple[0]) * create_citydist.environment.timer.time_discretization / (1000 * 3600)
        th_demand = np.sum(demand_tuple[1]) * create_citydist.environment.timer.time_discretization / (1000 * 3600)

        daily_consumption = 70
        t_flow = 70
        supply_temp = 25
        #  Reference value dhw (in kWh)
        ref_dwh_value = 365 * daily_consumption * 4180 * (t_flow - supply_temp) / (1000 * 3600)

        assert (el_demand - 3 * 3000) <= 0.001 * el_demand
        assert (th_demand - 3 * 100 * 150 - ref_dwh_value) <= 0.001 * th_demand

    #  TODO: Add tests for RES, PV and Windpower
