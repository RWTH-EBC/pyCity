# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 16:50:30 2015

@author: tsz
"""

from __future__ import division

import classes.HeatingDevice

class Boiler(classes.HeatingDevice.HeatingDevice):
    """
    Implementation of the boiler
    """
    
    def __init__(self, environment, qNominal, eta, tMax=85, lowerActivationLimit=1):
        """
        Parameter
        ---------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        qNominal : array of float
            nominal heat output in Watt
        eta : array of float
            efficiency (without unit)
        tMax : Integer, optional
            maximum provided temperature in °C
        lowerActivationLimit : Float (0 <= lowerActivationLimit <= 1)
            Define the lower activation limit. For example, heat pumps are 
            typically able to operate between 50 % part load and rated load. 
            In this case, lowerActivationLimit would be 0.5
            Two special cases: 
            Linear behavior: lowerActivationLimit = 0
            Two-point controlled: lowerActivationLimit = 1
        """
        
        self.eta = eta
        super(Boiler, self).__init__(environment, qNominal, tMax, lowerActivationLimit)
        self._kind = "boiler"
        
    def getEta(self):
        """ Return the device's (thermal) efficiency """
        return self.eta
        