#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 17:44:16 2015

@author: tsz
"""

from __future__ import division

import numpy as np
from pycity_base.functions import handle_data as handleData


class Inverter(object):
    """
    Implementation of the AC-DC / DC-AC inverter
    """
    
    def __init__(self, environment, eta, p_nominal, input_AC=True):
        """
        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        eta : float (0 <= eta <= 1)
            efficiency (without unit)
        p_nominal : float
            nominal electrical power in Watt
        input_AC : boolean, optional
            True if input is AC
            False if input is DC
        """
        self._kind = "inverter"
        self.environment = environment
        self.eta = eta
        self.p_nominal = p_nominal
        self.input_AC = input_AC

        timesteps_total = environment.timer.timesteps_total
        timesteps_used_horizon = environment.timer.timesteps_used_horizon
        
        self.total_p_input = np.zeros(timesteps_total)
        self.total_p_output = np.zeros(timesteps_total)
        self.current_p_input = np.zeros(timesteps_used_horizon)
        self.current_p_output = np.zeros(timesteps_used_horizon)

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
        pInput : array-like
            Electricity input of the inverter
        pOutput : array-like
            Electricity output of the inverter
        """
        pInput = handleData.getValues(currentValues, 
                                      self.current_p_input,
                                      self.total_p_input)
        
        pOutput = handleData.getValues(currentValues, 
                                       self.current_p_output,
                                       self.total_p_output)
        
        return (pInput, pOutput)

    def setResults(self, pInput, pOutput):
        """
        Save electricity input and output of the inverter.
        """
        results = handleData.saveResult(self.environment.timer, 
                                        self.current_p_input,
                                        self.total_p_input,
                                        pInput)
        (self.current_p_input, self.total_p_input) = results
        
        results = handleData.saveResult(self.environment.timer, 
                                        self.current_p_output,
                                        self.total_p_output,
                                        pOutput)
        (self.current_p_output, self.total_p_output) = results
        
    def getNominalValues(self):
        """
        Return the inverter's nominal values as a tuple.
        
        Order: Type of inverter, electrical efficiency and nominal input power.
        """
        return (self.input_AC, self.eta, self.p_nominal)
