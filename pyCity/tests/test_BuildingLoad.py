# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 15:57:11 2015

@author: tsz
"""

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

# Create Load curves
manual_loadcurve = [5, 4, 2, 10, 0, 5] # some random values
manual_load = classes.BuildingLoad.BuildingLoad(environment, "", loadcurve=manual_loadcurve, dataOnFile=False)

path = "inputs\\input_DHW_W.txt"
buildingload = classes.BuildingLoad.BuildingLoad(environment, path, dataOnFile=True)

# Print results
print
print "Manual load curve"
print manual_load.loadcurve

print
print "Load curve from file"
print buildingload.loadcurve