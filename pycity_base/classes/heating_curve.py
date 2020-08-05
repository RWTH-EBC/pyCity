#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 11 16:01:52 2015

@author: tsz
"""

from __future__ import division

import numpy as np


class HeatingCurve(object):
    """
    The heating curve presents a functional relationship between ambient 
    temperature and required flow temperature.
    """
    
    def __init__(self, 
                 environment, 
                 m=0.33, 
                 t_set_room=20,
                 t_set_ambient=-10,
                 t_set_flow=55,
                 t_set_return=45):
        """
        Parameters
        ----------
        timer : Timer object
            Pointer to the common Timer object
        m : float, optional
            Heater characteristic. 
            Normally: 0.25 <= m <= 0.40
        t_set_room : integer, optional
            Room's set temperature in °C
        t_set_ambient : integer, optional
            Nominal ambient temperature in °C
        t_set_flow : integer, optional
            Nominal heater flow temperature in °C
        t_set_return : integer, optional
            Nominal heater return temperature in °C
        """
        self._kind = "heatingcurve"
        self.environment = environment
        self.m = m
        self.t_set_room = t_set_room
        self.t_set_ambient = t_set_ambient
        self.t_set_flow = t_set_flow
        self.t_set_return = t_set_return

    @property
    def kind(self):
        return self._kind

    def computeRequiredFlowTemperature(self, 
                                       ambientTemperature, 
                                       smoothingPeriod=1):
        """
        This function is a straight-forward implementation of the heating_curve
        algorithm of the E.ON ERC Modelica library.
        (Cities.Supply.BaseClasses.heating_curve)
        
        Parameters
        ----------
        ambientTemperature : Array-like
            Temperature time series in °C
        smoothingPeriod : Integer, optional
            Over how many days (not time steps!) the moving average is 
            computed
            
        Returns
        -------
        flow_temperature : Array-like
            Temperature time series in °C
        """

        # Smooth the ambient temperature
        dema = self.doubleExponentialMovingAverage
        ambientTemperature = dema(ambientTemperature, smoothingPeriod)

        # Determine design room excess temperature
        dTmN = (self.t_set_flow + self.t_set_return)/2 - self.t_set_room
            
        # Calculate design temperature spread of heating system
        dTN  = self.t_set_flow - self.t_set_return
    
        # Compute load situation of heating system (parameter phi)
        # If room-set-temperature < ambient-temperature, phi equals 0
        phi = np.zeros_like(ambientTemperature)
        index = ambientTemperature <= self.t_set_room
        phi[index] = ((self.t_set_room - ambientTemperature[index])
                       / (self.t_set_room - self.t_set_ambient))
    
        # Compute flow temperature according to heating curve
        return (np.power(phi, 1/(1 + self.m)) * dTmN 
                + 0.5 * phi * dTN + self.t_set_room)

    def doubleExponentialMovingAverage(self, timeseries, smoothingPeriod=1):
        """
        This function implements the double exponential moving average (DEMA), 
        as explained here:
        http://etfhq.com/blog/2010/11/17/double-and-triple-exponential-moving-average/
        
        Parameters
        ----------
        timeseries : Array-like
            Array that represents the "unsmoothed", original data
        smoothingPeriod : Integer, optional
            Over how many days (not time steps!) the moving average is 
            computed
        """
    
        # weightingFactor: Scalar value between 0 and 1.
        # 0 makes the "current" observation irrelevant
        # 1 makes the "previous" observation irrelevant
        time_discretization = self.environment.timer.time_discretization
        smoothingPeriod = 24 * 3600 / time_discretization * smoothingPeriod
        weightingFactor = 2 / (smoothingPeriod + 1)
        
        # Compute exponential moving average (ema) of the given time series
        ema = self.exponential_moving_average(timeseries, weightingFactor)
        # Compute the ema of the previously computed ema
        emaEma = self.exponential_moving_average(ema, weightingFactor)
        
        # Compute double exponential moving average
        return 2 * ema - emaEma
        
    def exponential_moving_average(self, timeseries, alpha):
        """ 
        Compute the exponential moving average for a given timeseries.
    
        Explanation of the statistics behind exponential moving average:
            http://etfhq.com/blog/2010/11/08/exponential-moving-average/
        """
        ema = np.zeros_like(timeseries)  # exponential moving average
        ema[0] = timeseries[0]
        for i in range(1, len(timeseries)):
            ema[i] = ema[i-1] + alpha * (timeseries[i] - ema[i-1])
        return ema
