# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 14:19:59 2015

@author: tsz
"""

import classes.HeatingDevice
import numpy as np

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

# Create Heating Device
lowerActivationLimit = 0.5
heater = classes.HeatingDevice.HeatingDevice(environment, lowerActivationLimit)

someSchedule = np.random.randint(low=0, high=2, size=environment.getTimestepsUsedHorizon())

# Print results
print
print "Lower activation limit: " + str(heater.getLowerActivationLimit())
print "Previous schedule: "      + str(heater.getSchedule(True))

heater.setSchedule(someSchedule)
print "Current schedule: " + str(heater.getSchedule(True))