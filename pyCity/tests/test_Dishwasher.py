# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 09:26:20 2015

@author: tsz
"""

from __future__ import division

import numpy as np

import tests.test_DishwasherOptimizer as optimizer

import classes.Environment
import classes.Prices
import classes.Weather
import classes.Timer

import classes.PV
import classes.Dishwasher

# Create a simple building with a boiler and a small TES unit
# Create environment
timer = classes.Timer.Timer()
pathTRY = "inputs\\weather\\TRY2011\\TRY2010_01_Jahr.dat"
weather = classes.Weather.Weather(timer, pathTRY)
prices = classes.Prices.Prices()
environment = classes.Environment.Environment(timer, weather, prices)

# PV and dishwasher
pv = classes.PV.PV(environment, 20, 0.2)
pathDwEl = "inputs\\dishwasher_purely_electrical.txt"
dishwasher = classes.Dishwasher.Dishwasher(environment, 30, np.random.rand(timer.getTimestepsTotal()), 20, 0, timer.getTimeDiscretization(), timeEl=1, thermalConnection=False, pathElectric=pathDwEl)

while environment.getCurrentDay() <= 5:
    optimizer.optimize(pv, dishwasher, environment)
    environment.update()

schedule = dishwasher.currentSchedule
p_cons   = dishwasher.currentPConsumption
soc      = dishwasher.currentSoc