# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 20:26:30 2015

@author: T_ohne_admin
"""

from __future__ import division

class Environment(object):
    """
    This class keeps track of the simulation time and the weather conditions
    """

    def __init__(self, timer, weather, prices):
        """
        Parameters
        ----------
        timer : Timer object
            Handles current timestep, time discretization and horizon lengths.
        weather : Weather object
            Includes ambient temperature, solar radiation (diffuse, direct),
            relative humidity, air pressure and wind velocity
        prices : Prices object
            Definition of electricity price, remuneration ...
        """
        self._kind = "environment"
        self.timer   = timer
        self.weather = weather
        self.prices  = prices
    
    def getTimer(self):
        """ Return a pointer to the common Timer object """
        return self.timer
    
    def update(self):
        """ Increase current timestep and current day """
        self.timer.update()

    def getPriceInformation(self):
        """
        Return all market information.
        
        Order: Electricity costs, gas costs, CHP revenue, feed-in remuneration
        """
        return self.prices.getAllData()
        
    def getTimeDiscretization(self):
        """ Return the timer's timeDiscretization attribute """
        return self.timer.getTimeDiscretization()
        
    def getTimestepsHorizon(self):
        """ Return the timer's timestepsHorizon attribute """
        return self.timer.getTimestepsHorizon()
        
    def getTimestepsUsedHorizon(self):
        """ Return the timer's timestepsUsedHorizon attribute """
        return self.timer.getTimestepsUsedHorizon()
        
    def getTimestepsTotal(self):
        """ Return the timer's timestepsTotal attribute """
        return self.timer.getTimestepsTotal()
        
    def getCurrentTimestep(self):
        """ Return the currentTimestep attribute """
        return self.timer.getCurrentTimestep()
    
    def getCurrentDay(self):
        """ Return the currentDay attribute """
        return self.timer.getCurrentDay()
        
    def reinit(self, timeDiscretization, timestepsHorizon, timestepsUsedHorizon, timestepsTotal, overwriteCurrentValues=True):
        """ 
        Reset the timer's attributes
            
        Parameters
        ----------
        timeDiscretization: Scalar value (preferably integer)
            A value of 3600 corresponds to one hour.
        timestepsHorizon : Scalar integer value 
            How many timesteps are in one forecasting horizon?
            If timeDiscretization=3600, timestepsHorizon=10 would require 
            forecasts for the next 10 hours.
        timestepsUsedHorizon : Scalar integer value
            How many timesteps are shifted/accepted in each horizon?
            1 <= timestepsUsedHorizon <= timestepsHorizon
        timestepsTotal : Scalar integer value.
            How long is the entire scheduling period?
            If timeDiscretization=3600, timestepsTotal=8760 is equivalent to a 
            full year simulation.
        overwriteCurrentValues : Boolean, optional
            If True: reset currentDay and currentTimestep to 0
            If False: keep values for currentDay and currentTimestep
        """
        self.timer.reinit(timeDiscretization, timestepsHorizon, timestepsUsedHorizon, timestepsTotal, overwriteCurrentValues)
        
    def getWeatherForecast(self, getTAmbient=True, getQDirect=True, getQDiffuse=True, getVWind=True, getPhiAmbient=True, getPAmbient=True):
        """
        Get the current weather forecast
        
        Parameters
        ----------
        getTAmbient : Boolean, optional
            If True, return current ambient temperature
        getQDirect : Boolean, optional
            If True, return current direct radiation
        getQDiffuse : Boolean, optional
            If True, return current diffuse radiation
        getVWind : Boolean, optional
            If True, return current wind velocity
        getPhiAmbient : Boolean, optional
            If True, return relative humidity
        getPAmbient : Boolean, optional
            If True, return ambient pressure
            
        Return
        ------
        The result is returned as a tuple
        """
        return self.weather.getWeatherForecast(getTAmbient, getQDirect, getQDiffuse, getVWind, getPhiAmbient, getPAmbient)
        
    def getPreviousWeather(self, fromTimestep=0, numberTimesteps=0, useTimesteps=True, getTAmbient=True, getQDirect=True, getQDiffuse=True, getVWind=True, getPhiAmbient=True, getPAmbient=True):
        """
        Get previous weather data from 'fromTimestep' up to the current timestep
        
        Parameters
        ----------
        fromTimestep : Integer, optional
            Get weather data from THIS timestep until the current timestep
        numberTimesteps : Integer, optional
            Get weather data for the last numberTimesteps days
        useTimesteps : Boolean, optional
            True: use fromTimestep 
            False: use numberTimesteps
        getTAmbient : Boolean, optional
            If True, return current ambient temperature
        getQDirect : Boolean, optional
            If True, return current direct radiation
        getQDiffuse : Boolean, optional
            If True, return current diffuse radiation
        getVWind : Boolean, optional
            If True, return current wind velocity
        getPhiAmbient : Boolean, optional
            If True, return relative humidity
        getPAmbient : Boolean, optional
            If True, return ambient pressure
            
        Return
        ------
        The result is returned as a tuple
        """
        return self.weather.getPreviousWeather(fromTimestep, numberTimesteps, useTimesteps, getTAmbient, getQDirect, getQDiffuse, getVWind, getPhiAmbient, getPAmbient)