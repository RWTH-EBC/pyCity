# -*- coding: utf-8 -*-
"""
Created on Sun Feb 08 09:53:48 2015

@author: T_ohne_admin
"""

from __future__ import division

import cPickle as pickle
import numpy as np

import tests.test_BuildingOptimizer

import classes.Environment
import classes.Prices
import classes.Weather
import classes.Timer

import classes.Building
import classes.Controller
import classes.HeatingCurve

import classes.Battery
import classes.BES
import classes.Boiler
import classes.CHP
import classes.ElectricalHeater
import classes.Inverter
import classes.PV
import classes.ThermalEnergyStorage

import classes.Apartment
import classes.DomesticHotWater
import classes.SpaceHeating
import classes.ElectricalDemand

import classes.Dishwasher
import classes.Washingmachine

# Create a simple building with a boiler and a small TES unit
# Create environment
timer = classes.Timer.Timer()
pathTRY = "inputs\\weather\\TRY2011\\TRY2010_01_Jahr.dat"
weather = classes.Weather.Weather(timer, pathTRY)
prices = classes.Prices.Prices()
environment = classes.Environment.Environment(timer, weather, prices)

# Create BES and required devices
batSocMax = 4 * 3600 * 1000
battery = classes.Battery.Battery(environment, 0.5*batSocMax, batSocMax, 0.001, 0.95, 0.9)
boiler = classes.Boiler.Boiler(environment, qNominal=25000, eta=0.9, lowerActivationLimit=0.3)
chp = classes.CHP.CHP(environment, 5000, 5000, 0.9, lowerActivationLimit=0.5)
elHeater = classes.ElectricalHeater.ElectricalHeater(environment, 3000, 0.99, lowerActivationLimit=0)
invAcdc = classes.Inverter.Inverter(environment, 0.98, 4000, True)
invDcac = classes.Inverter.Inverter(environment, 0.98, 4000, False)
pv = classes.PV.PV(environment, 20, 0.2)
tes = classes.ThermalEnergyStorage.ThermalEnergyStorage(environment, tInit=50, capacity=1000, tMax=100)
bes = classes.BES.BES(environment)
bes.addMultipleDevices([battery, boiler, tes, chp, invAcdc, invDcac])
bes.addDevice(elHeater)
bes.addDevice(pv)

# Create apartment and required entities
dhwTFlowMin = 55
pathDhw = "inputs\\input_DHW_W.txt"
dhw = classes.DomesticHotWater.DomesticHotWater(environment, dhwTFlowMin, thermal=True, pathLoadcurve=pathDhw, dataOnFile=True)
pathThDemand = "inputs\\input_Q_ENEV2009_W.txt"
thermalload = classes.SpaceHeating.SpaceHeating(environment, pathThDemand, dataOnFile=True)
pathElDemand = "inputs\\input_el_Demand_W.txt"
electricalload = classes.ElectricalDemand.ElectricalDemand(environment, pathElDemand, dataOnFile=True)
pathDwEl = "inputs\\dishwasher_mixed_electrical.txt"
pathDwTh = "inputs\\dishwasher_mixed_thermal.txt"
pathWmEl = "inputs\\washingmachine_mixed_electrical.txt"
pathWmTh = "inputs\\washingmachine_mixed_thermal.txt"
dishwasher = classes.Dishwasher.Dishwasher(environment, 100, np.random.rand(timer.getTimestepsTotal()), 70, 0, timer.getTimeDiscretization(), thermalConnection=True, pathElectric=pathDwEl, pathThermal=pathDwTh, timeEl=1, timeTh=1)
washingmachine = classes.Washingmachine.Washingmachine(environment, 100, np.random.rand(timer.getTimestepsTotal()), 70, 0, timer.getTimeDiscretization(), thermalConnection=True, pathElectric=pathWmEl, pathThermal=pathWmTh, timeEl=1, timeTh=1)
apartment = classes.Apartment.Apartment(environment)
apartment.addMultipleEntities([dhw, thermalload, electricalload])
apartment.addEntity(dishwasher)
#apartment.addEntity(washingmachine)

# Create building and controller
heatingCurve = classes.HeatingCurve.HeatingCurve(environment)
controller = classes.Controller.Controller(environment, heatingCurve)
building = classes.Building.Building(environment)
building.addMultipleEntities([controller, bes, apartment])

while environment.getCurrentDay() <= 2:
    tests.test_BuildingOptimizer.optimize(building, environment)
    environment.update()
    
# Save results
with open("results.pkl", 'wb') as output:
    pickle.dump(building, output, pickle.HIGHEST_PROTOCOL)
    
# Load results
with open("results.pkl", 'rb') as input:
    res = pickle.load(input)

    
    
    
    
    
    