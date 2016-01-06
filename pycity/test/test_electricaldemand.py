# coding=utf-8

from __future__ import division

import numpy as np

import pycity.classes.demand.ElectricalDemand as ED
import pytest
from pycity.test.pycity_fixtures import create_environment


class Test_ElectricalDemand(object):
    """
    Test class for pyCity electrical demand object.
    """

    def test_method0(self, create_environment):
        #  energy comparison array
        load_array = np.array([10, 10, 10, 10, 20, 20, 20, 20])

        el_demand_object = ED.ElectricalDemand(create_environment, method=0,
                                               loadcurve=load_array)

        el_load_curve = el_demand_object.getDemand()

        #  Compare arrays
        np.testing.assert_equal(el_load_curve, load_array)

    def test_method1(self, create_environment):  # Standard load profile
        #  Generate electrical demand object
        el_demand_object = ED.ElectricalDemand(create_environment, method=1,
                                               profileType="H0",
                                               annualDemand=3000)

        #  Get space heating load curve (in W) per timestep
        el_load_curve = el_demand_object.getDemand(currentValues=False)

        #  Convert power to energy values (W to Ws)
        el_en_demand_curve = create_environment.timer.timeDiscretization * \
                             el_load_curve

        #  Calculate electric energy demand value in kWh
        el_en_demand_curve = el_en_demand_curve / (1000 * 3600)
        el_en_demand_value = np.sum(el_en_demand_curve)

        #  Check if sum of energy demand values is (almost) equal to input
        assert abs(el_en_demand_value - 3000) <= 0.01

    def test_method2(self, create_environment):  # Stochastic load profile

        #  Occupancy profile
        occupancy_profile = np.ones((365 * 24 * 60,), dtype=np.int)

        el_dem_stochastic = ED.ElectricalDemand(create_environment,
                                                annualDemand=3000,
                                                method=2,
                                                total_nb_occupants=1,
                                                randomizeAppliances=False,
                                                lightConfiguration=10,
                                                occupancy=occupancy_profile)

        #  Get space heating load curve (in W) per timestep (1 minute)
        el_load_curve = el_dem_stochastic.getDemand(currentValues=False)

        #  Convert power to energy values (W to Ws)
        el_en_demand_curve = create_environment.timer.timeDiscretization * \
                             el_load_curve

        #  Calculate electric energy demand value in kWh
        el_en_demand_curve = el_en_demand_curve / (1000 * 3600)
        el_en_demand_value = np.sum(el_en_demand_curve)
        print('Electrical demand value for 1 person apartment for ' +
              'one year in kWh/a')
        print(el_en_demand_value)

        #  Plausibility check
        assert el_en_demand_value >= 1000, 'Electric energy demand is very low.'
        assert el_en_demand_value <= 3500, 'El. energy demand is very high.'
