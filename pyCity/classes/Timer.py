# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 17:05:44 2015

@author: tsz
"""

class Timer(object):
    """
    This class just holds the time discretization and the total number of time
    steps. Both are important to initialize the result-storing arrays of most
    other classes.
    """

    def __init__(self, timeDiscretization=900, timestepsHorizon=192, timestepsUsedHorizon=96, timestepsTotal=35040):
        """
        Parameters
        ----------
        timeDiscretization : Scalar value (preferably integer)
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
        """
        self._kind = "timer"        
        
        self.timeDiscretization   = timeDiscretization
        self.timestepsHorizon     = timestepsHorizon
        self.timestepsUsedHorizon = timestepsUsedHorizon
        self.timestepsTotal       = timestepsTotal
    
        self.currentTimestep = 0 # max. 365 * 24 * 3600 / timeDiscretization 
        self.currentDay      = 0 # max. 365

    def update(self):
        """ Increase currentDay and currentTimestep """
        self.currentDay      += 1
        self.currentTimestep += self.timestepsUsedHorizon
        
    def getTimeDiscretization(self):
        """ Return the timer's timeDiscretization attribute """
        return self.timeDiscretization
        
    def getTimestepsHorizon(self):
        """ Return the timer's timestepsHorizon attribute """
        return self.timestepsHorizon
        
    def getTimestepsUsedHorizon(self):
        """ Return the timer's timestepsUsedHorizon attribute """
        return self.timestepsUsedHorizon
        
    def getTimestepsTotal(self):
        """ Return the timer's timestepsTotal attribute """
        return self.timestepsTotal
        
    def getCurrentTimestep(self):
        """ Return the currentTimestep attribute """
        return self.currentTimestep
    
    def getCurrentDay(self):
        """ Return the currentDay attribute """
        return self.currentDay
        
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
        
        self.timeDiscretization   = timeDiscretization
        self.timestepsHorizon     = timestepsHorizon
        self.timestepsUsedHorizon = timestepsUsedHorizon
        self.timestepsTotal       = timestepsTotal
        
        if overwriteCurrentValues:
            self.currentDay      = 0
            self.currentTimestep = 0
