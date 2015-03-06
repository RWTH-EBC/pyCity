# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 14:55:09 2015

@author: tsz
"""

import classes.Inverter

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

# Create Inverter
p_nominal = 10000
eta = 0.98
inverter = classes.Inverter.Inverter(environment, eta, p_nominal)

# Print results
print
print("Efficiency: "               + str(inverter.getEta()))
print("Maximum electrical input: " + str(inverter.getPNominal()))
