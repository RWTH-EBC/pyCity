#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 11 15:07:39 2015

@author: tsz
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

    timer = pycity.classes.Timer.Timer()
    weather = pycity.classes.Weather.Weather(timer)
    prices = pycity.classes.Prices.Prices()

    environment = pycity.classes.Environment.Environment(timer, weather, prices)

    heat_demand = SpaceHeating.SpaceHeating(environment,
                                            method=1, # Standard load profile
                                            livingArea=146,
                                            specificDemand=166)

    el_demand = ElectricalDemand.ElectricalDemand(environment,
                                                  method=1, # Standard load profile
                                                  annualDemand=3000)

    dhw_annex42 = DomesticHotWater.DomesticHotWater(environment,
                                                    tFlow=60,
                                                    thermal=True,
                                                    method=1, # Annex 42
                                                    dailyConsumption=70,
                                                    supplyTemperature=25)

    apartment = Apartment.Apartment(environment)

    print(apartment.demandDomesticHotWater)
    print(apartment.power_el)
    print(apartment.demandSpaceheating)

    entities = [heat_demand, el_demand, dhw_annex42]
    apartment.addMultipleEntities(entities)

    print()
    print(apartment.get_power_curves())

    print()
    print(apartment.get_total_el_power())

    print()
    print(apartment.get_total_th_power())

if __name__ == '__main__':
    #  Run program
    run_test()