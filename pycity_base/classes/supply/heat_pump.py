#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 16:45:15 2015

@author: tsz
"""

from __future__ import division

import pycity_base.classes.supply.heating_device as HeatingDevice
import numpy as np
from pycity_base.functions import handle_data as handleData


class Heatpump(HeatingDevice.HeatingDevice):
    """
    Implementation of the heat pump.
    """
    
    def __init__(self, environment, 
                 t_ambient, t_flow,
                 heat, power, cop,
                 t_max, lower_activation_limit=1):
        """
        Parameters
        ----------
        environment : environment object
            Common to all other objects. Includes time and weather instances.
        t_ambient : array-like
            Outdoor ambient air temperature
        t_flow : array-like
            Heat pump's flow temperature
        heat : array-like (2 dimensional)
            Heat pump's heat power
        power : array-like (2 dimensional)
            Heat pump's electrical power
        cop : array-like (2 dimensional)
            Heat pump's coefficient of performance (cop)
        t_max : float
            Heat pump's nominal temperature
        lower_activation_limit : float (0 <= lower_activation_limit <= 1)
            Define the lower activation limit. For example, heat pumps are 
            typically able to operate between 50 % part load and rated load. 
            In this case, lower_activation_limit would be 0.5
            Two special cases: 
            Linear behavior: lower_activation_limit = 0
            Two-point controlled: lower_activation_limit = 1
        """
        
        q_nominal=np.zeros(environment.timer.timesteps_horizon)
        super(Heatpump, self).__init__(environment, 
                                       q_nominal,
                                       t_max,
                                       lower_activation_limit)
        self._kind = "heatpump"
        
        self.t_ambient = t_ambient
        self.t_flow = t_flow
        self.heat = heat
        self.power = power
        self.cop = cop
        
        timesteps_total = environment.timer.timesteps_total
        timesteps_used_horizon = environment.timer.timesteps_used_horizon
        self.total_p_consumption = np.zeros(timesteps_total)
        self.current_p_consumption = np.zeros(timesteps_used_horizon)

    @property
    def kind(self):
        return self._kind
        
    def getNominalValues(self, t_flow):
        """
        Return the nominal electricity consumption, heat output and lower 
        activation limit.
        
        The electricity consumption and heat output are computed by two 
        dimensional interpolation with the ambient temperature and required
        flow temperature as well as the heat pump's characteristics.
        
        Parameters
        ----------
        t_flow : array-like
            Required flow temperature
            
        Returns
        -------
        p_nominal : array-like
            Nominal electricity consumption at the given flow temperatures and
            the forecast of the current ambient temperature
        q_nominal : array-like
            Nominal heat output at the given flow temperatures and the 
            forecast of the current ambient temperature
        t_max : float
            Maximum flow temperature that can be provided by the heat pump
        lower_activation_limit : float (0 <= lower_activation_limit <= 1)
            Define the lower activation limit. For example, heat pumps are 
            typically able to operate between 50 % part load and rated load. 
            In this case, lower_activation_limit would be 0.5
            Two special cases: 
            Linear behavior: lower_activation_limit = 0
            Two-point controlled: lower_activation_limit = 1
            
        Examples
        --------
        >>> t_flow = building.getFlowTemperature()
        >>> (p_nominal, q_nominal, lower_activation_limit) = hp.getNominals(t_flow)
        """
        # Get weather forecast
        weatherForecast = self.environment.weather.getWeatherForecast
        (t_ambient,) = weatherForecast(getTAmbient=True)
        
        # Two dimensional interpolation is required.
        # Initialize temporary results of the first interpolation
        timesteps_horizon = self.environment.timer.timesteps_horizon
        heat = np.zeros((timesteps_horizon, len(self.t_flow)))
        power = np.zeros((timesteps_horizon, len(self.t_flow)))
        
        # Compute first interpolation
        for i in range(len(self.t_flow)):
            heat[:,i] = np.interp(t_ambient, self.t_ambient, self.heat[:,i])
            power[:,i] = np.interp(t_ambient, self.t_ambient, self.power[:,i])
        
        # Initialize final results
        heatNominal  = np.zeros(timesteps_horizon)
        powerNominal = np.zeros(timesteps_horizon)
        for j in range(timesteps_horizon):
            heatNominal[j] = np.interp(t_flow[j], self.t_flow, heat[j,:])
            powerNominal[j] = np.interp(t_flow[j], self.t_flow, power[j,:])
            
        # Return results
        return (powerNominal, heatNominal, 
                self.t_max, self.lower_activation_limit)
        
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
            Electricity consumption of the heat pump
        qOutput : array-like
            Heat production of the heat pump
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
