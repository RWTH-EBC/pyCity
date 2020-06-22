#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Apartment class of pycity
"""

from __future__ import division

import warnings

import pycity_base.classes.demand.domestic_hot_water as DHW
import pycity_base.classes.demand.electrical_demand as ElecDemand
import pycity_base.classes.demand.space_heating as SpaceHeat


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

        # Create empty power curves using dummy devices
        self.power_el = ElecDemand.ElectricalDemand(environment,
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
        self.rooms = []

    @property
    def kind(self):
        return self._kind

    def addEntity(self, entity):
        """
        Add an entity to apartment.

        Parameters
        ----------
        entity : object
            Entity. Possible objects:
            - Electrical demand (entity.kind == "electricaldemand")
            - Domestic hot water demand (entity.kind == "domestichotwater")
            - Space heating demand (entity.kind == "spaceheating")
            - Occupancy (entity.kind == 'occupancy')
            - Room (entity.kind == "room"
        
        Example
        -------
        >>> myDHW = DomesticHotWater(...)
        >>> myApartment = Apartment(...)
        >>> myApartment.addDevice(myDHW)
        """

        if entity.kind == "electricaldemand":
            self.power_el = entity

        elif entity.kind == "domestichotwater":
            self.demandDomesticHotWater = entity

        elif entity.kind == "spaceheating":
            self.demandSpaceheating = entity

        elif entity.kind == 'occupancy':
            self.occupancy = entity

        elif entity.kind == "room":  # pragma: no cover
            self.rooms.append(entity)

        else:  # pragma: no cover
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

    def get_power_curves(self,
                         getElectrical=True,
                         getDomesticHotWater=True,
                         getSpaceheating=True,
                         currentValues=True):
        """
        Get apartment's current power curves
        
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
        Current power curves. Order: electrical, domestic hot water,
        space heating
        """
        result = ()
        if getElectrical:
            result += (self.power_el.get_power(currentValues),)
        if getDomesticHotWater:
            result += (self.demandDomesticHotWater.get_power(currentValues,
                                                             False),)
        if getSpaceheating:
            result += (self.demandSpaceheating.get_power(currentValues),)

        return result

    def get_total_el_power(self, currentValues=True):
        """
        Returns current el. power curve of building (net electric power plus
        electric hot water, if electric hot water device is installed).

        Parameters
        ----------
        currentValues : bool, optional
            Return the current values (True) or return values for all time
            steps (False).

        Return
        ------
        If dhw is supplied by electrical supply:
        result_tuple : tuple (power_dhw + power_el)
            Result tuple with power curve

        else (no dhw via electrical device):
        power_el : np.array
            Electrical power curve of apartment
        """
        power_el = self.power_el.get_power(currentValues)
        if not self.demandDomesticHotWater.thermal:
            power_dhw = self.demandDomesticHotWater.get_power(currentValues,
                                                              False)
            return (power_dhw + power_el)
        else:
            return power_el

    def get_total_th_power(self,
                           currentValues=True,
                           returnTemperature=True):
        """
        Returns current thermal power curve of building (space heating
        plus thermal hot water, if thermal hot water device is installed).

        Parameters
        ----------
        currentValues : bool, optional
            Return the current values (True) or return values for all time
            steps (False).
            (default: True)
        returnTemperature : bool, optional
            Defines, if return temperature should be returned
            (default: True)

        Return
        ------
        If returnTemperature is True:
        result_tuple : tuple (power_dhw[0] + demandSpaceHeating, power_dhw[1])
            Result tuple with thermal power curve and return temperature curve

        else (returnTemperature is False):
        result_tuple : tuple (power_dhw + demandSpaceHeating)
            Thermal power curve of apartment
        """
        demandSpaceHeating = self.demandSpaceheating.get_power(currentValues)
        if self.demandDomesticHotWater.thermal:
            function = self.demandDomesticHotWater.get_power
            power_dhw = function(currentValues, returnTemperature)

        if returnTemperature:
            return (power_dhw[0] + demandSpaceHeating, power_dhw[1])
        else:
            return (power_dhw + demandSpaceHeating)

    def get_space_heat_power_curve(self, current_values=True):
        """
        Returns space heating power curve of apartment
        Parameters
        ----------
        currentValues : bool, optional
            Return the current values (True) or return values for all time
            steps (False).
            (default: True)
        Returns
        -------
        space_heat_curve : array-like
            Space heating power curve
        """

        return self.demandSpaceheating.get_power(currentValues=current_values)

    def get_el_power_curve(self, current_values=True):
        """
        Returns net electrical power curve of apartment (without space heating
        or hot water demand!)
        Parameters
        ----------
        currentValues : bool, optional
            Return the current values (True) or return values for all time
            steps (False).
            (default: True)
        Returns
        -------
        el_power_curve : array-like
            Electrical power curve
        """

        return self.power_el.get_power(currentValues=current_values)

    def get_dhw_power_curve(self, current_values=True):
        """
        Returns hot water power curve of apartment
        Parameters
        ----------
        currentValues : bool, optional
            Return the current values (True) or return values for all time
            steps (False).
            (default: True)
        Returns
        -------
        el_power_curve : array-like
            Electrical power curve
        """

        return self.demandDomesticHotWater.get_power(
            currentValues=current_values, returnTemperature=False)

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
