from __future__ import division

import unittest
import numpy as np

import pycity.classes.demand.SpaceHeating as SpaceHeating

import pycity.classes.Timer
import pycity.classes.Weather
import pycity.classes.Environment
import pycity.classes.Prices


class TestSpaceheating(unittest.TestCase):
    """
    Test class for pyCity Spaceheating object.
    """

    def setUp(self):
        timer = pycity.classes.Timer.Timer(timeDiscretization=3600, timestepsHorizon=24, timestepsUsedHorizon=96,
                                           timestepsTotal=3600*24*365, initialDay=1)
        weather = pycity.classes.Weather.Weather(timer, useTRY=True)
        prices = pycity.classes.Prices.Prices()

        self.environment = pycity.classes.Environment.Environment(timer, weather, prices)

    def tearDown(self):
        del self.environment

    def test_method0(self):
        #  energy comparison array
        load_array = np.array ([10, 10, 10, 10, 20, 20, 20, 20])

        #  Space heating object
        spaceheating = SpaceHeating.SpaceHeating(self.environment, method=0, loadcurve=load_array)

        #  Return load curve of space heating object
        space_heat_load_curve = spaceheating.getDemand(currentValues=False)

        #  Compare arrays
        np.testing.assert_equal(space_heat_load_curve, load_array)

    def test_method1(self):  # Standard load profile
        #  Generate space heating object
        spaceheating = SpaceHeating.SpaceHeating(self.environment, method=1, livingArea=100, specificDemand=150)

        #  Get space heating load curve (in W) per timestep
        space_heat_load_curve = spaceheating.getDemand(currentValues=False)

        #  Check if sum of energy demand values is (almost) equal to input
        self.assertAlmostEqual(np.sum(space_heat_load_curve)/1000, 150*100, delta=3)

if __name__ == '__main__':
    unittest.main()
