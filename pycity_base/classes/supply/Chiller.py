#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cooling demand class
"""

from __future__ import division
import pycity_base.classes.supply.CoolingDevice as CoolingDevice


class Chiller(CoolingDevice.CoolingDevice):
    """
    Implementation of the chiller
    """

    def __init__(self,
                 environment,
                 tAmbient,
                 qNominal,
                 epsilon,
                 tMin=4,
                 lowerActivationLimit=1):
        """
        Parameter
        ---------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        qNominal : array of float
            nominal cooling output in Watt
        epsilon : array of float
            efficiency (without unit)
        tMin : Integer, optional
            minimum provided temperature in °C
        lowerActivationLimit : Float (0 <= lowerActivationLimit <= 1)
            Define the lower activation limit. For example, heat pumps are
            typically able to operate between 50 % part load and rated load.
            In this case, lowerActivationLimit would be 0.5
            Two special cases:
            Linear behavior: lowerActivationLimit = 0
            Two-point controlled: lowerActivationLimit = 1
        """

        super(Chiller, self).__init__(environment,
                                      qNominal,
                                      tMin,
                                      lowerActivationLimit)
        self._kind = "chiller"
        self.epsilon = epsilon
        self.tAmbient = tAmbient

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
        qOutput : array_like
            cooling production of the chiller
        schedule : array_like
            Operational schedule
        """
        return (self._getQOutput(currentValues),
                self._getSchedule(currentValues))

    def setResults(self, qOutput, schedule):
        """
        Save resulting cooling output and operational schedule.
        """
        self._setSchedule(schedule)
        self._setQOutput(qOutput)

    def getNominalValues(self):
        """
        Get the chiller's efficiency, nominal cooling output, minimal flow
        temperature and lower activation limit.
        """
        return (
            self.epsilon, self.qNominal, self.tMin, self.lowerActivationLimit)
