#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 07 07:09:12 2015

@author: Thomas
"""

from __future__ import division
import pycity_base.classes.demand.Load


class LoadComplex(pycity_base.classes.demand.Load.Load):
    """
    This class holds a load curve and is able to return it or parts of it.
    """

    def __init__(self, environment, loadcurve_complex):
        """
        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        loadcurve_complex: Array like
            Load curve for all time steps with active (loadcurve) and reactive power (loadcurve_q)
        """

        super(LoadComplex, self).__init__(environment, loadcurve_complex)

    def _getLoadcurve(self, currentValues=True):
        """
        Return the load curve for the upcoming scheduling period 
        (currentValues==True) or return the entire load curve 
        (currentValues==False)
        """
        if currentValues:
            initialPosition = self.environment.timer.currentTimestep
            timestepsHorizon = self.environment.timer.timestepsHorizon
            finalPosition = initialPosition + timestepsHorizon
            return self.loadcurve[initialPosition: finalPosition]
        else:
            return self.loadcurve

    def _getLoadcurve_q(self, currentValues=True):
        """
        Return the reactive load curve for the upcoming scheduling period
        (currentValues==True) or return the entire load curve
        (currentValues==False)
        """
        if currentValues:
            initialPosition = self.environment.timer.currentTimestep
            timestepsHorizon = self.environment.timer.timestepsHorizon
            finalPosition = initialPosition + timestepsHorizon
            return self.loadcurve_q[initialPosition: finalPosition]
        else:
            return self.loadcurve_q
