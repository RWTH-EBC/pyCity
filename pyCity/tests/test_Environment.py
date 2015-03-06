# -*- coding: utf-8 -*-
"""
Created on Fri Feb 13 11:01:43 2015

@author: tsz
env."""

from __future__ import division

import classes.Timer
import classes.Weather
import classes.Prices
import classes.Environment

timer = classes.Timer.Timer()

pathTRY = "inputs\\weather\\TRY2011\\TRY2010_01_Jahr.dat"
weather = classes.Weather.Weather(timer, pathTRY=pathTRY, useTRY=True)
prices = classes.Prices.Prices()
env = classes.Environment.Environment(timer, weather, prices)

def printResults(env):
    print("Current timestep: " + str(env.timer.currentTimestep))
    print("Ambient temperature for entire horizon: " + str(env.weather.getWeatherForecast(True, False, False, False, False, False)))
    
print 
print("Original environment (0 horizons passed)")
printResults(env)

env.update()
print 
print("Updated environment (1 horizon passed)")
printResults(env)