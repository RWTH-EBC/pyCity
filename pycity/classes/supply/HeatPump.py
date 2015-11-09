#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 16:45:15 2015

@author: tsz
"""

from __future__ import division
import pycity.classes.supply.HeatingDevice as HeatingDevice
import numpy as np
import pycity.functions.handleData as handleData


class Heatpump(HeatingDevice.HeatingDevice):
    """
    Implementation of the heat pump.
    """
    
    def __init__(self, environment, 
                 tAmbient, tFlow, 
                 heat, power, cop,
                 tMax, 
                 lowerActivationLimit=1):
        """
        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        tAmbient : Array_like
            DESCRIPTION
        tFlow : Array_like
            DESCRIPTION
        heat : Array_like (2 dimensional)
            DESCRIPTION
        power : Array_like (2 dimensional)
            DESCRIPTION
        cop : Array_like (2 dimensional)
            DESCRIPTION
        tMax : Float
            DESCRIPTION
        lowerActivationLimit : float (0 <= lowerActivationLimit <= 1)
            Define the lower activation limit. For example, heat pumps are 
            typically able to operate between 50 % part load and rated load. 
            In this case, lowerActivationLimit would be 0.5
            Two special cases: 
            Linear behavior: lowerActivationLimit = 0
            Two-point controlled: lowerActivationLimit = 1 
        """
        
        qNominal=np.zeros(environment.timer.timestepsHorizon)
        super(Heatpump, self).__init__(environment, 
                                       qNominal,
                                       tMax,
                                       lowerActivationLimit)
        self._kind = "heatpump"
        
        self.tAmbient = tAmbient
        self.tFlow = tFlow
        self.heat = heat
        self.power = power
        
        timestepsTotal = environment.timer.timestepsTotal
        timestepsUsedHorizon = environment.timer.timestepsUsedHorizon
        self.totalPConsumption   = np.zeros(timestepsTotal)
        self.currentPConsumption = np.zeros(timestepsUsedHorizon)
        
    def getNominalValues(self, tFlow):
        """
        Return the nominal electricity consumption, heat output and lower 
        activation limit.
        
        The electricity consumption and heat output are computed by two 
        dimensional interpolation with the ambient temperature and required
        flow temperature as well as the heat pump's characteristics.
        
        Parameters
        ----------
        tFlow : Array_like
            Required flow temperature
            
        Returns
        -------
        pNominal : Array_like
            Nominal electricity consumption at the given flow temperatures and
            the forecast of the current ambient temperature
        qNominal : Array_like
            Nominal heat output at the given flow temperatures and the 
            forecast of the current ambient temperature
        tMax : float
            Maximum flow temperature that can be provided by the heat pump
        lowerActivationLimit : float (0 <= lowerActivationLimit <= 1)
            Define the lower activation limit. For example, heat pumps are 
            typically able to operate between 50 % part load and rated load. 
            In this case, lowerActivationLimit would be 0.5
            Two special cases: 
            Linear behavior: lowerActivationLimit = 0
            Two-point controlled: lowerActivationLimit = 1
            
        Example
        -------
        >>> tFlow = building.getFlowTemperature()
        >>> (pNominal, qNominal, lowerActivationLimit) = hp.getNominals(tFlow)
        """
        # Get weather forecast
        weatherForecast = self.environment.weather.getWeatherForecast
        (tAmbient,) = weatherForecast(getTAmbient=True)
        
        # Two dimensional interpolation is required.
        # Initialize temporary results of the first interpolation
        timestepsHorizon = self.environment.timer.timestepsHorizon
        heat  = np.zeros((timestepsHorizon, len(self.tFlow)))
        power = np.zeros((timestepsHorizon, len(self.tFlow)))
        
        # Compute first interpolation
        for i in range(len(self.tFlow)):
            heat[:,i]  = np.interp(tAmbient, self.tAmbient, self.heat[:,i])
            power[:,i] = np.interp(tAmbient, self.tAmbient, self.power[:,i])
        
        # Initialize final results
        heatNominal  = np.zeros(timestepsHorizon)
        powerNominal = np.zeros(timestepsHorizon)
        for j in range(timestepsHorizon):
            heatNominal[j]  = np.interp(tFlow[j], self.tFlow, heat[j,:])
            powerNominal[j] = np.interp(tFlow[j], self.tFlow, power[j,:])
            
        # Return results
        return (powerNominal, heatNominal, 
                self.tMax, self.lowerActivationLimit)
        
    def getResults(self, currentValues=True):
        """
        Return results.
        
        Parameter
        ---------
        currentValues : boolean, optional
            - True : Return only values for this scheduling period
            - False : Return values for all scheduling periods
        
        Order
        -----
        pConsumption : array_like
            Electricity consumption of the heat pump
        qOutput : array_like
            Heat production of the heat pump
        schedule : array_like
            Operational schedule
        """
        pConsumption = handleData.getValues(currentValues, 
                                            self.currentPConsumption, 
                                            self.totalPConsumption)
        
        return (pConsumption,
                self._getQOutput(currentValues), 
                self._getSchedule(currentValues))

    def setResults(self, pConsumption, qOutput, schedule):
        """
        Save resulting electricty consumption, heat output and 
        operational schedule.
        """
        self._setSchedule(schedule)
        self._setQOutput(qOutput)
        result = handleData.saveResult(self.environment.timer, 
                                       self.currentPConsumption, 
                                       self.totalPConsumption, 
                                       pConsumption)
        (self.currentPConsumption, self.totalPConsumption) = result