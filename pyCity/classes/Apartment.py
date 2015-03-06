# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 13:30:09 2015

@author: tsz
"""

import numpy as np
import classes.DomesticHotWater
import classes.ElectricalDemand
import classes.SpaceHeating

class Apartment(object):
    """
    Apartments potentially contain:
        Dishwasher, washing machine and demand objects (electricity, domestic hot water and space heating)
    """
    
    def __init__(self, environment):
        """
        Parameter
        ---------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        """
        self._kind = "apartment"
        self.environment = environment
        
        # Initialize electrical appliances
        self.dishwasher = []    
        self.washingmachine = []
        self.hasDishwasher = False
        self.hasWashingmachine = False

        # Create "empty demands"
        timestepsTotal = environment.getTimestepsTotal()
        emptyDHW = classes.DomesticHotWater.DomesticHotWater(environment, 0, loadcurve=np.zeros(timestepsTotal), dataOnFile=False)
        emptyEl  = classes.ElectricalDemand.ElectricalDemand(environment,    loadcurve=np.zeros(timestepsTotal), dataOnFile=False)
        emptySh  = classes.SpaceHeating.SpaceHeating(        environment,    loadcurve=np.zeros(timestepsTotal), dataOnFile=False)
        self.demandDomesticHotWater = emptyDHW
        self.demandElectrical       = emptyEl
        self.demandSpaceheating     = emptySh

    def addEntity(self, entity):
        """
        Add an entity
        
        Example
        -------
        >>> myDW = Dishwasher(...)
        >>> myApartment = Apartment(...)
        >>> myApartment.addDevice(myDW)
        """
        
        # Append new device
        if entity._kind == "electricaldemand":
            self.demandElectrical = entity

        elif entity._kind == "domestichotwater":
            self.demandDomesticHotWater = entity

        elif entity._kind == "spaceheating":
            self.demandSpaceheating = entity

        elif entity._kind == "dishwasher":
            self.dishwasher    = entity
            self.hasDishwasher = True
        
        elif entity._kind == "washingmachine":
            self.washingmachine    = entity
            self.hasWashingmachine = True
        
    def addMultipleEntities(self, entities):
        """
        Add multiple entities to the existing apartment
        
        Parameter
        ---------
        entities: List-like
            List (or tuple) of entities that are added to the apartment
            
        Example
        -------
        >>> myDW = Dishwasher(...)
        >>> myWM = Washingmachine(...)
        >>> myApartment = Apartment(...)
        >>> myApartment.addDevice([myDW, myWM])
        """
        for entity in entities:
            self.addEntity(entity)
        
    def __updateSingleDemand(self, demandType):
        """
        Update (not return!) the electrical, thermal or domestic hot water 
        demand.
        
        Example
        -------
        >>> self.__updateSingleDemand(self.demandElectrical)
        """
        return demandType.getCurrentLoad()
    
    
    def updateDemands(self):
        """ 
        Update (not return!) the electrical, thermal and domestic hot water 
        demands.
        """
        self.__updateSingleDemand(self.demandElectrical)
        self.__updateSingleDemand(self.demandDomesticHotWater)
        self.__updateSingleDemand(self.demandSpaceheating)
        
    def __getSingleDemand(self, demandType):
        """ Return the currentLoad attribute of a demand type """
        return demandType.getCurrentLoad()
            
    def getDemands(self, getElectrical=True, getDomesticHotWater=True, getSpaceheating=True):
        """
        Get apartment's current demands
        
        Parameters
        ----------
        getElectrical : Boolean, optional
            Also return current electrical demand
        getDomesticHotWater : Boolean, optional
            Also return current domestic hot water demand
        getSpaceheating : Boolean, optional
            Also return current space heating demand
            
        Return
        ------
        Current demands. Order: electrical, domestic hot water, space heating
        """
        result = ()
        if getElectrical:
            result += (self.__getSingleDemand(self.demandElectrical),)
        if getDomesticHotWater:
            result += (self.__getSingleDemand(self.demandDomesticHotWater),)
        if getSpaceheating:
            result += (self.__getSingleDemand(self.demandSpaceheating),)
        
        return result
    
    def getDomesticHotWaterThermal(self):
        """ Return if domestic hot water is provided via TES """
        return self.demandDomesticHotWater.getThermalOrElectrical()
        
    def getDomesticHotWaterTemperature(self):
        """ Return required flow temperature array """
        return self.demandDomesticHotWater.getTemperature()
        
    def getApplianceInitialState(self, dishwasher=True):
        """ 
        Return the device's initial state of charge, activity level and 
        previous start indicators.
        
        Parameter
        ---------
        dishwasher : Boolean
            `True` if the initial state of the dishwasher shall be returned.
            `False` if the initial state of the washing machine shall be 
            returned.
        
        If the apartment does not have the specified device, a tuple of zeros 
        is returned
        """
        if dishwasher:
            if self.hasDishwasher:
                return self.dishwasher.getInitialState()
            else:
                return (0, 0, [0])
        else:
            if self.hasWashingmachine:
                return self.washingmachine.getInitialState()
            else:
                return (0, 0, [0])
    
    def getApplianceNominals(self, dishwasher=True):
        """ 
        Return the device's nominals and gains curve
        
        Parameter
        ---------
        dishwasher : Boolean
            `True` if the dishwasher's values shall be returned.
            `False` if the washing machine's data  shall be returned.
        
        Order of result: Maximum capacity, activation border (socMayrun), 
        charging curve (gains), connection to TES unit (ThermalConnection),
        electrical load curve, thermal load curve
        
        If the apartment does not have the specified device, a tuple of zeros 
        is returned
        """
        if dishwasher:
            if self.hasDishwasher:
                return self.dishwasher.getNominals()
            else:
                return (0, 0, np.zeros(self.environment.getTimestepsHorizon()), 0, [], [])
        else:
            if self.hasWashingmachine:
                return self.dishwasher.getNominals()
            else:
                return (0, 0, np.zeros(self.environment.getTimestepsHorizon()), 0, [], [])
                
    def getHasAppliance(self, dishwasher=True):
        """ 
        Return if a dishwasher or washing machine is installed in the apartment.
        
        Parameter
        ---------
        dishwasher : Boolean
            `True` if the dishwasher's values shall be returned.
            `False` if the washing machine's data  shall be returned.
        """
        if dishwasher:
            return self.hasDishwasher
        else:
            return self.hasWashingmachine
            
    def setElectricalApplianceResults(self, soc, power, heat, schedule, dishwasher=True):
        """
        Save the scheduling results of all electrical appliances of the same 
        type (dishwashers or washing machines).
        
        Parameters
        ----------
        soc : Array_like
            State of charge
        power : Array_like
            Electrical power consumption
        heat : Array_like
            Heat consumption
        schedule : Array_like
            Binary scheduling results
        """
        if dishwasher:
            if self.hasDishwasher:
                self.dishwasher.setSoc(soc)
                self.dishwasher.setPConsumption(power)
                self.dishwasher.setQConsumption(heat)
                self.dishwasher.setSchedule(schedule)
        else:
            if self.hasWashingmachine:
                self.washingmachine.setSoc(soc)
                self.washingmachine.setPConsumption(power)
                self.washingmachine.setQConsumption(heat)
                self.washingmachine.setSchedule(schedule)
    