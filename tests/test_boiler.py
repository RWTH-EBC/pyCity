#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 14:32:46 2015

@author: tsz
"""
import numpy as np

import classes.Timer
import classes.Weather
import classes.Environment
import classes.Prices

import classes.supply.Boiler as Boiler

# Create environment
timer = classes.Timer.Timer()
weather = classes.Weather.Weather(timer, useTRY=True)
prices = classes.Prices.Prices()
environment = classes.Environment.Environment(timer, weather, prices)

# Create Boiler
lower_activation_limit = 0.5
q_nominal = 10000
t_max = 90
eta = 0.9
heater = Boiler.Boiler(environment, q_nominal, eta, t_max, 
                       lower_activation_limit)

# Print results
print
print("Type: " + heater._kind)
print("Efficiency: "                 + str(heater.eta))
print("Maximum heat output: "        + str(heater.qNominal))
print("Maximum flow temperature: "   + str(heater.tMax))
print("Lower activation limit: "     + str(heater.lowerActivationLimit))

print
print("Nominals: " + str(heater.getNominalValues()))

np.random.seed(0)
result_q = np.random.rand(timer.timestepsUsedHorizon) * q_nominal
result_schedule = np.random.randint(2, size=timer.timestepsUsedHorizon)
heater.setResults(result_q, result_schedule)

results = heater.getResults(True)
print
print("Heat output: " + str(results[0]))
print
print("Schedule: " + str(results[1]))