# -*- coding: utf-8 -*-
"""
Created on Tue Feb 24 10:30:35 2015

@author: tsz
"""

import numpy as np

import SONSTIGES.SLPElectrical
import SONSTIGES.SLPThermal

import classes.Timer
import classes.Weather
import classes.Environment
import classes.Prices
timer = classes.Timer.Timer()
pathTRY = "inputs\\weather\\TRY2011\\TRY2010_01_Jahr.dat"
weather = classes.Weather.Weather(timer, pathTRY=pathTRY, useTRY=True)
prices = classes.Prices.Prices()
environment = classes.Environment.Environment(timer, weather, prices)

floorAreas = np.random.randint(low=25, high=500, size=100)
specificElectricalDemand = 31.7
specificThermalDemand    = 166

slpElectrical = SONSTIGES.SLPElectrical.SLPElectrical(environment)
slpThermal    = SONSTIGES.SLPThermal.SLPThermal(environment)

electricalDemands = []
thermalDemands    = []

for area in floorAreas:
    # Divide by 1000 in the scaling factor, as the SLP is scaled to 1000 kWh/a
    electricalDemands.append(slpElectrical.getDemandCurve(area*specificElectricalDemand/1000, False))
    thermalDemands.append(slpThermal.getDemandCurve(area*specificThermalDemand/1000, True, False))
    
electricalDemands = np.array(electricalDemands)
thermalDemands    = np.array(thermalDemands)