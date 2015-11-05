#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 11 16:01:52 2015

@author: tsz
"""



import numpy as np

class HeatingCurve(object):
    """
    The heating curve presents a functional relationship between ambient 
    temperature and required flow temperature
    """
    
    def __init__(self, 
                 environment, 
                 m=0.33, 
                 setRoom=20, 
                 setAmbient=-10, 
                 setFlow=55, 
                 setReturn=45):
        """
        Parameters
        ----------
        timer : Timer object
            Pointer to the common Timer object
        m : float, optional
            Heater characteristic. 
            Normally: 0.25 <= m <= 0.40
        setRoom : integer, optional
            Room's set temperature in °C
        setAmbient : integer, optional
            Nominal ambient temperature in °C
        setFlow : integer, optional
            Nominal heater flow temperature in °C
        setReturn : integer, optional
            Nominal heater return temperature in °C
        """
        self._kind = "heatingcurve"
        self.environment = environment
        self.m           = m
        self.setRoom     = setRoom
        self.setAmbient  = setAmbient
        self.setFlow     = setFlow
        self.setReturn   = setReturn

    def computeRequiredFlowTemperature(self, 
                                       ambientTemperature, 
                                       smoothingPeriod=1):
        """
        This function is a straight-forward implementation of the heatingCurve 
        algorithm of our Modelica library 
        (Cities.Supply.BaseClasses.heatingCurve)
        
        Parameters
        ----------
        ambientTemperature : Array-like
            Temperature time series in °C
        smoothingPeriod : Integer, optional
            Over how many days (not time steps!) the moving average is 
            computed
            
        Return
        ------
        flowTemperature : Array-like
            Temperature time series in °C
        """

        # Smooth the ambient temperature
        dema = self.doubleExponentialMovingAverage
        ambientTemperature = dema(ambientTemperature, smoothingPeriod)

        # Determine design room excess temperature
        dTmN = (self.setFlow + self.setReturn)/2 - self.setRoom
            
        # Calculate design temperature spread of heating system
        dTN  = self.setFlow - self.setReturn   
    
        # Compute load situation of heating system (parameter phi)
        # If room-set-temperature < ambient-temperature, phi equals 0
        phi = np.zeros_like(ambientTemperature)
        index = ambientTemperature <= self.setRoom
        phi[index] = ((self.setRoom - ambientTemperature[index]) 
                       / (self.setRoom - self.setAmbient))
    
        # Compute flow temperature according to heating curve
        return (np.power(phi, 1/(1 + self.m)) * dTmN 
                + 0.5 * phi * dTN + self.setRoom)
        

    def doubleExponentialMovingAverage(self, timeseries, smoothingPeriod=1):
        """
        This function implements the double exponential moving average (DEMA), 
        as eplained here: 
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
        timeDiscretization = self.environment.timer.timeDiscretization
        smoothingPeriod = 24 * 3600 / timeDiscretization * smoothingPeriod
        weightingFactor = 2 / (smoothingPeriod + 1)
        
        # Compute exponential moving average (ema) of the given time series
        ema = self.exponential_moving_average(timeseries, weightingFactor)
        # Compute the ema of the previously computed ema
        emaEma = self.exponential_moving_average(ema, weightingFactor)
        
        # Compute double exponential moving average
        return 2 * ema - emaEma
        
    def exponential_moving_average(self, timeseries, alpha):
        """ 
        Compute the exponential moving average of a given timeseries
    
        Explanation of the statistics behind exponential moving average:
            http://etfhq.com/blog/2010/11/08/exponential-moving-average/
        """
        ema = np.zeros_like(timeseries) # ema: exponential moving average
        ema[0] = timeseries[0]
        for i in range(1, len(timeseries)):
            ema[i] = ema[i-1] + alpha * (timeseries[i] - ema[i-1])
        return ema