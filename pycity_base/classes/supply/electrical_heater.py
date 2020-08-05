#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 17:01:58 2015

@author: tsz
"""

from __future__ import division

import pycity_base.classes.supply.heating_device as HeatingDevice
import numpy as np
from pycity_base.functions import handle_data as handleData


class ElectricalHeater(HeatingDevice.HeatingDevice):
    """
    Implementation of the electrical heater
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
            nominal heat production in Watt
        eta : array of float
            nominal efficiency (without unit)
        t_max : float, optional
            maximum provided temperature in °C
        lower_activation_limit : float, optional
            see HeatingDevice
        """
        
        super(ElectricalHeater, self).__init__(environment, 
                                               q_nominal,
                                               t_max,
                                               lower_activation_limit)
        self._kind = "electricalheater"
        self.eta = eta
        self.p_nominal = q_nominal / eta
        
        timesteps_total = environment.timer.timesteps_total
        timesteps_used_horizon = environment.timer.timesteps_used_horizon
        
        self.total_p_consumption = np.zeros(timesteps_total)
        self.current_p_consumption = np.zeros(timesteps_used_horizon)

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
        pConsumption : array-like
            Electricity consumption of the electrical heater
        qOutput : array-like
            Heat production of the electrical heater
        schedule : array-like
            Operational schedule
        """
        pConsumption = handleData.getValues(currentValues, 
                                            self.current_p_consumption,
                                            self.total_p_consumption)
        
        return (pConsumption,
                self._getQOutput(currentValues), 
                self._getSchedule(currentValues))

    def setResults(self, pConsumption, qOutput, schedule):
        """
        Save resulting electricty consumption, heat output and 
        operational schedule.
        """
        self._setSchedule(schedule)
        self._setQOutput(qOutput)
        result = handleData.saveResult(self.environment.timer, 
                                       self.current_p_consumption,
                                       self.total_p_consumption,
                                       pConsumption)
        (self.current_p_consumption, self.total_p_consumption) = result
        
    def getNominalValues(self):
        """
        Return the electrical heater's nominal values as a tuple. 
        
        Order: Electrical efficiency, nominal electricity consumption, nominal 
        heat output, maximum flow temperature and lower activation limit.
        """
        return (self.eta, self.p_nominal, self.q_nominal, self.t_max,
                self.lower_activation_limit)
