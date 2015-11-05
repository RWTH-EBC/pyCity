#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 17:01:58 2015

@author: tsz
"""

from __future__ import division
import classes.supply.HeatingDevice as HeatingDevice
import numpy as np
import functions.handleData as handleData


class ElectricalHeater(HeatingDevice.HeatingDevice):
    """
    Implementation of the electrical heater
    """
    
    def __init__(self, 
                 environment, 
                 qNominal, 
                 eta, 
                 tMax=85, 
                 lowerActivationLimit=1):
        """
        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        qNominal : array of float
            nominal heat production in Watt
        eta : array of float
            nominal efficiency (without unit)
        tMax : float, optional
            maximum provided temperature in °C
        lowerActivationLimit : float, optional
            see HeatingDevice
        """
        
        super(ElectricalHeater, self).__init__(environment, 
                                               qNominal, 
                                               tMax, 
                                               lowerActivationLimit)
        self._kind = "electricalheater"
        self.eta = eta
        self.pNominal = qNominal / eta
        
        timestepsTotal = environment.timer.timestepsTotal
        timestepsUsedHorizon = environment.timer.timestepsUsedHorizon
        
        self.totalPConsumption   = np.zeros(timestepsTotal)
        self.currentPConsumption = np.zeros(timestepsUsedHorizon)
        
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
            Electricity consumption of the electrical heater
        qOutput : array_like
            Heat production of the electrical heater
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
        
    def getNominalValues(self):
        """
        Return the electrical heater's nominal values as a tuple. 
        
        Order: Electrical efficiency, nominal electricity consumption, nominal 
        heat output, maximum flow temperature and lower activation limit.
        """
        return (self.eta, self.pNominal, self.qNominal, self.tMax, 
                self.lowerActivationLimit)
