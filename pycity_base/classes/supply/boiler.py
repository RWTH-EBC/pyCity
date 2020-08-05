#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 16:50:30 2015

@author: tsz
"""

from __future__ import division

import pycity_base.classes.supply.heating_device as HeatingDevice


class Boiler(HeatingDevice.HeatingDevice):
    """
    Implementation of the boiler
    """
    
    def __init__(self, 
                 environment, 
                 q_nominal,
                 eta, 
                 t_max=85,
                 lower_activation_limit=1):
        """
        Parameters
        ----------
        environment : environment object
            Common to all other objects. Includes time and weather instances
        q_nominal : array of float
            nominal heat output in Watt
        eta : array of float
            efficiency (without unit)
        t_max : integer, optional
            maximum provided temperature in °C
        lower_activation_limit : float (0 <= lower_activation_limit <= 1)
            Define the lower activation limit. For example, heat pumps are 
            typically able to operate between 50 % part load and rated load. 
            In this case, lower_activation_limit would be 0.5
            Two special cases: 
            Linear behavior: lower_activation_limit = 0
            Two-point controlled: lower_activation_limit = 1
        """
        
        self.eta = eta
        super(Boiler, self).__init__(environment, 
                                     q_nominal,
                                     t_max,
                                     lower_activation_limit)
        self._kind = "boiler"

    @property
    def kind(self):
        return self._kind
        
    def getResults(self, currentValues=True):
        """
        Return results.
        
        Parameters
        ----------
        currentValues : boolean, optional
            - True : Return only values for this scheduling period
            - False : Return values for all scheduling periods
        
        Returns
        -------
        qOutput : array-like
            Heat production of the boiler
        schedule : array-like
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
        return (self.eta, self.q_nominal, self.t_max, self.lower_activation_limit)
