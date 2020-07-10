#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 03 14:38:14 2015

@author: tsz
"""

from __future__ import division

import numpy as np
from pycity_base.functions import handle_data


class WindEnergyConverter(object):
    """
    """
    
    def __init__(self, 
                 environment,
                 velocity,
                 power,
                 hub_height=10,
                 roughness=0.1):
        """
        Create a wind energy converter.
        
        Parameters
        ----------
        environment : environment object
            Common to all other objects. Includes time and weather instances
        velocity : array-like
            Vector of wind velocities for which power data is available.
        power : array-like
            Vector of power data.
        hub_height : integer, optional
            Height of the turbine over ground.
        roughness : float, optional
            Roughness length as described here: 
            http://wind-data.ch/tools/profile.php?lng=en
            The standard value of 0.1 corresponds to algricultural land with 
            a few buildings and 8 m high hedges seperated by approx. 500 m.
        """
        
        self.environment = environment
        self._kind = "windenergyconverter"
        
        self.velocity = velocity
        self.power = power
        self.hub_height = hub_height
        self.roughness = roughness
        
        self.total_power = np.zeros(environment.timer.timesteps_total)
        self.current_power = np.zeros(environment.timer.timesteps_horizon)

    @property
    def kind(self):
        return self._kind
    
    def _logWindProfile(self, velocity):
        """
        Compute the wind velocity at the wind energy converter's height.
        
        The computations are based on the log wind profile as described here:
        http://wind-data.ch/tools/profile.php?lng=en
        """
        z0 = self.roughness
        h2 = self.hub_height
        h1 = self.environment.weather.height_velocity_measurement
        return (velocity * np.log(h2 / z0) / np.log(h1 / z0))
    
    def getPower(self, currentValues=True, updatePower=True):
        """
        Get the expected power output of the wind energy converter for the 
        current optimization period.
        
        Returns
        -------
        current_power : Array_like
            Output power in Watt.
        """
        if updatePower:
            current_timestep = self.environment.timer.current_timestep
            weatherForecast = self.environment.weather.getWeatherForecast
            (measuredWind,) = weatherForecast(getVWind=True)

            currentWind = self._logWindProfile(measuredWind)
        
            current_power = np.interp(currentWind, self.velocity, self.power, right=0)
            
            # `right` ensures that the electricity production is zero, if the 
            # wind speed is higher than the cut-off wind speed (max. wind 
            # speed)
                                     
            self.current_power = current_power
            timesteps = self.environment.timer.timesteps_horizon
            self.total_power[current_timestep:(current_timestep + timesteps)] = current_power
       
        return handle_data.getValues(currentValues, self.current_power, self.total_power)
