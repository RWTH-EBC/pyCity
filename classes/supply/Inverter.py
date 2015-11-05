#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 17:44:16 2015

@author: tsz
"""

import numpy as np
import functions.handleData as handleData
from __future__ import division


class Inverter(object):
    """
    Implementation of the AC-DC / DC-AC inverter
    """
    
    def __init__(self, environment, eta, pNominal, inputAC=True):
        """
        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        eta : float (0 <= eta <= 1)
            efficiency (without unit)
        pNominal : float
            nominal electrical power in Watt
        inputAC : Boolean, optional
            True if input is AC
            False if input is DC
        """
        self._kind = "inverter"
        self.environment = environment
        self.eta = eta
        self.pNominal = pNominal
        self.inputAC = inputAC

        timestepsTotal = environment.timer.timestepsTotal
        timestepsUsedHorizon = environment.timer.timestepsUsedHorizon
        
        self.totalPInput  = np.zeros(timestepsTotal)
        self.totalPOutput = np.zeros(timestepsTotal)
        self.currentPInput  = np.zeros(timestepsUsedHorizon)
        self.currentPOutput = np.zeros(timestepsUsedHorizon)
        
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
        pInput : array_like
            Electricity input of the inverter
        pOutput : array_like
            Electricity output of the inverter
        """
        pInput = handleData.getValues(currentValues, 
                                      self.currentPInput, 
                                      self.totalPInput)
        
        pOutput = handleData.getValues(currentValues, 
                                       self.currentPOutput, 
                                       self.totalPOutput)
        
        return (pInput, pOutput)

    def setResults(self, pInput, pOutput):
        """
        Save electricity input and output of the inverter.
        """
        results = handleData.saveResult(self.environment.timer, 
                                        self.currentPInput, 
                                        self.totalPInput, 
                                        pInput)
        (self.currentPInput, self.totalPInput) = results
        
        results = handleData.saveResult(self.environment.timer, 
                                        self.currentPOutput, 
                                        self.totalPOutput, 
                                        pOutput)
        (self.currentPOutput, self.totalPOutput) = results
        
    def getNominalValues(self):
        """
        Return the inverter's nominal values as a tuple.
        
        Order: Type of inverter, electrical efficiency and nominal input power.
        """
        return (self.inputAC, self.eta, self.pNominal)
