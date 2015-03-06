# -*- coding: utf-8 -*-
"""
Created on Wed Feb 11 15:07:39 2015

@author: tsz
"""

import classes.Timer
import classes.Weather
import classes.Prices
import classes.Environment

import classes.Apartment
import classes.Dishwasher
import classes.Washingmachine
import classes.DomesticHotWater
import classes.ElectricalDemand
import classes.SpaceHeating
import numpy as np

def print_attributes(apartment):
    print("Has dishwasher: "     + str(apartment.hasDishwasher))
    print("Has washingmachine: " + str(apartment.hasWashingmachine))

timer = classes.Timer.Timer()

pathTRY = "inputs\\weather\\TRY2011\\TRY2010_01_Jahr.dat"
weather = classes.Weather.Weather(timer, pathTRY=pathTRY, useTRY=True)
prices = classes.Prices.Prices()

environment = classes.Environment.Environment(timer, weather, prices)

# Create demand for domestic hot water
dhw_t_flow_min = 55
path_dhw = "inputs\\input_DHW_W.txt"
dhw = classes.DomesticHotWater.DomesticHotWater(environment, dhw_t_flow_min, thermal=True, pathLoadcurve=path_dhw, dataOnFile=True)

# Create thermal demand
path_th_demand = "inputs\\input_Q_ENEV2009_W.txt"
thermalload = classes.SpaceHeating.SpaceHeating(environment, path_th_demand, dataOnFile=True)

# Creat electrical demand
path_el_demand = "inputs\\input_el_Demand_W.txt"
electricalload = classes.ElectricalDemand.ElectricalDemand(environment, path_el_demand, dataOnFile=True)

# Create electrical appliance
capacity = 1
gains = np.random.random(timer.timestepsTotal) /10 # random gains
socMayrun = 0.8
path_wm_electrical = "inputs\\waschingmachine_purely_electrical.txt"
path_dw_electrical = "inputs\\dishwasher_purely_electrical.txt"
washingmachine = classes.Washingmachine.Washingmachine(environment, capacity, gains, socMayrun, pathElectric=path_wm_electrical, timeEl=1, thermalConnection=False)
dishwasher     = classes.Dishwasher.Dishwasher(environment, capacity, gains, socMayrun, pathElectric=path_dw_electrical, timeEl=1, thermalConnection=False)

# Handle apartment
apartment = classes.Apartment.Apartment(environment)
print
print "Before adding devices"
print_attributes(apartment)

# Add devices/demands to aparment
apartment.addEntity(dhw)
apartment.addEntity(dishwasher)
apartment.addEntity(washingmachine)
apartment.addEntity(thermalload)
apartment.addEntity(electricalload)

print
print "After adding devices"
print_attributes(apartment)

res = apartment.getDemands()