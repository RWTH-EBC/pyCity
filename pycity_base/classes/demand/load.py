#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 07 07:09:12 2015

@author: tsz
"""

from __future__ import division

import numpy as np


class Load(object):
    """
    This class holds a load curve and is able to return it or parts of it.
    """
    
    def __init__(self, environment, loadcurve):
        """
        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        loadcurve: Array like
            Load curve for all time steps
        """
        self._kind = "load"
        self.environment = environment
        
        self.loadcurve = np.array(loadcurve)

    @property
    def kind(self):
        return self._kind
        
    def _getLoadcurve(self, currentValues=True):
        """
        Return the load curve for the upcoming scheduling period 
        (currentValues==True) or return the entire load curve 
        (currentValues==False)
        """
        if currentValues:
            initialPosition  = self.environment.timer.currentTimestep
            timestepsHorizon = self.environment.timer.timestepsHorizon
            finalPosition = initialPosition + timestepsHorizon
            return self.loadcurve[initialPosition : finalPosition]
        else:
            return self.loadcurve
