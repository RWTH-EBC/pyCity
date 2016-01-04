from __future__ import division

import numpy as np

import pycity.classes.demand.DomesticHotWater as dhw
from pycity.test.pycity_fixtures import create_environment


class TestDomesticHotWater(object):
    """
    Test class for pyCity domestic hot water object.
    """

    def test_method1(self, create_environment):  # IEA annex 42 profile
        tFlow = 60
        supplyTemperature = 25
        dailyConsumption = 50

        dhw_annex42 = dhw.DomesticHotWater(create_environment,
                                           tFlow=tFlow,
                                           thermal=True,
                                           method=1,
                                           dailyConsumption=dailyConsumption,
                                           supplyTemperature=supplyTemperature)

        #  Thermal power in W (per 15 minute timestep)
        load_curve = dhw_annex42.getDemand(currentValues=False,
                                           returnTemperature=False)

        #  Convert power to energy demand values for dhw (in kWh)
        energy_curve = load_curve * \
                       create_environment.timer.timeDiscretization / \
                       (1000 * 3600)

        #  annual energy demand
        annual_dhw_energy_demand = np.sum(energy_curve)

        #  Reference value (in Joule)
        reference_value = 365 * dailyConsumption * 4180 * (tFlow -
                                                           supplyTemperature)
        #  Convert to kWh
        reference_value = reference_value / (1000 * 3600)

        assert abs(annual_dhw_energy_demand - reference_value) <= 0.01

    def test_method2(self, create_environment):  # Stochastic dhw profiles
        # Compute active occupants for one year
        # Max. occupancy is 5 people simultaneously
        occupancy = np.random.geometric(p=0.8, size=6 * 24 * 365) - 1
        occupancy = np.minimum(5, occupancy)

        dhw_stochastical = dhw.DomesticHotWater(create_environment,
                                                tFlow=60,
                                                thermal=True,
                                                method=2,
                                                supplyTemperature=20,
                                                occupancy=occupancy)

        #  Average daily dhw water consumption in liters
        av_daily_dhw_volume = np.sum(dhw_stochastical.water) / 365

        #  Check if av_daily_dhw_volume is within sufficient limits
        assert (av_daily_dhw_volume <= 300)
        assert (av_daily_dhw_volume >= 50)
