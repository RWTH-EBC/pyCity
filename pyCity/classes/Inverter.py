# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 17:44:16 2015

@author: tsz
"""

import numpy as np
import functions.handleData

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

        timestepsTotal = environment.getTimestepsTotal()
        timestepsUsedHorizon = environment.getTimestepsUsedHorizon()
        
        self.totalPInput  = np.zeros(timestepsTotal)
        self.totalPOutput = np.zeros(timestepsTotal)
        self.currentPInput  = np.zeros(timestepsUsedHorizon)
        self.currentPOutput = np.zeros(timestepsUsedHorizon)
        
    def setPInput(self, pInput):
        """ Save the computed input power """
        (self.currentPInput, self.totalPInput) = functions.handleData.saveResult(self.environment.getTimer(), self.currentPInput, self.totalPInput, pInput)
   
    def setPOutput(self, pOutput):
        """ Save the computed output power """
        (self.currentPOutput, self.totalPOutput) = functions.handleData.saveResult(self.environment.getTimer(), self.currentPOutput, self.totalPOutput, pOutput)
    
    def getInputAC(self):
        """ True: Input is AC, False: Input is DC """
        return self.inputAC
        
    def getEta(self):
        """ Return the inverter's efficiency """
        return self.eta
        
    def getPNominal(self):
        """ Return the inverter's nominal input power """
        return self.pNominal
    
    def getPInput(self, currentValues=True):
        """ Return the electricity input. If currentValues=True: current values, else: total values """
        return functions.handleData.getValues(currentValues, self.currentPInput, self.totalPInput)
        
    def getPOutput(self, currentValues=True):
        """ Return the electricity output. If currentValues=True: current values, else: total values """
        return functions.handleData.getValues(currentValues, self.currentPOutput, self.totalPOutput)
