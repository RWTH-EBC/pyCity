#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to initialize apartment object and add heat, electrical and hot water
demand objects
"""

from __future__ import division
import pycity.classes.Timer
import pycity.classes.Weather
import pycity.classes.Prices
import pycity.classes.Environment

import pycity.classes.demand.Apartment as Apartment
import pycity.classes.demand.DomesticHotWater as DomesticHotWater
import pycity.classes.demand.ElectricalDemand as ElectricalDemand
import pycity.classes.demand.SpaceHeating as SpaceHeating


def run_test():
    #  Generate environment
    timer = pycity.classes.Timer.Timer()
    weather = pycity.classes.Weather.Weather(timer)
    prices = pycity.classes.Prices.Prices()

    environment = pycity.classes.Environment.Environment(timer, weather,
                                                         prices)

    #  Generate heat demand object
    heat_demand = SpaceHeating.SpaceHeating(environment,
                                            method=1,  # Standard load profile
                                            livingArea=146,
                                            specificDemand=166)

    #  Generate electrical demand object
    el_demand = ElectricalDemand.ElectricalDemand(environment,
                                                  method=1,
                                                  # Standard load profile
                                                  annualDemand=3000)

    #  Generate hot water demand object (based on Annex 42 profiles)
    dhw_annex42 = DomesticHotWater.DomesticHotWater(environment,
                                                    tFlow=60,
                                                    thermal=True,
                                                    method=1,  # Annex 42
                                                    dailyConsumption=70,
                                                    supplyTemperature=25)

    #  Initialize apartment object
    apartment = Apartment.Apartment(environment)

    #  Add entities to apartment object
    entities = [heat_demand, el_demand, dhw_annex42]
    apartment.addMultipleEntities(entities)

    print('Get all power curves of apartment (for current horizon):')
    print(apartment.get_power_curves())
    print()

    print('Get space heating power curve for whole year:')
    print(apartment.get_space_heat_power_curve(current_values=False))
    print()

    print('Get electrical power curve for whole year:')
    print(apartment.get_el_power_curve(current_values=False))
    print()

    print('Get hot water power curve for whole year:')
    print(apartment.get_dhw_power_curve(current_values=False))


if __name__ == '__main__':
    #  Run program
    run_test()