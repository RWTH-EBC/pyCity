from __future__ import division

import unittest
import numpy as np

import pycity.classes.demand.ElectricalDemand as ED

import pycity.classes.Timer
import pycity.classes.Weather
import pycity.classes.Environment
import pycity.classes.Prices


class TestElectricalDemand(unittest.TestCase):
    """
    Test class for pyCity electrical demand object.
    """

    def setUp(self):
        timer = pycity.classes.Timer.Timer(timeDiscretization=60, timestepsTotal=365*24*60, initialDay=1)
        weather = pycity.classes.Weather.Weather(timer, useTRY=True)
        prices = pycity.classes.Prices.Prices()

        self.environment = pycity.classes.Environment.Environment(timer, weather, prices)

    def tearDown(self):
        del self.environment

    def test_method0(self):
        #  energy comparison array
        load_array = np.array ([10, 10, 10, 10, 20, 20, 20, 20])

        el_demand_object = ED.ElectricalDemand(self.environment, method=0, loadcurve=load_array)

        el_load_curve = el_demand_object.getDemand()

        #  Compare arrays
        np.testing.assert_equal(el_load_curve, load_array)

    def test_method1(self):  # Standard load profile
        #  Generate electrical demand object
        el_demand_object = ED.ElectricalDemand(self.environment, method=1, profileType="H0", annualDemand=3000)

        #  Get space heating load curve (in W) per timestep
        el_load_curve = el_demand_object.getDemand(currentValues=False)

        #  Convert power to energy values (W to Ws)
        el_en_demand_curve = self.environment.timer.timeDiscretization * el_load_curve

        #  Calculate electric energy demand value in kWh
        el_en_demand_curve = el_en_demand_curve / (1000*3600)
        el_en_demand_value = np.sum(el_en_demand_curve)

        #  Check if sum of energy demand values is (almost) equal to input
        self.assertAlmostEqual(el_en_demand_value, 3000, delta=3)

    #  TODO: Continue over here
    # def test_method2(self):  # Stochastic load profile
    #
    #     #  Occupancy profile
    #     occupancy_profile = np.ones((365*24*60,), dtype=np.int)
    #
    #     el_dem_stochastic = ED.ElectricalDemand(self.environment, annualDemand=3000,
    #                                         method=2,
    #                                         total_nb_occupants=1,
    #                                         randomizeAppliances=True,
    #                                         lightConfiguration=10,
    #                                         occupancy=occupancy_profile)
    #
    #     #  Get space heating load curve (in W) per timestep (1 minute)
    #     el_load_curve = el_dem_stochastic.getDemand(currentValues=False)
    #
    #     #  Convert power to energy values (W to Ws)
    #     el_en_demand_curve = self.environment.timer.timeDiscretization * el_load_curve
    #     print(len(el_en_demand_curve))
    #
    #     #  Calculate electric energy demand value in kWh
    #     el_en_demand_curve = el_en_demand_curve / (1000*3600)
    #     el_en_demand_value = np.sum(el_en_demand_curve)

if __name__ == '__main__':
    unittest.main()
