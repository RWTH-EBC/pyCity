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
                 qNominal,
                 tMin=85,
                 lowerActivationLimit=1):
        """
        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        qNominal : Array of float
            Nominal cooling output in Watt
        tMin : Float, optional
            Minimum provided temperature in °C
        lowerActivationLimit : float (0 <= lowerActivationLimit <= 1)
            Define the lower activation limit. For example, heat pumps are
            typically able to operate between 50 % part load and rated load.
            In this case, lowerActivationLimit would be 0.5
            Two special cases:
            Linear behavior: lowerActivationLimit = 0
            Two-point controlled: lowerActivationLimit = 1
        """

        self._kind = "coolingdevice"

        timestepsTotal = environment.timer.timestepsTotal
        timestepsUsedHorizon = environment.timer.timestepsUsedHorizon

        self.environment = environment
        self.qNominal = qNominal
        self.tMin = tMin
        self.lowerActivationLimit = lowerActivationLimit
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
