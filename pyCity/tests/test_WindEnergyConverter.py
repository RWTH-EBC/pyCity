# -*- coding: utf-8 -*-
"""
Created on Tue Mar 03 15:50:08 2015

@author: tsz
"""

from __future__ import division

import classes.WindEnergyConverter

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

# Create Wind Energy Converter (Enercon E-126)
nominalPower = 7580
wec = classes.WindEnergyConverter.WindEnergyConverter(environment, useStoredDevice=True, nominalPower=nominalPower)

(currentWind,) = environment.getWeatherForecast(False, False, False, True, False, False) # in m/s
currentPower = wec.getPower() / 1000 # in kW

# Plot wind and WEC power
figure = plt.figure(figsize=(8,6))
ax1 = plt.subplot(211)
ax1.plot(range(environment.getTimestepsHorizon()), currentWind)
plt.xlim((0,environment.getTimestepsHorizon()-1))
plt.ylim((0,12))
plt.ylabel("Wind velocity in m/s", fontsize=12)
ax2 = plt.subplot(212)
ax2.plot(range(environment.getTimestepsHorizon()), currentPower)
plt.xlim((0,environment.getTimestepsHorizon()-1))
plt.xlabel("Timesteps", fontsize=12)
plt.ylabel("Electricity generation in kW", fontsize=12)