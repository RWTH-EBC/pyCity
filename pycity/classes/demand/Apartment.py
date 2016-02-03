#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Apartment class of pycity
"""

from __future__ import division
import warnings

import pycity.classes.demand.DomesticHotWater as DHW
import pycity.classes.demand.ElectricalDemand as ElecDemand
import pycity.classes.demand.SpaceHeating as SpaceHeat


class Apartment(object):
    """
    Apartments potentially contain:
        Electricity, domestic hot water and space heating demand
    """

    def __init__(self, environment, net_floor_area=None, occupancy=None):
        """
        Parameter
        ---------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        net_floor_area : float, optional
            Net floor area of apartment in m^2 (default: None)
        occupancy : object
            Occupancy object of pycity (default: None)
        """
        self.environment = environment
        self._kind = "apartment"
        self.net_floor_area = net_floor_area
        self.occupancy = occupancy

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
        Add an entity to apartment.

        Parameters
        ----------
        entity : object
            Entity. Possible objects:
            - Electrical demand (entity._kind == "electricaldemand")
            - Domestic hot water demand (entity._kind == "domestichotwater")
            - Space heating demand (entity._kind == "spaceheating")
            - Occupancy (entity._kind == 'occupancy')
        
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

        elif entity._kind == 'occupancy':
            self.occupancy = entity

        else:
            warnings.warn('Kind of entity is unknown. Entity has not been ' +
                          'added')

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

    def get_max_nb_occupants(self):
        """
        Returns maximum number of occupants within apartment

        Returns
        -------
        max_nb_occupants : int
            Maximum number of occupants
        """
        max_nb_occupants = None
        if self.occupancy is not None:
            max_nb_occupants = self.occupancy.number_occupants
        return max_nb_occupants

    def get_occupancy_profile(self):
        """
        Returns occupancy profile (if occupancy object exists)

        Returns
        -------
        occupancy_profile : array-like
            1d array-like list with number of occupants per timestep
        """
        occupancy_profile = None
        if self.occupancy is not None:
            occupancy_profile = self.occupancy.occupancy
        return occupancy_profile
