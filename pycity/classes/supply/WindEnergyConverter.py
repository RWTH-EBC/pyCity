#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 03 14:38:14 2015

@author: tsz
"""

from __future__ import division
import numpy as np
import pycity.functions.handleData


class WindEnergyConverter(object):
    """
    """
    
    def __init__(self, 
                 environment,
                 velocity,
                 power,
                 hubHeight=10,
                 roughness=0.1):
        """
        Create a wind energy converter.
        
        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        velocity : Array_like
            Vector of wind velocities for which power data is available.
        power : Array_like
            Vector of power data.
        roughness : Float, optional
            Roughness length as described here: 
            http://wind-data.ch/tools/profile.php?lng=en
            The standard value of 0.1 corresponds to algricultural land with 
            a few buildings and 8 m high hedges seperated by approx. 500 m.
        """
        
        self.environment = environment
        self.__kind = "windenergyconverter"
        
        self.velocity  = velocity
        self.power     = power
        self.hubHeight = hubHeight
        self.roughness = roughness
        
        self.totalPower   = np.zeros(environment.timer.timestepsTotal)
        self.currentPower = np.zeros(environment.timer.timestepsHorizon)

    def __str__(self):
        return str('<Wind energy converter object of pyCity>')

    @property
    def kind(self):
        """
        Return type of pyCity object
        """
        return self.__kind
    
    def _logWindProfile(self, velocity):
        """
        Compute the wind velocity at the wind energy converter's height.
        
        The computations are based on the log wind profile as described here:
        http://wind-data.ch/tools/profile.php?lng=en
        """
        z0 = self.roughness
        h2 = self.hubHeight
        h1 = self.environment.weather.heightVelocityMeasurement
        return (velocity * np.log(h2 / z0) / np.log(h1 / z0))
    
    def getPower(self, currentValues=True, updatePower=True):
        """
        Get the expected power output of the wind energy converter for the 
        current optimization period.
        
        Returns
        -------
        currentPower : Array_like
            Output power in Watt.
        """
        if updatePower:
            currentTimestep = self.environment.timer.currentTimestep
            weatherForecast = self.environment.weather.getWeatherForecast
            (measuredWind,) = weatherForecast(getVWind=True)

            currentWind = self._logWindProfile(measuredWind)
        
            currentPower = np.interp(currentWind, self.velocity, self.power,
                                     right=0)
            
            # `right` ensures that the electricity production is zero, if the 
            # wind speed is higher than the cut-off wind speed (max. wind 
            # speed)
                                     
            self.currentPower = currentPower
            timesteps = self.environment.timer.timestepsHorizon
            self.totalPower[currentTimestep : (currentTimestep + 
                                               timesteps)] = currentPower
       
        return pycity.functions.handleData.getValues(currentValues,
                                              self.currentPower, 
                                              self.totalPower)  
