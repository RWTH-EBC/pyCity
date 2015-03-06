# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 20:01:19 2015

@author: T_ohne_admin
"""

import numpy as np
import functions.handleData

class Battery(object):
    """
    Implementation of the battery
    """
    
    def __init__(self, environment, socInit, capacity, selfDischarge=0.01, etaCharge=0.95, etaDischarge=0.95):
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
        
        timestepsTotal       = environment.getTimestepsTotal()
        timestepsUsedHorizon = environment.getTimestepsUsedHorizon()
        
        self.totalSoc          = np.zeros(timestepsTotal)
        self.totalPCharge      = np.zeros(timestepsTotal)
        self.totalPDischarge   = np.zeros(timestepsTotal)
        self.currentSoc        = np.zeros(timestepsUsedHorizon)
        self.currentPCharge    = np.zeros(timestepsUsedHorizon)
        self.currentPDischarge = np.zeros(timestepsUsedHorizon)

    def setSoc(self, soc):
        """ Save the computed SOC and update new initial SOC """
        (self.currentSoc, self.totalSoc, self.socInit) = functions.handleData.saveResultInit(self.environment.getTimer(), self.currentSoc, self.totalSoc, soc)
        
    def setPCharge(self, pCharge):
        """ Save the computed charge powers """
        (self.currentPCharge, self.totalPCharge) = functions.handleData.saveResult(self.environment.getTimer(), self.currentPCharge, self.totalPCharge, pCharge)
                
    def setPDischarge(self, pDischarge):
        """ Save the computed discharge powers """
        (self.currentPDischarge, self.totalPDischarge) = functions.handleData.saveResult(self.environment.getTimer(), self.currentPDischarge, self.totalPDischarge, pDischarge)
    
    def getSoc(self, currentValues=True):
        """ Return the SOC. If currentValues=True: current values, else: total values """
        return functions.handleData.getValues(currentValues, self.currentSoc, self.totalSoc)
            
    def getPCharge(self, currentValues=True):
        """ Return the charging power. If currentValues=True: current values, else: total values """
        return functions.handleData.getValues(currentValues, self.currentPCharge, self.totalPCharge)

    def getPDischarge(self, currentValues=True):
        """ Return the discharging power. If currentValues=True: current values, else: total values """
        return functions.handleData.getValues(currentValues, self.currentPDischarge, self.totalPDischarge)
    
    def getCapacity(self):
        """ Return the battery's capacity """
        return self.capacity
        
    def getSelfDischarge(self):
        """ Return the battery's rate of self-discharge """
        return self.selfDischarge
        
    def getEtaCharge(self):
        """ Return the battery's efficiency at charging """
        return self.etaCharge

    def getEtaDischarge(self):
        """ Return the battery's efficiency at discharging """
        return self.etaDischarge
        
    def getSocInit(self):
        """ Return the battery's initial state of charge """
        return self.socInit
