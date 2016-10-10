#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 16:50:30 2015

@author: tsz
"""

from __future__ import division
import pycity.classes.supply.HeatingDevice as HeatingDevice


class Boiler(HeatingDevice.HeatingDevice):
    """
    Implementation of the boiler
    """
    
    def __init__(self, 
                 environment, 
                 qNominal, 
                 eta, 
                 tMax=85, 
                 lowerActivationLimit=1):
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
        super(Boiler, self).__init__(environment, 
                                     qNominal, 
                                     tMax, 
                                     lowerActivationLimit)
        self.__kind = "boiler"

    def __str__(self):
        return str('<Boiler object of pyCity>')

    @property
    def kind(self):
        """
        Return type of pyCity object
        """
        return self.__kind
        
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
            Heat production of the boiler
        schedule : array_like
            Operational schedule
        """
        return (self._getQOutput(currentValues), 
                self._getSchedule(currentValues))

    def setResults(self, qOutput, schedule):
        """
        Save resulting heat output and operational schedule.
        """
        self._setSchedule(schedule)
        self._setQOutput(qOutput)

    
    def getNominalValues(self):
        """
        Get the boiler's efficiency, nominal heat output, maximum flow 
        temperature and lower activation limit.
        """
        return (self.eta, self.qNominal, self.tMax, self.lowerActivationLimit)
