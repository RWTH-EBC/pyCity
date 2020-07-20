#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Space heating test.
"""

from __future__ import division

import numpy as np
import pytest

import pycity_base.classes.demand.space_heating as sh
from pycity_base.test.pycity_fixtures import create_environment

create_environment2 = create_environment


class TestSpaceHeating(object):

    def test_method0(self, create_environment):  # User-defined load profile
        #  energy comparison array
        load_array = np.array([10, 10, 10, 10, 20, 20, 20, 20])

        #  Space heating object
        spaceheating = sh.SpaceHeating(create_environment, method=0, loadcurve=load_array)

        #  Return load curve of space heating object
        space_heating_load_curve = spaceheating.get_power(currentValues=False)

        #  Compare arrays
        np.testing.assert_equal(space_heating_load_curve, load_array)

    def test_method1(self, create_environment):  # Standard load profile

        #  Generate space heating object
        spaceheating = sh.SpaceHeating(create_environment,
                                       method=1,
                                       living_area=100,
                                       specific_demand=150)

        #  Get space heating load curve (in W) per timestep
        space_heating_load_curve = spaceheating.get_power(currentValues=False)

        #  Convert to energy demand values (in kWh)
        th_energy_demand_curve = space_heating_load_curve * create_environment.timer.time_discretization / (1000 * 3600)

        #  Check if sum of energy demand values is (almost) equal to input
        assert abs(np.sum(th_energy_demand_curve) - 150 * 100) <= 0.001 * 150 * 100

    def test_method3(self, create_environment):  # Modelica profile

        #  Generate space heating object
        spaceheating = sh.SpaceHeating(create_environment,
                                       method=3,
                                       living_area=100,
                                       specific_demand=150)

        #  Get space heating load curve (in W) per timestep
        space_heating_load_curve = spaceheating.loadcurve

        #  Convert to energy demand values (in kWh)
        th_energy_demand_curve = space_heating_load_curve * create_environment.timer.time_discretization / (1000 * 3600)

        #  Check if sum of energy demand values is (almost) equal to input
        assert abs(np.sum(th_energy_demand_curve) - 150 * 100) <= 0.001 * 150 * 100

    @pytest.mark.parametrize("create_environment2", [(3600)], indirect=["create_environment2"])
    def test_multiple_resolutions(self, create_environment, create_environment2):

        #  Generate space heating object
        assert create_environment2.timer.time_discretization == 3600
        assert create_environment.timer.time_discretization == 900
        sh_1 = sh.SpaceHeating(create_environment2,
                               method=1,
                               living_area=100,
                               specific_demand=150)

        sh_2 = sh.SpaceHeating(create_environment,
                               method=1,
                               living_area=100,
                               specific_demand=150)

        #  Get space heating load curve (in W) per timestep
        load_1 = sh_1.get_power(currentValues=False)
        load_2 = sh_2.get_power(currentValues=False)

        assert len(load_1) == 24*365
        assert len(load_2) == 24*4*365

        rescaled_load_2 = np.mean(load_2.reshape(-1, 4), axis=1)
        assert np.allclose(rescaled_load_2, load_1)
        assert np.isclose(rescaled_load_2.sum(), load_1.sum())
