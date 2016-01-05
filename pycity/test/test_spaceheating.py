from __future__ import division

import numpy as np
import pytest

import pycity.classes.demand.SpaceHeating as SpaceHeating
from pycity.test.pycity_fixtures import create_environment


class Test_SpaceHeating(object):

    def test_method0(self, create_environment):
        #  energy comparison array
        load_array = np.array([10, 10, 10, 10, 20, 20, 20, 20])

        #  Space heating object
        spaceheating = SpaceHeating.SpaceHeating(create_environment, method=0,
                                                 loadcurve=load_array)

        #  Return load curve of space heating object
        space_heat_load_curve = spaceheating.getDemand(currentValues=False)

        #  Compare arrays
        np.testing.assert_equal(space_heat_load_curve, load_array)


    def test_method1(self, create_environment):  # Standard load profile

        #  Generate space heating object
        spaceheating = SpaceHeating.SpaceHeating(create_environment, method=1,
                                                 livingArea=100,
                                                 specificDemand=150)

        #  Get space heating load curve (in W) per timestep
        space_heat_load_curve = spaceheating.getDemand(currentValues=False)
        #  Convert to energy demand values (in kWh)
        th_energy_demand_curve = space_heat_load_curve * \
                                 create_environment.timer.timeDiscretization / \
                                 (1000 * 3600)

        #  Check if sum of energy demand values is (almost) equal to input
        assert abs(np.sum(th_energy_demand_curve) - 150 * 100) <= 0.01
