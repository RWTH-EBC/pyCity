# -*- coding: utf-8 -*-
"""
Created on Sun Feb 15 20:37:25 2015

@author: T_ohne_admin
"""

import classes.Timer
import classes.Weather
import classes.Prices
import classes.Environment

import classes.Controller
import classes.Building
import classes.HeatingCurve

import classes.Apartment
import classes.Dishwasher
import classes.Washingmachine
import classes.DomesticHotWater
import classes.ElectricalDemand
import classes.SpaceHeating

import classes.Battery
import classes.BES
import classes.Boiler
import classes.CHP
import classes.ElectricalHeater
import classes.Inverter
import classes.PV
import classes.ThermalEnergyStorage

import numpy as np

def print_entities(building):
    print ("Has controller: "   + str(building.getHasController()))
    print ("Has BES: "          + str(building.getHasBes()))
    print ("Has apartment(s): " + str(building.getHasApartments()))


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
gains = np.random.random(timer.timestepsTotal) # random gains
socMayrun = 0.8
path_wm_electrical = "inputs\\waschingmachine_purely_electrical.txt"
path_dw_electrical = "inputs\\dishwasher_purely_electrical.txt"
washingmachine = classes.Washingmachine.Washingmachine(environment, capacity, gains, socMayrun, pathElectric=path_wm_electrical, timeEl=1, thermalConnection=False)
dishwasher     = classes.Dishwasher.Dishwasher(environment, capacity, gains, socMayrun, pathElectric=path_dw_electrical, timeEl=1, thermalConnection=False)

# Handle apartment
apartment = classes.Apartment.Apartment(environment)
# Add devices/demands to aparment
apartment.addEntity(dhw)
apartment.addEntity(dishwasher)
apartment.addEntity(washingmachine)
apartment.addEntity(thermalload)
apartment.addEntity(electricalload)

# Create BES entities
battery = classes.Battery.Battery(environment, 0.5, 4*3600*1000)
boiler = classes.Boiler.Boiler(environment, 10000, 0.8)
chp = classes.CHP.CHP(environment, 1000, 2000, 0.9)
elHeater = classes.ElectricalHeater.ElectricalHeater(environment, 3000, 0.99)
inverter_ac_dc = classes.Inverter.Inverter(environment, 0.98, 10000, True)
inverter_dc_ac = classes.Inverter.Inverter(environment, 0.98, 10000, False)
pv = classes.PV.PV(environment, 50, 0.15)
tes = classes.ThermalEnergyStorage.ThermalEnergyStorage(environment, 50, 1000, 85)

# Instantiate BES
bes = classes.BES.BES(environment)
# Add appliances to bes
bes.addDevice(battery)
bes.addDevice(boiler)
bes.addDevice(chp)
bes.addDevice(elHeater)
bes.addDevice(inverter_ac_dc)
bes.addDevice(inverter_dc_ac)
bes.addDevice(pv)
bes.addDevice(tes)

# Create a controller
heatingCurve = classes.HeatingCurve.HeatingCurve(environment)
controller = classes.Controller.Controller(environment, heatingCurve)

# Create a building and add BES and one apartment
building = classes.Building.Building(environment)
print 
print "Before adding entities"
print_entities(building)

building.addEntity(controller)
building.addEntity(apartment)
building.addEntity(bes)
print 
print "After adding entities"
print_entities(building)