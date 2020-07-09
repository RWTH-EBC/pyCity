#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Space cooling test.
"""

from __future__ import division

import numpy as np
import pytest

import pycity_base.classes.demand.space_cooling as sc
from pycity_base.test.pycity_fixtures import create_environment


class TestSpaceCooling(object):

    def test_method0(self, create_environment):  # User-defined load profile
        #  energy comparison array
        load_array = np.array([10, 10, 10, 10, 20, 20, 20, 20])

        #  Space cooling object
        spacecooling = sc.SpaceCooling(create_environment, method=0, loadcurve=load_array)

        #  Return load curve of space cooling object
        space_cooling_load_curve = spacecooling.get_power(currentValues=False)

        #  Compare arrays
        np.testing.assert_equal(space_cooling_load_curve, load_array)

    def test_method1(self, create_environment):  # Standard load profile

        #  Generate space cooling object
        spacecooling = sc.SpaceCooling(create_environment,
                                       method=1,
                                       living_area=100,
                                       specific_demand=150)

        #  Get space cooling load curve (in W) per timestep
        space_cooling_load_curve = spacecooling.get_power(currentValues=False)

        #  Convert to energy demand values (in kWh)
        th_energy_demand_curve = space_cooling_load_curve * create_environment.timer.time_discretization / (1000 * 3600)

        #  Check if sum of energy demand values is (almost) equal to input
        assert abs(np.sum(th_energy_demand_curve)) == 0.0
