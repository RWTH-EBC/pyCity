#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 14:59:48 2015

@author: tsz
"""

import numpy as np

import classes.supply.Battery as Battery
import classes.Timer
import classes.Weather
import classes.Prices
import classes.Environment

# Create environment
timer = classes.Timer.Timer()
weather = classes.Weather.Weather(timer)
prices = classes.Prices.Prices()
environment = classes.Environment.Environment(timer, weather, prices)

# Create Boiler
capacity = 4 * 3600 * 1000 # 4 kWh = 4 * 3600*1000 J
socInit = 0.5 * capacity
selfDischarge = 0.02
etaCharge = 0.96
etaDischarge = 0.95
battery = Battery.Battery(environment, socInit, capacity, 
                          selfDischarge, etaCharge, etaDischarge)

# Print results
print()
print(("Initial state of charge: "   + str(battery.socInit)))
print(("Rate of self discharge: "    + str(battery.selfDischarge)))
print(("Efficiency at discharging: " + str(battery.etaDischarge)))
print(("Efficiency at charging: "    + str(battery.etaCharge)))
print(("Battery's total capacity: "  + str(battery.capacity)))

print()
print(("Nominals: " + str(battery.getNominalValues())))

np.random.seed(0)
soc = np.random.rand(timer.timestepsUsedHorizon)
charge = np.random.rand(timer.timestepsUsedHorizon) * capacity / 3600.0
discharge = np.random.rand(timer.timestepsUsedHorizon)  * capacity / 3600.0
battery.setResults(soc, charge, discharge)

results = battery.getResults(True)
print()
print(("SOC: " + str(results[0])))
print()
print(("Charging power: " + str(results[1])))
print()
print(("Disharging power: " + str(results[2])))