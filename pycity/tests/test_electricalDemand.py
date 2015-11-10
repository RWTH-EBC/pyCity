#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 08:43:12 2015

@author: tsz
"""

from __future__ import division
import pycity.classes.demand.ElectricalDemand as ED

import pycity.classes.Timer
import pycity.classes.Weather
import pycity.classes.Environment
import pycity.classes.Prices

import pycity.classes.demand.Occupancy

def run_test():
    timer = pycity.classes.Timer.Timer()
    weather = pycity.classes.Weather.Weather(timer, useTRY=True)
    prices = pycity.classes.Prices.Prices()

    environment = pycity.classes.Environment.Environment(timer, weather, prices)

    el_demand = ED.ElectricalDemand(environment,
                                    method=1, # Standard load profile
                                    profileType="H0",
                                    annualDemand=3000)

    results = el_demand.getDemand()

    print()
    print("Electrical demand: " + str(results))



    occupancy = pycity.classes.demand.Occupancy.Occupancy(environment,
                                                   number_occupants=3)

    el_dem_stochastic = ED.ElectricalDemand(environment,
                                            method=2,
                                            numberHousehold=3,
                                            randomizeAppliances=True,
                                            lightConfiguration=10,
                                            occupancy=occupancy.occupancy)

if __name__ == '__main__':
    #  Run program
    run_test()