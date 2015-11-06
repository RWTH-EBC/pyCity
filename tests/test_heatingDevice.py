#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 14:19:59 2015

@author: tsz
"""

import classes.supply.HeatingDevice as HeatingDevice
import numpy as np

import classes.Timer
import classes.Weather
import classes.Prices
import classes.Environment

# Create environment
timer = classes.Timer.Timer()
weather = classes.Weather.Weather(timer, useTRY=True)
prices = classes.Prices.Prices()
environment = classes.Environment.Environment(timer, weather, prices)

# Create Heating Device
lowerActivationLimit = 0.5
qNominal = 5000
tMax = 70
heater = HeatingDevice.HeatingDevice(environment, 
                                     qNominal, 
                                     tMax, 
                                     lowerActivationLimit)

np.random.seed(0)
someSchedule = np.random.randint(low=0, high=2, 
                                 size=environment.timer.timestepsUsedHorizon)

# Print results
print
print("Lower activation limit: " + str(heater.lowerActivationLimit))
print("Nominal heat output: " + str(heater.qNominal))
print("Maximum flow temperature: " + str(heater.tMax))
print("Previous schedule: "      + str(heater._getSchedule(True)))

heater._setSchedule(someSchedule)
print
print("Current schedule: " + str(heater._getSchedule(True)))