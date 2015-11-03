#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 11:29:11 2015

@author: tsz
"""

import classes.demand.SpaceHeating as SpaceHeating

import classes.Timer
import classes.Weather
import classes.Environment
import classes.Prices

timer = classes.Timer.Timer()
weather = classes.Weather.Weather(timer, useTRY=True)
prices = classes.Prices.Prices()

environment = classes.Environment.Environment(timer, weather, prices)

hd_slp = SpaceHeating.SpaceHeating(environment,
                                   method=1, # Standard load profile
                                   livingArea=146, 
                                   specificDemand=166, 
                                   singleFamilyHouse=True)

results = hd_slp.getDemand()

print
print "Heat demand: " + str(results)

import matplotlib.pyplot as plt
plt.plot(hd_slp.loadcurve, label="SLP", color="b")
