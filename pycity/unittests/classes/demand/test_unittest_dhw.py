from __future__ import division

import unittest
import numpy as np

import pycity.classes.demand.DomesticHotWater as dhw

import pycity.classes.Timer
import pycity.classes.Weather
import pycity.classes.Environment
import pycity.classes.Prices


class TestDomesticHotWater(unittest.TestCase):
    """
    Test class for pyCity domestic hot water object.
    """

    def setUp(self):
        timer = pycity.classes.Timer.Timer(timeDiscretization=900, timestepsTotal=365*24*4, initialDay=1)
        weather = pycity.classes.Weather.Weather(timer, useTRY=True)
        prices = pycity.classes.Prices.Prices()

        self.environment = pycity.classes.Environment.Environment(timer, weather, prices)

    def tearDown(self):
        del self.environment

    def test_method1(self):  # IEA annex 42 profile
        tFlow = 60
        supplyTemperature = 25
        dailyConsumption = 50

        dhw_annex42 = dhw.DomesticHotWater(self.environment,
                                                    tFlow=tFlow,
                                                    thermal=True,
                                                    method=1,
                                                    dailyConsumption=dailyConsumption,
                                                    supplyTemperature=supplyTemperature)

        #  Thermal power in W (per 15 minute timestep)
        load_curve = dhw_annex42.getDemand(currentValues=False, returnTemperature=False)

        #  Convert power to energy demand values for dhw (in kWh)
        energy_curve = load_curve * self.environment.timer.timeDiscretization / (1000*3600)

        #  annual energy demand
        annual_dhw_energy_demand = np.sum(energy_curve)

        #  Reference value (in Joule)
        reference_value = 365 * dailyConsumption * 4180 * (tFlow - supplyTemperature)
        #  Convert to kWh
        reference_value = reference_value / (1000 * 3600)

        self.assertAlmostEqual(annual_dhw_energy_demand, reference_value, places=3)

    def test_method2(self):  # Stochastic dhw profiles
        # Compute active occupants for one year
        # Max. occupancy is 5 people simultaneously
        occupancy = np.random.geometric(p=0.8, size=6*24*365)-1
        occupancy = np.minimum(5, occupancy)

        dhw_stochastical = dhw.DomesticHotWater(self.environment,
                                                             tFlow=60,
                                                             thermal=True,
                                                             method=2,
                                                             supplyTemperature=20,
                                                             occupancy=occupancy)

        #  Average daily dhw water consumption in liters
        av_daily_dhw_volume = np.sum(dhw_stochastical.water)/365

        #  Check if av_daily_dhw_volume is within sufficient limits
        self.assertTrue(av_daily_dhw_volume <= 300)
        self.assertTrue(av_daily_dhw_volume >= 50)

if __name__ == '__main__':
    unittest.main()
