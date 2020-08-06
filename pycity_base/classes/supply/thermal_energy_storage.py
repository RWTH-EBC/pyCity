#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 23:00:27 2015

@author: tsz
"""

from __future__ import division

import numpy as np
from pycity_base.functions import handle_data as handleData


class ThermalEnergyStorage(object):
    """
    Implementation of the thermal energy storage unit
    """
    
    c_water = 4180  # heat capacity of water. In J/(kgK)
    
    def __init__(self, 
                 environment, 
                 t_init,
                 capacity, 
                 t_max,
                 t_surroundings=20,
                 k_losses=3):
        """
        Parameters
        ----------
        environment : environment object
            Common to all other objects. Includes time and weather instances
        t_init : integer
            initialization temperature in °C
        capacity : Integer
            storage mass in kg
        t_max : integer, optional
            maximum storage temperature in °C
        t_surroundings : Integer, optional
            temperature of the storage's surroundings in °C
        k_losses : float, optional
            storage's loss factor (area*U_value) in W/K
        """
        self._kind = "tes"
        
        self.environment = environment
        self.capacity = capacity
        self.t_surroundings = t_surroundings
        self.t_max = t_max
        self.k_losses = k_losses
        self.t_init = t_init
        
        self.total_t_sto = np.zeros(environment.timer.timesteps_total)
        self.current_t_sto = np.zeros(environment.timer.timesteps_used_horizon)

    @property
    def kind(self):
        return self._kind
        
    def setResults(self, tSto):
        """ 
        Save the computed storage temperature and update new initial 
        temperature 
        """
        results = handleData.saveResultInit(self.environment.timer, 
                                            self.current_t_sto,
                                            self.total_t_sto,
                                            tSto)
        (self.current_t_sto, self.total_t_sto, self.t_init) = results

    def getResults(self, currentValues=True):
        """ 
        Return the storage's temperature. If currentValues=True: current 
        values, else: total values 
        """
        return handleData.getValues(currentValues, 
                                    self.current_t_sto,
                                    self.total_t_sto)
    
    def getNominalValues(self):
        """
        Returns a tuple with the storage's constant parameters
        
        Returns
        -------
        capacity : integer
            storage mass in kg
        t_max : integer, optional
            maximum storage temperature in °C
        tSurroundings : integer, optional
            temperature of the storage's surroundings in °C
        kLosses : float, optional
            storage's loss factor (area*U_value) in W/K
        """
        return (self.capacity, self.t_max, self.t_surroundings, self.k_losses)
