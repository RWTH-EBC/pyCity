# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 16:06:18 2015

@author: tsz
"""

import classes.DomesticHotWater

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
t_flow_min = 55
thermal = True # Connected to the thermal storage, not provided electrically
manual_loadcurve = [5,4,2,10,0,5] # some random values
manual_load = classes.DomesticHotWater.DomesticHotWater(environment, t_flow_min, thermal, "", loadcurve= manual_loadcurve, dataOnFile=False)

path = "inputs\\input_DHW_W.txt"
thermalload = classes.DomesticHotWater.DomesticHotWater(environment, t_flow_min, thermal, path, dataOnFile=True)

# Print results
print
print "Manual load curve"
print manual_load.loadcurve
print ("Minimum flow temperature: " + str(manual_load.getTemperature()))

print
print "Load curve from file"
print thermalload.loadcurve
print ("Minimum flow temperature: " + str(thermalload.getTemperature()))