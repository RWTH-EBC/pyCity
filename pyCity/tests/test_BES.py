# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 15:35:37 2015

@author: tsz
"""

import classes.Timer
import classes.Weather
import classes.Environment
import classes.Prices

import classes.Battery
import classes.BES
import classes.Boiler
import classes.CHP
import classes.ElectricalHeater
import classes.Inverter
import classes.PV
import classes.ThermalEnergyStorage

def print_bes_attributes(bes):
    print("Has Battery: " + str(bes.hasBattery))
    print("Has Boiler: " + str(bes.hasBoiler))
    print("Has CHP unit: " + str(bes.hasChp))
    print("Has Electrical Heater: " + str(bes.hasElectricalHeater))    
    print("Has AC/DC inverter: " + str(bes.hasInverterAcdc))
    print("Has DC/AC inverter: " + str(bes.hasInverterDcac))
    print("Has PV: " + str(bes.hasPv))
  

timer = classes.Timer.Timer()

pathTRY = "inputs\\weather\\TRY2011\\TRY2010_01_Jahr.dat"
weather = classes.Weather.Weather(timer, pathTRY=pathTRY, useTRY=True)
prices = classes.Prices.Prices()

environment = classes.Environment.Environment(timer, weather, prices)

# Create appliances
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

# Print "status quo"
print
print("Original BES - before adding devices")
print_bes_attributes(bes)

# Add appliances to bes
bes.addDevice(battery)
bes.addDevice(boiler)
bes.addDevice(chp)
bes.addDevice(elHeater)
bes.addDevice(inverter_ac_dc)
bes.addDevice(inverter_dc_ac)
bes.addDevice(pv)

bes.addDevice(tes)

# Print current status
print
print("Final BES - after adding devices")
print_bes_attributes(bes)