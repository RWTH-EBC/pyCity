#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 14:29:18 2015

@author: tsz
"""



import numpy as np

class CityDistrict(object):
    """
    """
    
    def __init__(self, environment):
        """
        """
        self.environment = environment
        
        self._kind = "citydistrict"

        # Initialize buildings and renewables (wind energy converters (wec) 
        # and photovoltaic modules (pv))
        self.buildings = []
        self.wec = []
        self.pv = []
        
        
    def addEntity(self, entity):
        """
        Add an entity
        
        Example
        -------
        >>> myBuilding = Building(...)
        >>> myCityDistrict = CityDistrict(...)
        >>> myCityDistrict.addDevice(myBuilding)
        """

        # Append new device (note: there can be multiple wec and/or pv devices)
        if entity._kind == "building":
            self.buildings.append(entity)

        elif entity._kind == "windenergyconverter":
            self.wec.append(entity)

        elif entity._kind == "pv":
            self.pv.append(entity)


    def addMultipleEntities(self, entities):
        """
        Add multiple entities to the existing city district
        
        Parameter
        ---------
        entities: List-like
            List (or tuple) of entities that are added to the city district
            
        Example
        -------
        >>> myPV  = PV(...)
        >>> myWEC = WindEnergyConverter(...)
        >>> myCityDistrict = CityDistrict(...)
        >>> myCityDistrict.addMultipleEntities([myPV, myWEC])
        """
        for entity in entities:
            self.addEntity(entity)


    def _getRESPower(self, generators):
        """
        Get the (aggregated) forecast of all renewable electricity generators.
        """
        power = np.zeros(self.environment.timer.timestepsHorizon)
        for generator in generators:
            power += generator.getPower()

        return power


    def getPVPower(self):
        """
        Get the (aggregated) forecast of all pv units.
        """
        if len(self.pv) == 0:
            return np.zeros(self.environment.timer.timestepsHorizon)
        else:
            return self._getRESPower(self.pv)


    def getWindEnergyConverterPower(self):
        """
        Get the (aggregated) forecast of all wind energy converters.
        """
        if len(self.wec) == 0:
            return np.zeros(self.environment.timer.timestepsHorizon)
        else:
            return self._getRESPower(self.wec)
         
    def getDemands(self):
        """ 
        Get the aggregated electricity and heat demand forecast of all
        buildings.
        
        Order
        -----
        ElectricityDemand : Array_like
            Aggregated electrical demand
        HeatDemand : Array_like
            Aggregated heat demand
        """
        timesteps = self.environment.timer.timestepsHorizon
        demandElectrical = np.zeros(timesteps)
        demandThermal = np.zeros(timesteps)
        
        for building in self.buildings:
            temp = building.getDemands()
            demandElectrical += temp[0]
            demandThermal += temp[1]
        
        return (demandElectrical, demandThermal)
        
    def getFlowTemperatures(self):
        """ 
        Get the aggregated flow temperature forecast.
        """
        timesteps = self.environment.timer.timestepsHorizon
        flowTemperature = np.zeros(timesteps)
        
        for building in self.buildings:
            flowTemperature = np.maximum(flowTemperature,
                                         building.getFlowTemperature())
        
        return flowTemperature
        
        