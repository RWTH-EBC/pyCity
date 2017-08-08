#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 20:01:19 2015

@author: Thomas
"""

from __future__ import division
import numpy as np
import pycity_base.functions.handleData as handleData


class Battery(object):
    """
    Implementation of the battery
    """
    
    def __init__(self, environment, socInit, capacity, selfDischarge=0.01, 
                 etaCharge=0.95, etaDischarge=0.95):
        """
        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        socInit : float (0 <= socInit <= capacity)
            Initial state of charge in Joule
        capacity : float 
            Battery's capacity in Joule
        selfDischarge : float (0 <= selfDischarge <= 1)
            Rate of self discharge per time step (without unit)
        etaCharge : float (0 <= etaCharge <= 1)
            Charging efficiency (without unit)
        etaDischarge : float (0 <= etaDischarge <= 1)
            Discharging efficiency (without unit)
            
        """
        self._kind = "battery"
        self.environment = environment
        self.capacity = capacity
        self.selfDischarge = selfDischarge
        self.etaCharge = etaCharge
        self.etaDischarge = etaDischarge
        self.socInit = socInit
        
        timestepsTotal       = environment.timer.timestepsTotal
        timestepsUsedHorizon = environment.timer.timestepsUsedHorizon
        
        self.totalSoc          = np.zeros(timestepsTotal)
        self.totalPCharge      = np.zeros(timestepsTotal)
        self.totalPDischarge   = np.zeros(timestepsTotal)
        self.currentSoc        = np.zeros(timestepsUsedHorizon)
        self.currentPCharge    = np.zeros(timestepsUsedHorizon)
        self.currentPDischarge = np.zeros(timestepsUsedHorizon)

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
        soc : array_like
            State of charge
        charge : array_like
            Charging power
        discharge : array_like
            Discharging power
        """
        soc = handleData.getValues(currentValues, self.currentSoc, 
                                   self.totalSoc)
        charge = handleData.getValues(currentValues, self.currentPCharge, 
                                      self.totalPCharge)
        discharge = handleData.getValues(currentValues, self.currentPDischarge,
                                         self.totalPDischarge)
        return (soc, charge, discharge)

    def setResults(self, soc, charge, discharge):
        """
        Save resulting state of charge, charging and discharging powers.
        """
        # Save state of charge
        results = handleData.saveResultInit(self.environment.timer,
                                            self.currentSoc, 
                                            self.totalSoc, 
                                            soc)
        (self.currentSoc, self.totalSoc, self.socInit) = results
        
        # Save charging power
        results = handleData.saveResult(self.environment.timer, 
                                        self.currentPCharge, 
                                        self.totalPCharge, 
                                        charge)
        (self.currentPCharge, self.totalPCharge) = results
        
        # Save discharging power
        results = handleData.saveResult(self.environment.timer, 
                                        self.currentPDischarge, 
                                        self.totalPDischarge, 
                                        discharge)
        (self.currentPDischarge, self.totalPDischarge) = results
    
    def getNominalValues(self):
        """
        Get battery's capacity, rate of self discharge, charging and 
        discharging efficiency.
        """
        return (self.capacity, self.selfDischarge, 
                self.etaCharge, self.etaDischarge)
