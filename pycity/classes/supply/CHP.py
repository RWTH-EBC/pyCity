#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 16:16:07 2015

@author: tsz
"""

from __future__ import division
import numpy as np
import pycity.classes.supply.HeatingDevice as HeatingDevice
import pycity.functions.handleData as handleData


class CHP(HeatingDevice.HeatingDevice):
    """
    Implementation of the CHP unit
    """

    def __init__(self, 
                 environment, 
                 pNominal, 
                 qNominal, 
                 omega, 
                 tMax=85, 
                 lowerActivationLimit=1):
        """
        Parameters
        ---------
        environment : environment object
            Common to all other objects. Includes time and weather instances
        pNominal : array of float
            nominal electricity output in Watt
        qNominal : array of float
            nominal heat output in Watt
        omega : array of float
            total efficiency of the CHP unit (without unit)
        tMax : integer, optional
            maximum provided temperature in °C
        lowerActivationLimit : float (0 <= lowerActivationLimit <= 1)
            Define the lower activation limit. For example, heat pumps are 
            typically able to operate between 50 % part load and rated load. 
            In this case, lowerActivationLimit would be 0.5
            Two special cases: 
            Linear behavior: lowerActivationLimit = 0
            Two-point controlled: lowerActivationLimit = 1
        """

        self.pNominal = pNominal
        self.omega = omega
        self.sigma = pNominal / qNominal
        super(CHP, self).__init__(environment, 
                                  qNominal, 
                                  tMax, 
                                  lowerActivationLimit)
        
        self.__kind = "chp"

        self.totalPOutput   = np.zeros(environment.timer.timestepsTotal)
        self.currentPOutput = np.zeros(environment.timer.timestepsUsedHorizon)

    def __str__(self):
        return str('<CHP object of pyCity>')

    @property
    def kind(self):
        """
        Return type of pyCity object
        """
        return self.__kind
       

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
        pOutput : array_like
            Electricity production of the CHP unit
        qOutput : array_like
            Heat production of the CHP unit
        schedule : array_like
            Operational schedule
        """
        pOutput = handleData.getValues(currentValues, 
                                       self.currentPOutput, 
                                       self.totalPOutput)
        
        return (pOutput,
                self._getQOutput(currentValues), 
                self._getSchedule(currentValues))

    def setResults(self, pOutput, qOutput, schedule):
        """
        Save resulting electricty, heat output and operational schedule.
        """
        self._setSchedule(schedule)
        self._setQOutput(qOutput)
        result = handleData.saveResult(self.environment.timer, 
                                       self.currentPOutput, 
                                       self.totalPOutput, 
                                       pOutput)
        (self.currentPOutput, self.totalPOutput) = result
        
    def getNominalValues(self):
        """
        Return the CHP unit's nominal values as a tuple. 
        
        Order: Overall efficiency, power to heat ratio, nominal electricity 
        output, nominal heat output, maximum flow temperature and lower 
        activation limit.
        """
        return (self.omega, self.sigma, self.pNominal, self.qNominal, 
                self.tMax, self.lowerActivationLimit)
        