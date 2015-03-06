# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 16:13:54 2015

@author: tsz
"""

import classes.ElectricalAppliance
import numpy as np

import classes.Timer
import classes.Weather
import classes.Prices
import classes.Environment
import classes.BuildingLoad

# Create environment
timer = classes.Timer.Timer()
pathTRY = "inputs\\weather\\TRY2011\\TRY2010_01_Jahr.dat"
weather = classes.Weather.Weather(timer, pathTRY=pathTRY, useTRY=True)
prices = classes.Prices.Prices()
environment = classes.Environment.Environment(timer, weather, prices)

# Create electrical appliance
capacity = 1
gains = np.random.random(timer.getTimestepsTotal()) # random gains
soc_mayrun = 0.8

path_electrical = "inputs\\waschingmachine_purely_electrical.txt"

washingmachine = classes.ElectricalAppliance.ElectricalAppliance(environment, capacity, gains, soc_mayrun, pathElectric=path_electrical, timeEl=1, thermalConnection=False)

print
print "Capacity: "                + str(washingmachine.capacity)
print "SOC may run: "             + str(washingmachine.socMayrun)
print "Gains: "                   + str(washingmachine.gains)
print "Thermal connection: "      + str(washingmachine.thermalConnection)
print "Load curve (electrical): " + str(washingmachine.loadElectrical.loadcurve)
print "Load curve (thermal): "    + str(washingmachine.loadThermal.loadcurve)
