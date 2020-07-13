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
                 time_discretization=900,
                 timesteps_horizon=192,
                 timesteps_used_horizon=96,
                 timesteps_total=35040,
                 initial_day=1):
        """
        Parameters
        ----------
        time_discretization : Scalar value (preferably integer)
            A value of 3600 corresponds to one hour.
        timesteps_horizon : Scalar integer value
            How many timesteps are in one forecasting horizon?
            If time_discretization=3600, timesteps_horizon=10 would require
            forecasts for the next 10 hours.
        timesteps_used_horizon : Scalar integer value
            How many timesteps are shifted/accepted in each horizon?
            1 <= timesteps_used_horizon <= timesteps_horizon
        timesteps_total : Scalar integer value.
            How long is the entire scheduling period?
            If time_discretization=3600, timesteps_total=8760 is equivalent to a
            full year simulation.
        initial_day : Integer, optional
            Define the initial weekday (`Monday` corresponds to 
            ``initial_day==1``, `Sunday` corresponds to ``initial_day==7``)
        """
        self._kind = "timer"        
        
        self.time_discretization = time_discretization
        self.timesteps_horizon = timesteps_horizon
        self.timesteps_used_horizon = timesteps_used_horizon
        self.timesteps_total = timesteps_total
        self.total_days = int(timesteps_total * time_discretization / 86400)
    
        self.current_timestep = 0  # max. 365 * 24 * 3600 / time_discretization
        self.current_day = 0  # max. 365

        self.initial_day = initial_day
        self.current_weekday = initial_day
        self.current_day_weekend = self._setWeekend()

    @property
    def kind(self):
        return self._kind

    def _setWeekend(self):
        """ Determine if the currend day of the week is on a weekend """
        if self.current_weekday < 6:
            return False
        else:
            return True

    def update(self):
        """ Increase current_day and current_timestep """
        self.current_timestep += self.timesteps_used_horizon
        newDay = int(self.current_timestep * 150 / self.time_discretization)
        # 150 = 3600 / 24
        if newDay > self.current_day:
            self.current_day += 1
            self.current_weekday += 1
            if self.current_weekday > 7:
                self.current_weekday = 1
            self.current_day_weekend = self._setWeekend()
        
    def setCurrentValues(self, current_day, current_timestep):
        """
        Set values for the current day and current time step
        """
        self.current_day = current_day
        self.current_timestep = current_timestep
    
    def reinit(self, 
               time_discretization,
               timesteps_horizon,
               timesteps_used_horizon,
               timesteps_total,
               initial_day,
               overwriteCurrentValues=True):
        """ 
        Reset the timer's attributes
            
        Parameters
        ----------
        time_discretization : Scalar value (preferably integer)
            A value of 3600 corresponds to one hour.
        timesteps_horizon : Scalar integer value
            How many timesteps are in one forecasting horizon?
            If time_discretization=3600, timesteps_horizon=10 would require
            forecasts for the next 10 hours.
        timesteps_used_horizon : Scalar integer value
            How many timesteps are shifted/accepted in each horizon?
            1 <= timesteps_used_horizon <= timesteps_horizon
        timesteps_total : Scalar integer value.
            How long is the entire scheduling period?
            If time_discretization=3600, timesteps_total=8760 is equivalent to a
            full year simulation.
        initial_day : Integer, optional
            Define the initial weekday (`Monday` corresponds to 
            ``initial_day==1``, `Sunday` corresponds to ``initial_day==7``)
        overwriteCurrentValues : Boolean, optional
            If True: reset current_day and current_timestep to 0
            If False: keep values for current_day and current_timestep
        """
        
        self.time_discretization = time_discretization
        self.timesteps_horizon = timesteps_horizon
        self.timesteps_used_horizon = timesteps_used_horizon
        self.timesteps_total = timesteps_total
        self.current_weekday = initial_day
        self.total_days = int(timesteps_total * time_discretization / 86400)
        self._setWeekend()
        
        if overwriteCurrentValues:
            self.current_day = 0
            self.current_timestep = 0
