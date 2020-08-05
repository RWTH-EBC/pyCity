#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 20:01:19 2015

@author: tsz
"""

from __future__ import division

import numpy as np
from pycity_base.functions import handle_data as handleData


class Battery(object):
    """
    Implementation of the battery
    """
    
    def __init__(self, environment, soc_init, capacity, self_discharge=0.01,
                 eta_charge=0.95, eta_discharge=0.95):
        """
        Parameters
        ----------
        environment : environment object
            Common to all other objects. Includes time and weather instances
        soc_init : float (0 <= soc_init <= capacity)
            Initial state of charge in Joule
        capacity : float 
            Battery's capacity in Joule
        self_discharge : float (0 <= self_discharge <= 1)
            Rate of self discharge per time step (without unit)
        eta_charge : float (0 <= eta_charge <= 1)
            Charging efficiency (without unit)
        eta_discharge : float (0 <= eta_discharge <= 1)
            Discharging efficiency (without unit)
            
        """
        self._kind = "battery"
        self.environment = environment
        self.capacity = capacity
        self.self_discharge = self_discharge
        self.eta_charge = eta_charge
        self.eta_discharge = eta_discharge
        self.soc_init = soc_init
        
        timesteps_total = environment.timer.timesteps_total
        timesteps_used_horizon = environment.timer.timesteps_used_horizon
        
        self.total_soc = np.zeros(timesteps_total)
        self.total_p_charge = np.zeros(timesteps_total)
        self.total_p_discharge = np.zeros(timesteps_total)
        self.current_soc = np.zeros(timesteps_used_horizon)
        self.current_p_charge = np.zeros(timesteps_used_horizon)
        self.current_p_discharge = np.zeros(timesteps_used_horizon)

    @property
    def kind(self):
        return self._kind

    def getResults(self, currentValues=True):
        """
        Return results.
        
        Parameters
        ----------
        currentValues : boolean, optional
            - True : Return only values for this scheduling period
            - False : Return values for all scheduling periods
        
        Returns
        -------
        soc : array-like
            State of charge
        charge : array-like
            Charging power
        discharge : array-like
            Discharging power
        """
        soc = handleData.getValues(currentValues, self.current_soc,
                                   self.total_soc)
        charge = handleData.getValues(currentValues, self.current_p_charge,
                                      self.total_p_charge)
        discharge = handleData.getValues(currentValues, self.current_p_discharge,
                                         self.total_p_discharge)
        return (soc, charge, discharge)

    def setResults(self, soc, charge, discharge):
        """
        Save resulting state of charge, charging and discharging powers.
        """
        # Save state of charge
        results = handleData.saveResultInit(self.environment.timer,
                                            self.current_soc,
                                            self.total_soc,
                                            soc)
        (self.current_soc, self.total_soc, self.soc_init) = results
        
        # Save charging power
        results = handleData.saveResult(self.environment.timer, 
                                        self.current_p_charge,
                                        self.total_p_charge,
                                        charge)
        (self.current_p_charge, self.total_p_charge) = results
        
        # Save discharging power
        results = handleData.saveResult(self.environment.timer, 
                                        self.current_p_discharge,
                                        self.total_p_discharge,
                                        discharge)
        (self.current_p_discharge, self.total_p_discharge) = results
    
    def getNominalValues(self):
        """
        Get battery's capacity, rate of self discharge, charging and 
        discharging efficiency.
        """
        return (self.capacity, self.self_discharge,
                self.eta_charge, self.eta_discharge)
