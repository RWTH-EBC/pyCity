# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 14:35:05 2015

@author: tsz
"""

import classes.ElectricalHeater

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

# Create Electrical Heater
lower_activation_limit = 0.5
q_nominal = 10000
t_max = 90
eta = 0.9
heater = classes.ElectricalHeater.ElectricalHeater(environment, q_nominal, eta, t_max, lower_activation_limit)

# Print results
print
print("Efficiency: "                 + str(heater.getEta()))
print("Maximum heat output: "        + str(heater.getQNominal()))
print("Maximum electricity input: "  + str(heater.getPNominal()))
print("Maximum flow temperature: "   + str(heater.getTMax()))
print("Lower activation limit: "     + str(heater.getLowerActivationLimit()))