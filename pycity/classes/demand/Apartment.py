#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 13:30:09 2015

@author: tsz
"""

from __future__ import division
import pycity.classes.demand.DomesticHotWater as DHW
import pycity.classes.demand.ElectricalDemand as ElecDemand
import pycity.classes.demand.SpaceHeating as SpaceHeat


class Apartment(object):
    """
    Apartments potentially contain:
        Electricity, domestic hot water and space heating demand
    """

    def __init__(self, environment, nb_of_occupants=None, net_floor_area=None,
                 occupancy_profile=None):
        """
        Parameter
        ---------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        nb_of_occupants : int, optional
            Maximum number of occupants living within apartment (default: None)
        net_floor_area : float, optional
            Net floor area of apartment in m^2 (default: None)
        occupancy_profile : array-like, optional
            Occupancy profile of apartment (default: None)
        """
        self.environment = environment
        self._kind = "apartment"
        self.nb_of_occupants = nb_of_occupants
        self.net_floor_area = net_floor_area
        self.occupancy_profile = occupancy_profile

        # Create empty demands
        self.demandElectrical = ElecDemand.ElectricalDemand(environment,
                                                            method=0,
                                                            annualDemand=0)
        self.demandDomesticHotWater = DHW.DomesticHotWater(environment,
                                                           tFlow=0,
                                                           method=1,
                                                           dailyConsumption=0,
                                                           supplyTemperature=0)
        self.demandSpaceheating = SpaceHeat.SpaceHeating(environment,
                                                         method=1,
                                                         livingArea=0,
                                                         specificDemand=0)

    def addEntity(self, entity):
        """
        Add an entity
        
        Example
        -------
        >>> myDHW = DomesticHotWater(...)
        >>> myApartment = Apartment(...)
        >>> myApartment.addDevice(myDHW)
        """

        if entity._kind == "electricaldemand":
            self.demandElectrical = entity

        elif entity._kind == "domestichotwater":
            self.demandDomesticHotWater = entity

        elif entity._kind == "spaceheating":
            self.demandSpaceheating = entity

    def addMultipleEntities(self, entities):
        """
        Add multiple entities to the existing apartment
        
        Parameter
        ---------
        entities: List-like
            List (or tuple) of entities that are added to the apartment
            
        Example
        -------
        >>> myDHW = DomesticHotWater(...)
        >>> mySH = SpaceHeating(...)
        >>> myApartment = Apartment(...)
        >>> myApartment.addDevice([myDHW, mySH])
        """
        for entity in entities:
            self.addEntity(entity)

    def getDemands(self,
                   getElectrical=True,
                   getDomesticHotWater=True,
                   getSpaceheating=True,
                   currentValues=True):
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
        currentValues : Boolean, optional
            Return the current values (True) or return values for all time 
            steps (False).
            
        Return
        ------
        Current demands. Order: electrical, domestic hot water, space heating
        """
        result = ()
        if getElectrical:
            result += (self.demandElectrical.getDemand(currentValues),)
        if getDomesticHotWater:
            result += (self.demandDomesticHotWater.getDemand(currentValues,
                                                             False),)
        if getSpaceheating:
            result += (self.demandSpaceheating.getDemand(currentValues),)

        return result

    def getTotalElectricalDemand(self, currentValues=True):
        """
        """
        demandElectrical = self.demandElectrical.getDemand(currentValues)
        if not self.demandDomesticHotWater.thermal:
            demandDHW = self.demandDomesticHotWater.getDemand(currentValues,
                                                              False)
            return (demandDHW + demandElectrical)
        else:
            return demandElectrical

    def getTotalThermalDemand(self,
                              currentValues=True,
                              returnTemperature=True):
        """
        """
        demandSpaceHeating = self.demandSpaceheating.getDemand(currentValues)
        if self.demandDomesticHotWater.thermal:
            function = self.demandDomesticHotWater.getDemand
            demandDHW = function(currentValues, returnTemperature)

        if returnTemperature:
            return (demandDHW[0] + demandSpaceHeating, demandDHW[1])
        else:
            return (demandDHW + demandSpaceHeating)
