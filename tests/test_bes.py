#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 15:35:37 2015

@author: tsz
"""

import classes.Timer
import classes.Weather
import classes.Environment
import classes.Prices

import classes.supply.Battery as Battery
import classes.supply.BES as BES
import classes.supply.Boiler as Boiler
import classes.supply.CHP as CHP
import classes.supply.ElectricalHeater as ElectricalHeater
import classes.supply.Inverter as Inverter
import classes.supply.PV as PV
import classes.supply.ThermalEnergyStorage as ThermalEnergyStorage

def print_bes_attributes(bes):
    print(("Has Battery: " + str(bes.hasBattery)))
    print(("Has Boiler: " + str(bes.hasBoiler)))
    print(("Has CHP unit: " + str(bes.hasChp)))
    print(("Has Electrical Heater: " + str(bes.hasElectricalHeater)))    
    print(("Has AC/DC inverter: " + str(bes.hasInverterAcdc)))
    print(("Has DC/AC inverter: " + str(bes.hasInverterDcac)))
    print(("Has PV: " + str(bes.hasPv)))
  

timer = classes.Timer.Timer()
weather = classes.Weather.Weather(timer, useTRY=True)
prices = classes.Prices.Prices()

environment = classes.Environment.Environment(timer, weather, prices)

# Create appliances
battery = Battery.Battery(environment, 0.5, 4*3600*1000)
boiler = Boiler.Boiler(environment, 10000, 0.8)
chp = CHP.CHP(environment, 1000, 2000, 0.9)
elHeater = ElectricalHeater.ElectricalHeater(environment, 3000, 0.99)
inverter_ac_dc = Inverter.Inverter(environment, 0.98, 10000, True)
inverter_dc_ac = Inverter.Inverter(environment, 0.98, 10000, False)
pv = PV.PV(environment, 50, 0.15)
tes = ThermalEnergyStorage.ThermalEnergyStorage(environment, 50, 1000, 85)

# Instantiate BES
bes = BES.BES(environment)

# Print "status quo"
print()
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
print()
print("Final BES - after adding devices")
print_bes_attributes(bes)

# Check if objects stored in BES are the same as the original objects:
print()
print("Battery: " + str(battery is bes.battery))
print("Boiler: " + str(boiler is bes.boiler))
print("CHP: " + str(chp is bes.chp))
print("Electrical heater: " + str(elHeater is bes.electricalHeater))
print("Inverter AC to DC: " + str(inverter_ac_dc is bes.inverterAcdc))
print("Inverter DC to AC: " + str(inverter_dc_ac is bes.inverterDcac))
print("PV: " + str(pv is bes.pv))
print("TES: " + str(tes is bes.tes))
