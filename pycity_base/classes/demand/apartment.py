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
import pycity_base.classes.demand.space_cooling as SpaceCool


class Apartment(object):
    """
    Apartments potentially contain:
        Electricity, domestic hot water and space heating demand
    """

    def __init__(self, environment, net_floor_area=None, occupancy=None):
        """
        Parameters
        ----------
        environment : environment object
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
                                                    annual_demand=0)
        self.demand_domestic_hot_water = DHW.DomesticHotWater(environment,
                                                              t_flow=0,
                                                              method=1,
                                                              daily_consumption=0,
                                                              supply_temperature=0)
        self.demand_space_heating = SpaceHeat.SpaceHeating(environment,
                                                           method=1,
                                                           living_area=0,
                                                           specific_demand=0)
        self.demand_space_cooling = SpaceCool.SpaceCooling(environment,
                                                           method=1,
                                                           living_area=0,
                                                           specific_demand=0)
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
            - Space cooling demand (entity.kind == "spacecooling")
            - Occupancy (entity.kind == 'occupancy')
            - Room (entity.kind == "room"
        
        Examples
        --------
        >>> myDHW = DomesticHotWater(...)
        >>> myApartment = Apartment(...)
        >>> myApartment.addDevice(myDHW)
        """

        if entity.kind == "electricaldemand":
            self.power_el = entity

        elif entity.kind == "domestichotwater":
            self.demand_domestic_hot_water = entity

        elif entity.kind == "spaceheating":
            self.demand_space_heating = entity

        elif entity.kind == "spacecooling":
            self.demand_space_cooling = entity

        elif entity.kind == 'occupancy':
            self.occupancy = entity

        elif entity.kind == "room":  # pragma: no cover
            self.rooms.append(entity)

        else:  # pragma: no cover
            warnings.warn('Kind of entity is unknown. Entity has not been added!')

    def addMultipleEntities(self, entities):
        """
        Add multiple entities to the existing apartment
        
        Parameters
        ----------
        entities: List-like
            List (or tuple) of entities that are added to the apartment
            
        Examples
        --------
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
                         getSpaceHeating=True,
                         getSpaceCooling=True,
                         currentValues=True):
        """
        Get apartment's current power curves
        
        Parameters
        ----------
        getElectrical : Boolean, optional
            Also return current electrical demand
        getDomesticHotWater : Boolean, optional
            Also return current domestic hot water demand
        getSpaceHeating : Boolean, optional
            Also return current space heating demand
        getSpaceCooling : Boolean, optional
            Also return current space heating demand
        currentValues : Boolean, optional
            Return the current values (True) or return values for all time 
            steps (False).
            
        Returns
        -------
        Current power curves. Order: electrical, domestic hot water,
        space heating
        """
        result = ()
        if getElectrical:
            result += (self.power_el.get_power(currentValues),)
        if getDomesticHotWater:
            result += (self.demand_domestic_hot_water.get_power(currentValues, False),)
        if getSpaceHeating:
            result += (self.demand_space_heating.get_power(currentValues),)
        if getSpaceCooling:
            result += (self.demand_space_cooling.get_power(currentValues),)

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

        Returns
        -------
        If dhw is supplied by electrical supply:
        result_tuple : tuple (power_dhw + power_el)
            Result tuple with power curve

        else (no dhw via electrical device):
        power_el : np.array
            Electrical power curve of apartment
        """
        power_el = self.power_el.get_power(currentValues)
        if not self.demand_domestic_hot_water.thermal:
            power_dhw = self.demand_domestic_hot_water.get_power(currentValues, False)
            return (power_dhw + power_el)
        else:
            return power_el

    def get_total_th_space_heating_power(self,
                                         currentValues=True,
                                         returnTemperature=True):
        """
        Returns the current thermal power curve of the building (space heating
        plus domestic hot water, if thermal hot water device is installed).

        Parameters
        ----------
        currentValues : bool, optional
            Return the current values (True) or return values for all time
            steps (False).
            (default: True)
        returnTemperature : bool, optional
            Defines, if return temperature should be returned
            (default: True)

        Returns
        -------
        If returnTemperature is True:
        result_tuple : tuple (power_dhw[0] + demandSpaceHeating, power_dhw[1])
            Result tuple with thermal power curve and return temperature curve

        else (returnTemperature is False):
        result_tuple : tuple (power_dhw + demandSpaceHeating)
            Thermal power curve of apartment
        """
        demandSpaceHeating = self.demand_space_heating.get_power(currentValues)
        if self.demand_domestic_hot_water.thermal:
            function = self.demand_domestic_hot_water.get_power
            power_dhw = function(currentValues, returnTemperature)

        if returnTemperature:
            return (power_dhw[0] + demandSpaceHeating, power_dhw[1])
        else:
            return (power_dhw + demandSpaceHeating)

    def get_space_heating_power_curve(self, currentValues=True):
        """
        Returns the space heating power curve of the apartment.

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

        return self.demand_space_heating.get_power(currentValues=currentValues)

    def get_space_cooling_power_curve(self, currentValues=True):
        """
        Returns space cooling power curve of the apartment.

        Parameters
        ----------
        currentValues : bool, optional
            Return the current values (True) or return values for all time
            steps (False).
            (default: True)

        Returns
        -------
        space_cool_curve : array-like
            Space cooling power curve
        """

        return self.demand_space_cooling.get_power(currentValues=currentValues)

    def get_el_power_curve(self, currentValues=True):
        """
        Returns the net electrical power curve of the apartment (without space heating, space cooling
        or domestic hot water demand!)

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

        return self.power_el.get_power(currentValues=currentValues)

    def get_dhw_power_curve(self, currentValues=True):
        """
        Returns the domestic hot water power curve of the apartment.

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

        return self.demand_domestic_hot_water.get_power(
            currentValues=currentValues, returnTemperature=False)

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
        Returns the occupancy profile (if occupancy object exists) of the apartment.

        Returns
        -------
        occupancy_profile : array-like
            1d array-like list with number of occupants per timestep
        """
        occupancy_profile = None
        if self.occupancy is not None:
            occupancy_profile = self.occupancy.occupancy
        return occupancy_profile
