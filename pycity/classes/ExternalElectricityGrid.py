#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 08:52:56 2015

@author: Thomas
"""

from __future__ import division
import numpy as np
import pycity.functions.handleData as handleData


class ExternalElectricityGrid(object):
    """
    """
    
    def __init__(self, environment):
        """
        """
        self.__kind = "externalelectricitygrid"
        self.environment = environment
        
        # Initialize current and total grid interaction
        timestepsUsedHorizon = environment.getTimestepsUsedHorizon()
        timestepsTotal       = environment.getTimestepsTotal()
        
        self.currentPSurplus    = np.zeros(timestepsUsedHorizon)
        self.currentPAdditional = np.zeros(timestepsUsedHorizon)
        self.totalPSurplus    = np.zeros(timestepsTotal)
        self.totalPAdditional = np.zeros(timestepsTotal)

    def __str__(self):
        return str('<External electrical grid object of pyCity>')

    @property
    def kind(self):
        """
        Return type of pyCity object
        """
        return self.__kind
        
    def setPSurplus(self, pSurplus):
        """ Save the electrical surplus that is sold to the grid """
        results = handleData.saveResult(self.getTimer(), 
                                        self.currentPSurplus, 
                                        self.totalPSurplus, 
                                        pSurplus)
        (self.currentPSurplus, self.totalPSurplus) = results
        
    def setPAdditional(self, pAdditional):
        """ Save the electricity imports from the grid """
        results = handleData.saveResult(self.getTimer(), 
                                        self.currentPAdditional, 
                                        self.totalPAdditional, 
                                        pAdditional)
        (self.currentPAdditional, self.totalPAdditional) = results
        
    def getPSurplus(self, currentValues=True):
        """ 
        Return the electrical surplus. If currentValues=True: current values, 
        else: total values 
        """
        return handleData.getValues(currentValues, 
                                    self.currentPSurplus, 
                                    self.totalPSurplus)
        
    def getPAdditional(self, currentValues=True):
        """ 
        Return the electricity imports. If currentValues=True: current values, 
        else: total values 
        """
        return handleData.getValues(currentValues, 
                                    self.currentPAdditional, 
                                    self.totalPAdditional)