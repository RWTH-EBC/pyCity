# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 16:16:07 2015

@author: tsz
"""

from __future__ import division

import numpy as np
import classes.HeatingDevice
import functions.handleData


class CHP(classes.HeatingDevice.HeatingDevice):
    """
    Implementation of the CHP unit
    """

    def __init__(self, environment, pNominal, qNominal, omega, tMax=85, lowerActivationLimit=1):
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
        super(CHP, self).__init__(environment, qNominal, tMax, lowerActivationLimit)
        
        self._kind = "chp"

        self.totalPOutput   = np.zeros(environment.getTimestepsTotal())
        self.currentPOutput = np.zeros(environment.getTimestepsUsedHorizon())
       
       
    def setPOutput(self, pOutput):
        """ Save the computed electrical output of the CHP unit """
        (self.currentPOutput, self.totalSchedule) = functions.handleData.saveResult(self.environment.getTimer(), self.currentPOutput, self.totalPOutput, pOutput)
    
    def getPOutput(self, currentValues=True):
        """ Return the power output. If currentValues=True: current values, else: total values """
        return functions.handleData.getValues(currentValues, self.currentPOutput, self.totalPOutput)
        
    def getOmega(self):
        """ Return the device's (overall) efficiency (array of float) """
        return self.omega
        
    def getSigma(self):
        """ Return the device's power to heat ratio (array of float) """
        return self.sigma
        
    def getPNominal(self):
        """ Return the device's nominal electricity output (array of float) """
        return self.pNominal