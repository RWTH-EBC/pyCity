#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 23:00:27 2015

@author: T_ohne_admin
"""

import numpy as np
import functions.handleData as handleData

class ThermalEnergyStorage(object):
    """
    Implementation of the thermal energy storage unit
    """
    
    cWater = 4180 # heat capacity of water. In J/(kg.K)
    
    def __init__(self, 
                 environment, 
                 tInit, 
                 capacity, 
                 tMax, 
                 tSurroundings=20, 
                 kLosses=3):
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
        
        self.totalTSto   = np.zeros(environment.timer.timestepsTotal)
        self.currentTSto = np.zeros(environment.timer.timestepsUsedHorizon)
        
    def setResults(self, tSto):
        """ 
        Save the computed storage temperature and update new initial 
        temperature 
        """
        results = handleData.saveResultInit(self.environment.timer, 
                                            self.currentTSto, 
                                            self.totalTSto, 
                                            tSto)
        (self.currentTSto, self.totalTSto, self.tInit) = results 

    def getResults(self, currentValues=True):
        """ 
        Return the storage's temperature. If currentValues=True: current 
        values, else: total values 
        """
        return handleData.getValues(currentValues, 
                                    self.currentTSto, 
                                    self.totalTSto)
    
    def getNominalValues(self):
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
