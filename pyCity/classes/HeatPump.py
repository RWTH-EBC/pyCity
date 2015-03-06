# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 16:45:15 2015

@author: tsz
"""

import classes.HeatingDevice
import numpy as np

class Heatpump(classes.HeatingDevice.HeatingDevice):
    """
    Implementation of the heat pump.
    """
    
    def __init__(self, environment, characteristics, lowerActivationLimit=1):
        """
        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        characteristics : Heat pump characteristics
            DESCRIPTION
        lowerActivationLimit : float (0 <= lowerActivationLimit <= 1)
            Define the lower activation limit. For example, heat pumps are 
            typically able to operate between 50 % part load and rated load. 
            In this case, lowerActivationLimit would be 0.5
            Two special cases: 
            Linear behavior: lowerActivationLimit = 0
            Two-point controlled: lowerActivationLimit = 1 
        """
        self._kind = "heatpump"
        
        (tAmbient, tFlow, heat, power, tMax) = characteristics.getCharacteristics()
        
        super(Heatpump, self).__init__(environment, qNominal=np.ones(environment.getTimestepsHorizon()), tMax=tMax, lowerActivationLimit=lowerActivationLimit)
        
        self.tAmbient = tAmbient
        self.tFlow = tFlow
        self.heat = heat
        self.power = power
        
    def getNominals(self, tFlow):
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
        (tAmbient,) = self.environment.getWeatherForecast(getTAmbient=True, getQDirect=False, getQDiffuse=False, getVWind=False, getPhiAmbient=False, getPAmbient=False)
        
        # Two dimensional interpolation is required.
        # Initialize temporary results of the first interpolation
        heat  = np.zeros((self.environment.getTimestepsHorizon(), len(self.tFlow)))
        power = np.zeros((self.environment.getTimestepsHorizon(), len(self.tFlow)))
        
        # Compute first interpolation
        for i in xrange(len(tFlow)):
            heat[:,i]  = np.interp(tAmbient, self.tAmbient, self.heat[:,i])
            power[:,i] = np.interp(tAmbient, self.tAmbient, self.power[:,i])
        
        # Initialize final results
        heatNominal  = np.zeros(self.environment.getTimestepsHorizon())
        powerNominal = np.zeros(self.environment.getTimestepsHorizon())
        for j in xrange(self.environment.getTimestepsHorizon()):
            heatNominal[j]  = np.interp(tFlow[j], self.tFlow, heat[j,:])
            powerNominal[j] = np.interp(tFlow[j], self.tFlow, power[j,:])
            
        # Return results
        return (powerNominal, heatNominal, self.lowerActivationLimit)