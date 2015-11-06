#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 22:07:04 2015

@author: Thomas
"""
from __future__ import division
import numpy as np

import classes.demand.DomesticHotWater as DomesticHotWater

import classes.Timer
import classes.Weather
import classes.Environment
import classes.Prices

timer = classes.Timer.Timer(3600, 8760, 8760, 8760, 0)
weather = classes.Weather.Weather(timer, useTRY=True)
prices = classes.Prices.Prices()

environment = classes.Environment.Environment(timer, weather, prices)

dhw_annex42 = DomesticHotWater.DomesticHotWater(environment,
                                                tFlow=60,
                                                thermal=True,
                                                method=1, # Annex 42
                                                dailyConsumption=200,
                                                supplyTemperature=25)

results = dhw_annex42.getDemand()

print
print("Thermal demand: " + str(results[0]))
print("Required flow temperature: " + str(results[1]))
print

# Compute active occupants for one year
# Max. occupancy is 5 people simultaneously
occupancy = np.random.geometric(p=0.8, size=6*24*365)-1
occupancy = np.minimum(5, occupancy)

dhw_stochastical = DomesticHotWater.DomesticHotWater(environment,
                                                     tFlow=60,
                                                     thermal=True,
                                                     method=2,
                                                     supplyTemperature=20,
                                                     occupancy=occupancy)

import matplotlib.pyplot as plt
ax1=plt.subplot(2,1,1)
plt.step(np.arange(8760)+1, dhw_stochastical.loadcurve, linewidth=2)
plt.ylabel("Heat demand in Watt")
plt.xlim((0,8760))

plt.subplot(2,1,2, sharex=ax1)
plt.step((np.arange(len(occupancy)) * 10+10)/60, occupancy, linewidth=2)
plt.ylabel("Active occupants")
offset = 0.2
plt.ylim((-offset, max(occupancy)+offset))
plt.yticks(range(int(max(occupancy)+1)))

plt.show()

