# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 23:00:27 2015

@author: T_ohne_admin
"""

import numpy as np
import functions.handleData

class ThermalEnergyStorage(object):
    """
    Implementation of the thermal energy storage unit
    """
    
    def __init__(self, environment, tInit, capacity, tMax, tSurroundings=20, kLosses=3):
        """
        Parameter
        ---------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        tInit : Integer
            initialization temperature in °C
        capacity : Integer
            storage mass in kg
        tMax : Integer, optional
            maximum storage temperature in °C
        tSurroundings : Integer, optional
            temperature of the storage's surroundings in °C
        kLosses : Float, optional
            storage's loss factor (area*U_value) in W/K
        """
        self._kind = "tes"
        
        self.environment = environment
        self.capacity = capacity
        self.tSurroundings = tSurroundings
        self.tMax = tMax
        self.kLosses = kLosses
        self.tInit = tInit
        
        self.totalTSto   = np.zeros(environment.getTimestepsTotal())
        self.currentTSto = np.zeros(environment.getTimestepsUsedHorizon())
        
    def setTSto(self, tSto):
        """ Save the computed storage temperature and update new initial temperature """
        (self.currentTSto, self.totalTSto, self.tInit) = functions.handleData.saveResultInit(self.environment.getTimer(), self.currentTSto, self.totalTSto, tSto)

    def getTSto(self, currentValues=True):
        """ Return the storage's temperature. If currentValues=True: current values, else: total values """
        return functions.handleData.getValues(currentValues, self.currentTSto, self.totalTSto)
    
    def getTInit(self):
        """ Return the initial temperature """
        return self.tInit
        
    def getStorageParameters(self):
        """
        Returns a tuple with the storage's constant parameters
        
        Returns
        -------
        capacity : Integer
            storage mass in kg
        tMax : Integer, optional
            maximum storage temperature in °C
        tSurroundings : Integer, optional
            temperature of the storage's surroundings in °C
        kLosses : Float, optional
            storage's loss factor (area*U_value) in W/K
        """
        return (self.capacity, self.tMax, self.tSurroundings, self.kLosses)
