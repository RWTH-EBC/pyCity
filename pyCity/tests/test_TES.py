# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 14:37:31 2015

@author: tsz
"""

import classes.ThermalEnergyStorage

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

# Create Heating Device
t_init = 20 # °C
capacity = 1000 # kg
t_max = 95 # °C
t_surroundings = 20 # °C
k_losses = 3 # W/K
tes = classes.ThermalEnergyStorage.ThermalEnergyStorage(environment, t_init, capacity, t_max, t_surroundings, k_losses)

(tesCapacity, tesTMax, tesTSurroundings, tesKLosses) = tes.getStorageParameters()

# Print results
print
print("Initial temperature: "      + str(tes.getTInit()))
print("Water mass: "               + str(tesCapacity))
print("Maximum temperature: "      + str(tesTMax))
print("Surroundings temperature: " + str(tesTSurroundings))
print("Loss factor: "              + str(tesKLosses))