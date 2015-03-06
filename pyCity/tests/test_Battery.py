# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 14:59:48 2015

@author: tsz
"""

import classes.Battery
import classes.Timer
import classes.Weather
import classes.Prices
import classes.Environment

# Create environment
timer = classes.Timer.Timer()
weather = classes.Weather.Weather(timer, "inputs\\weather\\TRY2011\\TRY2010_01_Jahr.dat")
prices = classes.Prices.Prices()
environment = classes.Environment.Environment(timer, weather, prices)

# Create Boiler
capacity = 4 * 3600 * 1000 # 4 kWh = 4 * 3600*1000 J
socInit = 0.5 * capacity
selfDischarge = 0.02
etaCharge = 0.96
etaDischarge = 0.95
battery = classes.Battery.Battery(environment, socInit, capacity, selfDischarge, etaCharge, etaDischarge)

# Print results
print
print("Initial state of charge: "   + str(battery.getSocInit()))
print("Rate of self discharge: "    + str(battery.getSelfDischarge()))
print("Efficiency at discharging: " + str(battery.getEtaDischarge()))
print("Efficiency at charging: "    + str(battery.getEtaCharge()))
print("Battery's total capacity: "  + str(battery.getCapacity()))