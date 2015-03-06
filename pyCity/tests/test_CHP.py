# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 14:25:16 2015

@author: tsz
"""

import classes.CHP

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

# Create CHP
lower_activation_limit = 0.5
q_nominal = 10000
t_max = 90
p_nominal = 6000
omega = 0.9
heater = classes.CHP.CHP(environment, p_nominal, q_nominal, omega, t_max, lower_activation_limit)

# Print results
print
print("Maximum electricity output: " + str(heater.getPNominal()))
print("Total efficiency: "           + str(heater.getOmega()))
print("Power to heat ratio: "        + str(heater.getSigma()))
print("Maximum heat output: "        + str(heater.getQNominal()))
print("Maximum flow temperature: "   + str(heater.getTMax()))
print("Lower activation limit: "     + str(heater.getLowerActivationLimit()))