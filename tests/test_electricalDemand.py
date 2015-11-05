#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 08:43:12 2015

@author: tsz
"""

from __future__ import division
import classes.demand.ElectricalDemand as ED

import classes.Timer
import classes.Weather
import classes.Environment
import classes.Prices

import classes.demand.Occupancy


timer = classes.Timer.Timer()
weather = classes.Weather.Weather(timer, useTRY=True)
prices = classes.Prices.Prices()

environment = classes.Environment.Environment(timer, weather, prices)

el_demand = ED.ElectricalDemand(environment,
                                method=1, # Standard load profile
                                profileType="H0",
                                annualDemand=3000)

results = el_demand.getDemand()

print()
print("Electrical demand: " + str(results))



occupancy = classes.demand.Occupancy.Occupancy(environment, 
                                               number_occupants=3)

el_dem_stochastic = ED.ElectricalDemand(environment, 
                                        method=2,
                                        numberHousehold=3,
                                        randomizeAppliances=True,
                                        lightConfiguration=10,
                                        occupancy=occupancy.occupancy)
