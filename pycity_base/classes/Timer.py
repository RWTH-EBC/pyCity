#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 17:05:44 2015

@author: tsz
"""

from __future__ import division


class Timer(object):
    """
    This class just holds the time discretization and the total number of time
    steps. Both are important to initialize the result-storing arrays of most
    other classes.
    """

    def __init__(self, 
                 timeDiscretization=900, 
                 timestepsHorizon=192, 
                 timestepsUsedHorizon=96, 
                 timestepsTotal=35040,
                 initialDay=1):
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
        initialDay : Integer, optional
            Define the initial weekday (`Monday` corresponds to 
            ``initialDay==1``, `Sunday` corresponds to ``initialDay==7``)
        """
        self._kind = "timer"        
        
        self.timeDiscretization   = timeDiscretization
        self.timestepsHorizon     = timestepsHorizon
        self.timestepsUsedHorizon = timestepsUsedHorizon
        self.timestepsTotal       = timestepsTotal
        self.totalDays = int(timestepsTotal * timeDiscretization / 86400)
    
        self.currentTimestep = 0 # max. 365 * 24 * 3600 / timeDiscretization
        self.currentOptimizationPeriod = 0
        self.currentDay      = 0 # max. 365

        self.initialDay = initialDay
        self.currentWeekday = initialDay
        self.currentDayWeekend = self._setWeekend()

    def _setWeekend(self):
        """ Determine if the currend day of the week is on a weekend """
        if self.currentWeekday < 6:
            return False
        else:
            return True

    def update(self):
        """ Increase currentDay and currentTimestep """
        self.currentOptimizationPeriod += 1
        self.currentTimestep += self.timestepsUsedHorizon
        newDay = int(self.currentTimestep * 150 / self.timeDiscretization)
        # 150 = 3600 / 24
        if  newDay > self.currentDay:
            self.currentDay += 1
            self.currentWeekday += 1
            if self.currentWeekday > 7:
                self.currentWeekday = 1
            self.currentDayWeekend = self._setWeekend()
        
    def setCurrentValues(self, currentDay, currentTimestep):
        """
        Set values for the current day and current time step
        """
        self.currentDay      = currentDay
        self.currentTimestep = currentTimestep
    
    def reinit(self, 
               timeDiscretization, 
               timestepsHorizon, 
               timestepsUsedHorizon, 
               timestepsTotal, 
               initialDay,
               overwriteCurrentValues=True):
        """ 
        Reset the timer's attributes
            
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
        initialDay : Integer, optional
            Define the initial weekday (`Monday` corresponds to 
            ``initialDay==1``, `Sunday` corresponds to ``initialDay==7``)
        overwriteCurrentValues : Boolean, optional
            If True: reset currentDay and currentTimestep to 0
            If False: keep values for currentDay and currentTimestep
        """
        
        self.timeDiscretization   = timeDiscretization
        self.timestepsHorizon     = timestepsHorizon
        self.timestepsUsedHorizon = timestepsUsedHorizon
        self.timestepsTotal       = timestepsTotal
        self.currentWeekday       = initialDay
        self.totalDays = int(timestepsTotal * timeDiscretization / 86400)
        self._setWeekend()
        
        if overwriteCurrentValues:
            self.currentDay                = 0
            self.currentTimestep           = 0
            self.currentOptimizationPeriod = 0
