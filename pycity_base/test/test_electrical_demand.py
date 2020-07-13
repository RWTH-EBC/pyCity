#!/usr/bin/env python
# coding=utf-8
"""
Electrical demand test
"""

from __future__ import division

import numpy as np

import pycity_base.classes.demand.electrical_demand as ed
import pytest
from pycity_base.test.pycity_fixtures import create_environment, create_occupancy


class TestElectricalDemand(object):
    """
    Test class for pyCity electrical demand object.
    """

    def test_method0(self, create_environment):
        #  energy comparison array
        load_array = np.array([10, 10, 10, 10, 20, 20, 20, 20])

        el_demand_object = ed.ElectricalDemand(create_environment, method=0,
                                               loadcurve=load_array)

        el_load_curve = el_demand_object.get_power()

        #  Compare arrays
        np.testing.assert_equal(el_load_curve, load_array)

    def test_method1(self, create_environment):  # Standard load profile
        #  Generate electrical demand object
        el_demand_object = ed.ElectricalDemand(create_environment, method=1,
                                               profile_type="H0",
                                               annual_demand=3000)

        #  Get space heating load curve (in W) per timestep
        el_load_curve = el_demand_object.get_power(currentValues=False)

        #  Convert power to energy values (W to Ws)
        el_en_demand_curve = create_environment.timer.time_discretization * el_load_curve

        #  Calculate electric energy demand value in kWh
        el_en_demand_curve = el_en_demand_curve / (1000 * 3600)
        el_en_demand_value = np.sum(el_en_demand_curve)

        #  Check if sum of energy demand values is (almost) equal to input
        assert abs(el_en_demand_value - 3000) <= 0.001 * 3000

    # def test_method2(self, create_environment, create_occupancy):
    #     """
    #     Pytest method for stochastic load profiles.
    #
    #     Parameters
    #     ----------
    #     create_environment : object
    #         Environment object (as fixture of pytest)
    #     create_occupancy : object
    #         occupancy object
    #     """
    #
    #     #  Occupancy profile
    #     occupancy_profile = create_occupancy.occupancy
    #     max_occ = np.max(occupancy_profile)
    #
    #     el_dem_stochastic = ed.ElectricalDemand(create_environment,
    #                                             annual_demand=3000,
    #                                             method=2,
    #                                             total_nb_occupants=max_occ,
    #                                             randomize_appliances=False,
    #                                             light_configuration=10,
    #                                             occupancy=occupancy_profile)
    #
    #     #  Get space heating load curve (in W) per timestep (1 minute)
    #     el_load_curve = el_dem_stochastic.get_power(currentValues=False)
    #
    #     #  Convert power to energy values (W to Ws)
    #     el_en_demand_curve = create_environment.timer.time_discretization * \
    #                          el_load_curve
    #
    #     #  Calculate electric energy demand value in kWh
    #     el_en_demand_curve = el_en_demand_curve / (1000 * 3600)
    #     el_en_demand_value = np.sum(el_en_demand_curve)
    #     print('Electrical demand value for 1 person apartment for ' +
    #           'one year in kWh/a')
    #     print(el_en_demand_value)
    #
    #     #  Plausibility check
    #     assert el_en_demand_value >= 1000, 'Electric energy demand is very low.'
    #     assert el_en_demand_value <= 3500, 'El. energy demand is very high.'

    def test_method3(self, create_environment, create_occupancy):
        """
        Pytest method for stochastic load profiles with normalization to
        annual demand

        Parameters
        ----------
        create_environment : object
            Environment object (as fixture of pytest)
        create_occupancy : object
            occupancy object
        """

        ann_demand = 3000

        #  Occupancy profile
        occupancy_profile = create_occupancy.occupancy
        max_occ = np.max(occupancy_profile)

        el_dem_stochastic = ed.ElectricalDemand(create_environment,
                                                annual_demand=ann_demand,
                                                method=2,
                                                total_nb_occupants=max_occ,
                                                randomize_appliances=False,
                                                light_configuration=10,
                                                occupancy=occupancy_profile,
                                                do_normalization=True)

        #  Get space heating load curve (in W) per timestep (1 minute)
        el_load_curve = el_dem_stochastic.get_power(currentValues=False)

        #  Convert power to energy values (W to Ws)
        el_en_demand_curve = create_environment.timer.time_discretization * el_load_curve

        #  Calculate electric energy demand value in kWh
        el_en_demand_curve = el_en_demand_curve / (1000 * 3600)
        el_en_demand_value = sum(el_en_demand_curve)
        print('Electrical demand value for 1 person apartment for ' +
              'one year in kWh/a')
        print(el_en_demand_value)

        assert ann_demand - el_en_demand_value <= 0.001 * ann_demand

    def test_multiple_resolutions(self, create_environment):
        timer = create_environment.timer
        #  Generate electrical demand object
        el_demand_object_1 = ed.ElectricalDemand(create_environment,
                                                 method=1,
                                                 profile_type="H0",
                                                 annual_demand=3000)

        timer.time_discretization = int(timer.time_discretization/2)
        el_demand_object_2 = ed.ElectricalDemand(create_environment,
                                                 method=1,
                                                 profile_type="H0",
                                                 annual_demand=3000)

        #  Get space heating load curve (in W) per timestep
        load_1 = el_demand_object_1.get_power(currentValues=False)
        load_2 = el_demand_object_2.get_power(currentValues=False)

        assert len(load_2) == len(load_1) * 2
        rescaled_load_2 = np.mean(load_2.reshape(-1, 2), axis=1)
        assert np.allclose(rescaled_load_2, load_1)
