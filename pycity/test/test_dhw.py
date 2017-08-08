from __future__ import division

import numpy as np

import pycity_base.classes.demand.DomesticHotWater as dhw
from pycity.test.pycity_fixtures import create_environment, create_occupancy


class TestDomesticHotWater(object):
    """
    Test class for pyCity domestic hot water object.
    """

    def test_method1(self, create_environment):
        """
        Test method for IEA annex 42 domestic hot water profile generator

        Parameters
        ----------
        create_environment : object
            Environment object (pytest fixture)
        """
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
        load_curve = dhw_annex42.get_power(currentValues=False,
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

        print('Reference value in kWh: ', reference_value)
        print('DHW annual energy demand in kWh: ', annual_dhw_energy_demand)

        assert abs(annual_dhw_energy_demand - reference_value) <= 0.01


    def test_method2(self, create_environment, create_occupancy):
        """
        Test method for stochastic domestic hot water profile generator

        Parameters
        ----------
        create_environment : object
            Environment object (pytest fixture)
        """
        occupancy_profile = create_occupancy.occupancy

        dhw_stochastical = dhw.DomesticHotWater(create_environment,
                                                tFlow=60,
                                                thermal=True,
                                                method=2,
                                                supplyTemperature=20,
                                                occupancy=occupancy_profile)

        #  DHW volume flow curve in liters/hour
        volume_flow_curve = dhw_stochastical.water
        #  Recalc into water volume in liters
        water_volume_per_timestep = volume_flow_curve / 3600 * \
                                    create_environment.timer.timeDiscretization
        # Average daily dhw consumption in liters
        av_daily_dhw_volume = np.sum(water_volume_per_timestep) / 365

        #  Check if av_daily_dhw_volume is within sufficient limits
        assert (av_daily_dhw_volume <= 250)
        assert (av_daily_dhw_volume >= 45)
