#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cooling demand class
"""

from __future__ import division
import numpy as np
import pycity_base.functions.handleData as handleData


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
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        q_nominal : Array of float
            Nominal cooling output in Watt
        t_min : Float, optional
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

        timestepsTotal = environment.timer.timestepsTotal
        timestepsUsedHorizon = environment.timer.timestepsUsedHorizon

        self.environment = environment
        self.q_nominal = q_nominal
        self.t_min = t_min
        self.lower_activation_limit = lower_activation_limit
        self.totalQOutput = np.zeros(timestepsTotal)
        self.totalSchedule = np.zeros(timestepsTotal)
        self.currentQOutput = np.zeros(timestepsUsedHorizon)
        self.currentSchedule = np.zeros(timestepsUsedHorizon)

    def _setSchedule(self, schedule):
        """ Save the computed schedule to the cooling device """
        results = handleData.saveResult(self.environment.timer,
                                        self.currentSchedule,
                                        self.totalSchedule,
                                        schedule)
        (self.currentSchedule, self.totalSchedule) = results

    def _setQOutput(self, qOutput):
        """ Save the computed heat output to the cooling device """
        results = handleData.saveResult(self.environment.timer,
                                        self.currentQOutput,
                                        self.totalQOutput,
                                        qOutput)
        (self.currentQOutput, self.totalQOutput) = results

    def _getSchedule(self, currentValues=True):
        """
        Return the schedule. If currentValues=True: current values,
        else: total values
        """
        return handleData.getValues(currentValues,
                                    self.currentSchedule,
                                    self.totalSchedule)

    def _getQOutput(self, currentValues=True):
        """
        Return the heat output. If currentValues=True: current values,
        else: total values
        """
        return handleData.getValues(currentValues,
                                    self.currentQOutput,
                                    self.totalQOutput)
