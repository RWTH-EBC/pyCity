# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 17:01:58 2015

@author: tsz
"""

from __future__ import division

import classes.HeatingDevice
import numpy as np
import functions.handleData

class ElectricalHeater(classes.HeatingDevice.HeatingDevice):
    """
    Implementation of the electrical heater
    """
    
    def __init__(self, environment, qNominal, eta, tMax=85, lowerActivationLimit=1):
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
        
        super(ElectricalHeater, self).__init__(environment, qNominal, tMax, lowerActivationLimit)
        self._kind = "electricalheater"
        self.eta = eta
        self.pNominal = qNominal / eta
        
        self.totalPConsumption = np.zeros(environment.getTimestepsTotal())
        self.currentPConsumption = np.zeros(environment.getTimestepsUsedHorizon())
                
    def setPConsumption(self, pConsumption):
        """ Save the computed electrical output of the CHP unit """
        (self.currentPConsumption, self.totalPConsumption) = functions.handleData.saveResult(self.environment.getTimer(), self.currentPConsumption, self.totalPConsumption, pConsumption)
        
    def getPConsumption(self, currentValues=True):
        """ Return the power consumption. If currentValues=True: current values, else: total values """
        return functions.handleData.getValues(currentValues, self.currentPConsumption, self.totalPConsumption)
        
    def getEta(self):
        """ Return the device's (electrical) efficiency (array of float) """
        return self.eta
    
    def getPNominal(self):
        """ Return the device's nominal electricity consumption (array of float) """
        return self.pNominal
           