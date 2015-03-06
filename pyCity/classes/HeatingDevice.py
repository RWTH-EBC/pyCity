# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 15:57:15 2015

@author: tsz
"""

import numpy as np
import functions.handleData

class HeatingDevice(object):
    """
    Superclass of all heating devices.
    """
   
    def __init__(self, environment, qNominal, tMax=85, lowerActivationLimit=1):
        """
        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        qNominal : Array of float
            Nominal heat output in Watt
        tMax : Float, optional 
            Maximum provided temperature in °C
        lowerActivationLimit : float (0 <= lowerActivationLimit <= 1)
            Define the lower activation limit. For example, heat pumps are 
            typically able to operate between 50 % part load and rated load. 
            In this case, lowerActivationLimit would be 0.5
            Two special cases: 
            Linear behavior: lowerActivationLimit = 0
            Two-point controlled: lowerActivationLimit = 1
        """
        self._kind = "heatingdevice"

        timestepsTotal = environment.getTimestepsTotal()
        timestepsUsedHorizon = environment.getTimestepsUsedHorizon()
        
        self.environment = environment
        self.qNominal = qNominal
        self.tMax = tMax
        self.lowerActivationLimit = lowerActivationLimit
        self.totalQOutput  = np.zeros(timestepsTotal)
        self.totalSchedule = np.zeros(timestepsTotal)
        self.currentQOutput  = np.zeros(timestepsUsedHorizon)
        self.currentSchedule = np.zeros(timestepsUsedHorizon)
        
    def setSchedule(self, schedule):
        """ Save the computed schedule to the heating device """
        (self.currentSchedule, self.totalSchedule) = functions.handleData.saveResult(self.environment.getTimer(), self.currentSchedule, self.totalSchedule, schedule)

    def setQOutput(self, qOutput):
        """ Save the computed heat output to the heating device """
        (self.currentQOutput, self.totalQOutput) = functions.handleData.saveResult(self.environment.getTimer(), self.currentQOutput, self.totalQOutput, qOutput)

    def getSchedule(self, currentValues=True):
        """ Return the schedule. If currentValues=True: current values, else: total values """
        return functions.handleData.getValues(currentValues, self.currentSchedule, self.totalSchedule)
            
    def getQOutput(self, currentValues=True):
        """ Return the heat output. If currentValues=True: current values, else: total values """
        return functions.handleData.getValues(currentValues, self.currentQOutput, self.totalQOutput)
            
    def getLowerActivationLimit(self):
        """ Return the lower activation level of the heating device """
        return self.lowerActivationLimit
    
    def getQNominal(self):
        """ Return nominal heat output for the current optimization horizon """
        return self.qNominal

    def getTMax(self):
        """ Return the maximum temperature the device can provide """
        return self.tMax