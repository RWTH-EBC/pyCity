#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 16:16:07 2015

@author: tsz
"""

from __future__ import division

import numpy as np
import pycity_base.classes.supply.heating_device as HeatingDevice
from pycity_base.functions import handle_data as handleData


class CHP(HeatingDevice.HeatingDevice):
    """
    Implementation of the CHP unit
    """

    def __init__(self, 
                 environment, 
                 p_nominal,
                 q_nominal,
                 omega, 
                 t_max=85,
                 lower_activation_limit=1):
        """
        Parameters
        ---------
        environment : environment object
            Common to all other objects. Includes time and weather instances
        p_nominal : array of float
            nominal electricity output in Watt
        q_nominal : array of float
            nominal heat output in Watt
        omega : array of float
            total efficiency of the CHP unit (without unit)
        t_max : integer, optional
            maximum provided temperature in °C
        lower_activation_limit : float (0 <= lower_activation_limit <= 1)
            Define the lower activation limit. For example, heat pumps are 
            typically able to operate between 50 % part load and rated load. 
            In this case, lower_activation_limit would be 0.5
            Two special cases: 
            Linear behavior: lower_activation_limit = 0
            Two-point controlled: lower_activation_limit = 1
        """

        self.p_nominal = p_nominal
        self.omega = omega
        self.sigma = p_nominal / q_nominal
        super(CHP, self).__init__(environment, 
                                  q_nominal,
                                  t_max,
                                  lower_activation_limit)
        
        self._kind = "chp"

        self.total_p_output = np.zeros(environment.timer.timesteps_total)
        self.current_p_output = np.zeros(environment.timer.timesteps_used_horizon)

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
        pOutput : array-like
            Electricity production of the CHP unit
        qOutput : array-like
            Heat production of the CHP unit
        schedule : array-like
            Operational schedule
        """
        pOutput = handleData.getValues(currentValues, 
                                       self.current_p_output,
                                       self.total_p_output)
        
        return (pOutput,
                self._getQOutput(currentValues), 
                self._getSchedule(currentValues))

    def setResults(self, pOutput, qOutput, schedule):
        """
        Save obtained electricity, heat output and operational schedule.
        """
        self._setSchedule(schedule)
        self._setQOutput(qOutput)
        result = handleData.saveResult(self.environment.timer, 
                                       self.current_p_output,
                                       self.total_p_output,
                                       pOutput)
        (self.current_p_output, self.total_p_output) = result
        
    def getNominalValues(self):
        """
        Return the CHP unit's nominal values as a tuple. 
        
        Order: Overall efficiency, power to heat ratio, nominal electricity 
        output, nominal heat output, maximum flow temperature and lower 
        activation limit.
        """
        return (self.omega, self.sigma, self.p_nominal, self.q_nominal,
                self.t_max, self.lower_activation_limit)
