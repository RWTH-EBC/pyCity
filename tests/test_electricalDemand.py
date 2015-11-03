#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 08:43:12 2015

@author: tsz
"""

import classes.demand.ElectricalDemand as ElectricalDemand

import classes.Timer
import classes.Weather
import classes.Environment
import classes.Prices

timer = classes.Timer.Timer()
weather = classes.Weather.Weather(timer, useTRY=True)
prices = classes.Prices.Prices()

environment = classes.Environment.Environment(timer, weather, prices)

el_demand = ElectricalDemand.ElectricalDemand(environment,
                                              method=1, # Standard load profile
                                              profileType="H0",
                                              annualDemand=3000)

results = el_demand.getDemand()

print
print "Electrical demand: " + str(results)


el_dem_stochastic = ElectricalDemand.ElectricalDemand(environment, method=2,
                                                      numberHousehold=3,
                                                      randomizeAppliances=True,
                                                      lightConfiguration=10)
                                                      
