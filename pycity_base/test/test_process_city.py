#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test for processing a city district.
"""

from __future__ import division

import copy
import shapely.geometry.point as point

import pycity_base.classes.building as building
from pycity_base.functions import process_city as processcity

from pycity_base.test.pycity_fixtures import create_environment, \
    create_building, create_apartment, create_demands, \
    create_empty_citydist, create_citydist


class TestProcessCity():
    def test_get_subcity(self, create_empty_citydist, create_environment):

        city = copy.deepcopy(create_empty_citydist)

        building1 = building.Building(environment=create_environment)
        building2 = building.Building(environment=create_environment)
        building3 = building.Building(environment=create_environment)

        pos1 = point.Point(0, 0)
        pos2 = point.Point(0, 20)
        pos3 = point.Point(0, 40)

        city.addEntity(entity=building1, position=pos1)
        city.addEntity(entity=building2, position=pos2)
        city.addEntity(entity=building3, position=pos3)

        list_subcity = [1002, 1003]

        subcity = processcity.get_subcity(city=city, nodelist=list_subcity)

        assert sorted(subcity.nodes()) == list_subcity
