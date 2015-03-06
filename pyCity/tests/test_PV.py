# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 14:43:11 2015

@author: tsz
"""

from __future__ import division

import classes.PV

import numpy as np
import matplotlib.pyplot as plt

import classes.Timer
import classes.Weather
import classes.Prices
import classes.Environment

# Create environment
timer = classes.Timer.Timer()
pathTRY = "inputs\\weather\\TRY2011\\TRY2010_01_Jahr.dat"
weather = classes.Weather.Weather(timer, pathTRY=pathTRY, useTRY=True)
prices = classes.Prices.Prices()
environment = classes.Environment.Environment(timer, weather, prices)

# Create PV 
area = 20 # m2
eta = 0.2
pv = classes.PV.PV(environment, area, eta)

pvPower = pv.getPower()

# Print results
print
print("Efficiency: " + str(pv.eta))
print("PV area: "    + str(pv.area))

print
print("PV power: " + np.str(pvPower))

# Plot PV power
figure = plt.figure(figsize=(6,6))
plt.plot(range(environment.getTimestepsHorizon()), pvPower, label="PV electricity")
plt.xlabel("Time", fontsize=12)
plt.ylabel("Power", fontsize=12)
plt.xlim((0,environment.getTimestepsHorizon()-1))