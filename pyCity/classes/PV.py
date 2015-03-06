# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 17:39:01 2015

@author: tsz
"""

from __future__ import division

class PV(object):
    """
    Implementation of the PV class.
    """
    
    def __init__(self, environment, area, eta):
        """
        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        area : integer
            installation area in m2
        eta : float
            efficiency (without unit)
        """
        self._kind = "pv"        
        
        self.environment = environment
        self.area = area
        self.eta = eta
        
    def getPower(self):
        """ Get the PV power for the current forecasting horizon"""
        (directRadiation, diffuseRadiation) = self.environment.getWeatherForecast(False, True, True, False, False, False)
        self.power = self.area * self.eta * directRadiation
        
        return self.power
