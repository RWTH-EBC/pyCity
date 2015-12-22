from __future__ import division

import unittest
import numpy as np

import pycity.classes.Timer
import pycity.classes.Weather
import pycity.classes.Prices
import pycity.classes.Environment

import pycity.classes.demand.Apartment as Apartment
import pycity.classes.demand.DomesticHotWater as DomesticHotWater
import pycity.classes.demand.ElectricalDemand as ElectricalDemand
import pycity.classes.demand.SpaceHeating as SpaceHeating


class MyTestCase(unittest.TestCase):

    def setUp(self):
        timer = pycity.classes.Timer.Timer(timeDiscretization=900, timestepsTotal=365*24*4, initialDay=1)
        weather = pycity.classes.Weather.Weather(timer, useTRY=True)
        prices = pycity.classes.Prices.Prices()

        self.environment = pycity.classes.Environment.Environment(timer, weather, prices)

    def tearDown(self):
        del self.environment

    def test_init(self):
        #  Generate apartment object
        test_apartment = Apartment.Apartment(self.environment)

        #  Return all demands
        el_load_curve = test_apartment.getTotalElectricalDemand()
        th_load_curves = test_apartment.getTotalThermalDemand()
        self.assertEqual(np.sum(el_load_curve), 0)
        self.assertEqual(np.sum(th_load_curves[0]), 0)
        self.assertEqual(np.sum(th_load_curves[1]), 0)

    def test_addEntity(self):
        #  Generate heating demand
        heat_demand = SpaceHeating.SpaceHeating(self.environment,
                                            method=1, # Standard load profile
                                            livingArea=100,
                                            specificDemand=150)

        #  Generate apartment object
        test_apartment = Apartment.Apartment(self.environment)

        #  Add entity
        test_apartment.addEntity(heat_demand)

        #  Return heat power (in W)
        heat_load_curve = test_apartment.getTotalThermalDemand(currentValues=False, returnTemperature=False)

        #  Convert to energy values (in kWh)
        th_energy_demand_values = heat_load_curve * self.environment.timer.timeDiscretization / (1000*3600)

        self.assertAlmostEqual(np.sum(th_energy_demand_values), 100*150, places=3)

    def test_addMultipleEntities(self):
        el_demand = ElectricalDemand.ElectricalDemand(self.environment,
                                                  method=1, # Standard load profile
                                                  annualDemand=3000)

        daily_consumption = 70
        t_flow = 70
        supply_temp = 25
        dhw_annex42 = DomesticHotWater.DomesticHotWater(self.environment,
                                                    tFlow=t_flow,
                                                    thermal=True,
                                                    method=1, # Annex 42
                                                    dailyConsumption=daily_consumption,
                                                    supplyTemperature=supply_temp)

        #  Generate apartment object
        test_apartment = Apartment.Apartment(self.environment)
        #  Add multiple entities
        test_apartment.addMultipleEntities([el_demand, dhw_annex42])

        #  Return electrical power (in W)
        el_load_curve = test_apartment.getTotalElectricalDemand(currentValues=False)
        #  Convert to energy values (in kWh)
        el_energy_demand_values = el_load_curve * self.environment.timer.timeDiscretization / (1000*3600)
        self.assertAlmostEqual(np.sum(el_energy_demand_values), 3000, places=3)

        #  Return thermal power
        dhw_heat_load_curve = test_apartment.getTotalThermalDemand(currentValues=False, returnTemperature=False)
        #  Convert to energy values (in kWh)
        th_energy_demand_values = dhw_heat_load_curve * self.environment.timer.timeDiscretization / (1000*3600)
        #  Annual energyy demand value (in kWh)
        dhw_annual_demand = np.sum(th_energy_demand_values)
        #  Reference value in kWh
        reference_value = daily_consumption * 365 * 4180 * (t_flow - supply_temp) / (1000 * 3600)

        self.assertAlmostEqual(dhw_annual_demand, reference_value, places=3)

if __name__ == '__main__':
    unittest.main()
