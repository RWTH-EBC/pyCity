#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 15:57:15 2015

@author: tsz
"""

from __future__ import division

import numpy as np
from pycity_base.functions import handle_data as handleData


class HeatingDevice(object):
    """
    Superclass of all heating devices.
    """
   
    def __init__(self, environment, q_nominal, t_max=85, lower_activation_limit=1):
        """
        Parameters
        ----------
        environment : environment object
            Common to all other objects. Includes time and weather instances
        q_nominal : array of float
            Nominal heat output in Watt
        t_max : float, optional
            Maximum provided temperature in °C
        lower_activation_limit : float (0 <= lower_activation_limit <= 1)
            Define the lower activation limit. For example, heat pumps are 
            typically able to operate between 50 % part load and rated load. 
            In this case, lower_activation_limit would be 0.5
            Two special cases: 
            Linear behavior: lower_activation_limit = 0
            Two-point controlled: lower_activation_limit = 1
        """
        self._kind = "heatingdevice"

        timesteps_total = environment.timer.timesteps_total
        timesteps_used_horizon = environment.timer.timesteps_used_horizon
        
        self.environment = environment
        self.q_nominal = q_nominal
        self.t_max = t_max
        self.lower_activation_limit = lower_activation_limit
        self.total_q_output = np.zeros(timesteps_total)
        self.total_device_schedule = np.zeros(timesteps_total)
        self.current_q_output = np.zeros(timesteps_used_horizon)
        self.current_device_schedule = np.zeros(timesteps_used_horizon)

    @property
    def kind(self):
        return self._kind
        
    def _setSchedule(self, schedule):
        """
        Save the computed schedule to the heating device.
        """
        results = handleData.saveResult(self.environment.timer,
                                        self.current_device_schedule,
                                        self.total_device_schedule,
                                        schedule)
        (self.current_device_schedule, self.total_device_schedule) = results

    def _setQOutput(self, qOutput):
        """
        Save the computed heat output to the heating device.
        """
        results = handleData.saveResult(self.environment.timer, 
                                        self.current_q_output,
                                        self.total_q_output,
                                        qOutput)
        (self.current_q_output, self.total_q_output) = results

    def _getSchedule(self, currentValues=True):
        """ 
        Returns the schedule.
        If currentValues=True: current values, else: total values.
        """
        return handleData.getValues(currentValues, 
                                    self.current_device_schedule,
                                    self.total_device_schedule)
            
    def _getQOutput(self, currentValues=True):
        """ 
        Returns the heat output. If currentValues=True: current values, else: total values.
        """
        return handleData.getValues(currentValues, 
                                    self.current_q_output,
                                    self.total_q_output)
