#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 15:17:26 2015

@author: tsz
"""

import classes.Timer
import classes.Weather
import classes.Prices
import classes.Environment

import classes.demand.Apartment as Apartment
import classes.demand.DomesticHotWater as DomesticHotWater
import classes.demand.ElectricalDemand as ElectricalDemand
import classes.demand.SpaceHeating as SpaceHeating
import classes.HeatingCurve as HeatingCurve
import classes.Building as Building
import classes.CityDistrict as CityDistrict

import classes.supply.PV as PV

timer = classes.Timer.Timer()
weather = classes.Weather.Weather(timer)
prices = classes.Prices.Prices()

environment = classes.Environment.Environment(timer, weather, prices)

heat_demand = SpaceHeating.SpaceHeating(environment,
                                        method=1, # Standard load profile
                                        livingArea=146, 
                                        specificDemand=166, 
                                        singleFamilyHouse=True)
                                        
el_demand = ElectricalDemand.ElectricalDemand(environment,
                                              method=1, # Standard load profile
                                              annualDemand=3000)
                                              
dhw_annex42 = DomesticHotWater.DomesticHotWater(environment,
                                                tFlow=60,
                                                thermal=True,
                                                method=1, # Annex 42
                                                dailyConsumption=70,
                                                supplyTemperature=25)
                                        
apartment = Apartment.Apartment(environment)
apartment.addEntity(heat_demand)
apartment.addMultipleEntities([el_demand, dhw_annex42])

heatingCurve = HeatingCurve.HeatingCurve(environment)

building = Building.Building(environment)
entities = [apartment, heatingCurve]
building.addMultipleEntities(entities)

pv = PV.PV(environment, 20, 0.15)

cityDistrict = CityDistrict.CityDistrict(environment)
cityDistrict.addEntity(building)
cityDistrict.addEntity(building)
cityDistrict.addEntity(building)
cityDistrict.addEntity(building)
cityDistrict.addEntity(pv)
cityDistrict.addEntity(pv)
cityDistrict.addEntity(pv)

print()
print(cityDistrict.getDemands())

print()
print(cityDistrict.getFlowTemperatures())

print()
print(cityDistrict.getPVPower())