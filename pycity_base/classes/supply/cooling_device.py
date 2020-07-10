#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cooling demand class
"""

from __future__ import division

import numpy as np
from pycity_base.functions import handle_data as handleData


class CoolingDevice(object):
    """
    Superclass of all cooling devices.
    """

    def __init__(self,
                 environment,
                 q_nominal,
                 t_min=4,
                 lower_activation_limit=1):
        """
        Parameters
        ----------
        environment : environment object
            Common to all other objects. Includes time and weather instances
        q_nominal : array of float
            Nominal cooling output in Watt
        t_min : float, optional
            Minimum provided temperature in °C
        lower_activation_limit : float (0 <= lower_activation_limit <= 1)
            Define the lower activation limit. For example, heat pumps are
            typically able to operate between 50 % part load and rated load.
            In this case, lower_activation_limit would be 0.5
            Two special cases:
            Linear behavior: lower_activation_limit = 0
            Two-point controlled: lower_activation_limit = 1
        """

        self._kind = "coolingdevice"

        timesteps_total = environment.timer.timesteps_total
        timesteps_used_horizon = environment.timer.timesteps_used_horizon

        self.environment = environment
        self.q_nominal = q_nominal
        self.t_min = t_min
        self.lower_activation_limit = lower_activation_limit
        self.total_q_output = np.zeros(timesteps_total)
        self.total_device_schedule = np.zeros(timesteps_total)
        self.current_q_output = np.zeros(timesteps_used_horizon)
        self.current_device_schedule = np.zeros(timesteps_used_horizon)

    @property
    def kind(self):
        return self._kind

    def _set_schedule(self, schedule):
        """
        Save the computed schedule to the cooling device.
        """
        results = handleData.saveResult(self.environment.timer,
                                        self.current_device_schedule,
                                        self.total_device_schedule,
                                        schedule)
        (self.current_device_schedule, self.total_device_schedule) = results

    def _set_q_output(self, q_output):
        """
        Save the computed heat output to the cooling device.
        """
        results = handleData.saveResult(self.environment.timer,
                                        self.current_q_output,
                                        self.total_q_output,
                                        q_output)
        (self.current_q_output, self.total_q_output) = results

    def _get_schedule(self, currentValues=True):
        """
        Return the schedule. If currentValues=True: current values, else: total values.
        """
        return handleData.getValues(currentValues,
                                    self.current_device_schedule,
                                    self.total_device_schedule)

    def _get_q_output(self, currentValues=True):
        """
        Return the heat output. If currentValues=True: current values, else: total values.
        """
        return handleData.getValues(currentValues,
                                    self.current_q_output,
                                    self.total_q_output)
