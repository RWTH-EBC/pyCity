#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Building object of pycity
"""

from __future__ import division

import numpy as np
import warnings


class Building(object):
    """
    Implementation of a building that consists of a single Building Energy 
    System (BES), one controller and multiple apartments
    """
    
    def __init__(self, environment):
        """
        Workflow
        --------
        1 : Create an empty building that only contains the environment 
            pointer
        2 : Add entities such as heating curve or BES, by invoking the 
            addEntity or addMultipleEntities methods.
        
        Parameter
        ---------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        """
        self._kind = "building"
        
        self.environment = environment
        
        self.apartments = []
        self.bes = None
        self.heating_curve = None
        
        self.has_apartment = False
        self.has_bes = False
        self.has_heating_curve = False
        
        self.flow_temperature = np.zeros(environment.timer.timesteps_horizon)

    @property
    def kind(self):
        return self._kind
    
    def addEntity(self, entity):
        """ 
        Add an entity (apartment, BES or heating curve) to the building 
        
        Example
        -------
        >>> myBes = BES(...)
        >>> myBuilding = Building(...)
        >>> myBuilding.addEntity(myBes)
        """
        if entity.kind == "apartment":
            self.apartments.append(entity)
            self.has_apartment = True
        
        elif entity.kind == "bes":
            self.bes = entity
            self.has_bes = True

        elif entity.kind == "heatingcurve":
            self.heating_curve = entity
            self.has_heating_curve = True

    def addMultipleEntities(self, entities):
        """
        Add multiple entities to the existing building
        
        Parameter
        ---------
        entities: List-like
            List (or tuple) of entities that are added to the building
            
        Example
        -------
        >>> myBes = BES(...)
        >>> myHeatingCurve = HeatingCurve(...)
        >>> myBuilding = Building(...)
        >>> myBuilding.addEntity([myBes, myHeatingCurve])
        """
        for entity in entities:
            self.addEntity(entity)    
    
    def get_power_curves(self, current_values=True):
        """
        Get the entire electrical and thermal power curves of all apartments
        in this building.

        Parameters
        ----------
        current_values : bool, optional
            Defines, if only current horizon or all timesteps should be used.
            (default: True)
            False - Use complete number of timesteps
            True - Use horizon

        Order: (resultElectrical, resultThermal)
        """
        # Initialization
        # Demands are zero
        if current_values:
            timesteps = self.environment.timer.timesteps_horizon
        else:
            timesteps = self.environment.timer.timesteps_total
        power_el = np.zeros(timesteps)
        power_th = np.zeros(timesteps)
        
        # Add demands of each apartment
        for apartment in self.apartments:
            # Get entire electrical, domestic hot water and space heating 
            # demand
            (tempEl, tempDhw, tempSh) = apartment.get_power_curves(currentValues=current_values)
            dhwThermal = apartment.demand_domestic_hot_water.thermal
            
            if dhwThermal:
                power_th += tempSh + tempDhw
                power_el += tempEl
            else:
                power_th += tempSh
                power_el += tempEl + tempDhw

        return (power_el, power_th)

    def get_space_heating_power_curve(self, current_values=False):
        """
        Returns space heating power curve

        Parameters
        ----------
        current_values : bool, optional
            Defines, if only current horizon or all timesteps should be used.
            (default: False)
            False - Use complete number of timesteps
            True - Use horizon

        Returns
        -------
        space_heat_power : array-like
            Space heating power curve in W
        """

        #  Initialize array with zeros
        space_heat_power = np.zeros(len(self.apartments[0].demand_space_heating.get_power(currentValues=current_values)))

        # Get power curves of each apartment
        for apartment in self.apartments:
            space_heat_power += apartment.demand_space_heating.get_power(currentValues=current_values)

        return space_heat_power

    def get_electric_power_curve(self, current_values=False):
        """
        Returns electric power curve

        Parameters
        ----------
        current_values : bool, optional
            Defines, if only current horizon or all timesteps should be used.
            (default: False)
            False - Use complete number of timesteps
            True - Use horizon

        Returns
        -------
        el_power_curve : array-like
           Electrical power curve in W
        """

        #  Initialize array with zeros
        el_power_curve = np.zeros(len(self.apartments[0].power_el.get_power(currentValues=current_values)))

        # Get power curves of each apartment
        for apartment in self.apartments:
            el_power_curve += apartment.power_el.get_power(currentValues=current_values)

        return el_power_curve

    def get_dhw_power_curve(self, current_values=False):
        """
        Returns domestic hot water (dhw) power curve

        Parameters
        ----------
        current_values : bool, optional
            Defines, if only current horizon or all timesteps should be used.
            (default: False)
            False - Use complete number of timesteps
            True - Use horizon

        Returns
        -------
        dhw_heat_power : array-like
            DHW power curve in W
        """

        #  Initialize array with zeros
        dhw_heat_power = \
            np.zeros(len(self.apartments[0].demand_domestic_hot_water.
                         get_power(currentValues=current_values,
                                   returnTemperature=False)))

        # Get power curves of each apartment
        for apartment in self.apartments:

            dhw_heat_power += apartment.demand_domestic_hot_water.get_power(
                    currentValues=current_values, returnTemperature=False)

        return dhw_heat_power
        
    def get_occupancy_profile(self):
        """
        Returns occupancy profile of the whole building. Returns None,
        if occupancy object or profile do not exist.

        Returns
        -------
        occupancy_profile : array-like
        """

        for ap in self.apartments:
            if ap.occupancy is None:  # pragma: no cover
                msg = 'Building has no occupancy object.' \
                      ' Cannot return profile.'
                warnings.warn(msg)
                return None
            else:
                if ap.occupancy.occupancy is None:  # pragma: no cover
                    msg = 'Building occupancy object has no occupancy ' \
                          'profile. Cannot return profile.'
                    warnings.warn(msg)
                    return None

        #  Initialize array with zeros
        occupancy_profile = \
            np.zeros(len(self.apartments[0].get_occupancy_profile()))

        # Get power curves of each apartment
        for apartment in self.apartments:

            occupancy_profile += apartment.get_occupancy_profile()

        return occupancy_profile

    def getFlowTemperature(self):
        """ Get the required flow temperature of this building. """
        
        # Get ambient temperature
        relevantPreviousDays = 1  # Number of previous days' weather forecast
                                  # relevant to the heating curve
        numberTimesteps = (relevantPreviousDays * 24 / 
                           self.environment.timer.time_discretization * 3600)
        function = self.environment.weather.getPreviousWeather
        (t_ambient_previous,) = function(numberTimesteps=numberTimesteps,
                                       useTimesteps=True, getTAmbient=True)
                                       
        function = self.environment.weather.getWeatherForecast
        (t_ambient_forecast,) = function(getTAmbient=True)
        t_ambient = np.concatenate((t_ambient_previous, t_ambient_forecast))
        
        # Get flow temperature according to heating curve
        function = self.heating_curve.computeRequiredFlowTemperature
        rawTFlow = function(t_ambient, smoothingPeriod=relevantPreviousDays)
        timesteps_horizon = self.environment.timer.timesteps_horizon
        firstIndex = len(rawTFlow) - timesteps_horizon
        lastIndex = firstIndex + timesteps_horizon
        t_flow = rawTFlow[firstIndex:lastIndex]
        
        # Check if this flow temperature has to be increased at certain time 
        # steps due to domestic hot water
        for apartment in self.apartments:
            t_flow_DHW = (apartment.get_total_th_power())[1]
            t_flow = np.maximum(t_flow, t_flow_DHW)
        
        self.flow_temperature = t_flow
        return t_flow
        
    def getHeatpumpNominals(self):
        """
        Return the nominal electricity consumption, heat output and lower 
        activation limit.
            
        Returns
        -------
        p_nominal : Array_like
            Nominal electricity consumption at the given flow temperatures and 
            the forecast of the current ambient temperature
        q_nominal : Array_like
            Nominal heat output at the given flow temperatures and the 
            forecast of the current ambient temperature
        lower_activation_limit : float (0 <= lower_activation_limit <= 1)
            Define the lower activation limit. For example, heat pumps are 
            typically able to operate between 50 % part load and rated load. 
            In this case, lower_activation_limit would be 0.5
            Two special cases: 
            Linear behavior: lower_activation_limit = 0
            Two-point controlled: lower_activation_limit = 1
        """
        t_flow = self.getFlowTemperature()
        heatpump_nominals = []
        for heatpump in self.bes.heatpump:
            heatpump_nominals.append(heatpump.getNominalValues(t_flow))
        return heatpump_nominals

    def get_number_of_apartments(self):
        """
        Returns number of apartments within chosen building. Of no apartment
        exists, returns None.

        Returns
        -------
        number_of_apartments : int
            Number of apartments within building
        """
        number_of_apartments = None
        if len(self.apartments) > 0:
            number_of_apartments = len(self.apartments)
        return number_of_apartments

    def get_number_of_occupants(self):
        """
        Returns number of occupants of all apartments within building.
        If no occupants exist within building/apartment(s), returns None.

        Returns
        -------
        occupants_total : int
            Total number of occupants
        """
        occupants_total = None  # default value
        if len(self.apartments) != 0:
            occupants_total = 0  # Initial value, if apartments exist
            for apartment in self.apartments:
                if apartment.occupancy is not None:
                    occupants_total += apartment.occupancy.number_occupants
        return occupants_total

    def get_net_floor_area_of_building(self):
        """
        Returns net floor area of building. If undefined (within apartments)
        returns None.

        Returns
        -------
        nfa : float
            Net floor area of building in m^2
        """
        nfa = None
        if len(self.apartments) != 0:
            nfa = 0  # Initial value
            for apartment in self.apartments:
                if apartment.net_floor_area is not None:
                    nfa += apartment.net_floor_area
                else:
                    warnings.warn('Net floor area of one apartment is' +
                                  'defined as None. Please check if this' +
                                  'is correct.')
        return nfa
