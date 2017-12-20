#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 17:39:01 2015

@author: tsz
"""

from __future__ import division
import numpy as np
import pycity_base.functions.handleData


class PV(object):
    """
    Implementation of the PV class.
    """
    
    def __init__(self, environment, area, eta, temperature_nominal=45,
                 alpha=0, beta=0, gamma=0, tau_alpha=0.9):
        """
        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        area : integer
            installation area in m2
        eta : float
            Electrical efficiency at NOCT conditions (without unit)
        temperature_nominal : float
            Nominal cell temperature at NOCT conditions (in degree Celsius)
        alpha : float
            Temperature coefficient at NOCT conditions
        beta : float, optional
            Slope, the angle (in degree) between the plane of the surface in 
            question and the horizontal. 0 <= beta <= 180. If beta > 90, the 
            surface faces downwards.
        gamma : float, optional
            Surface azimuth angle. The deviation of the projection on a 
            horizontal plane of the normal to the surface from the local 
            meridian, with zero due south, east negative, and west positive.
            -180 <= gamma <= 180
        tau_alpha : float
            Optical properties of the PV unit. Product of absorption and 
            transmission coeffients.
            According to Duffie, Beckman - Solar Engineering of Thermal 
            Processes (4th ed.), page 758, this value is typically close to 0.9
        """
        self._kind = "pv"        
        
        self.environment = environment
        self.area = area
        self.eta = eta
        
        self.temperature_nominal = temperature_nominal
        self.alpha = alpha
        self.tau_alpha = tau_alpha
        
        self.totalPower     = np.zeros(environment.timer.timestepsTotal)
        self.totalRadiation = np.zeros(environment.timer.timestepsTotal)
        self.currentPower   = np.zeros(environment.timer.timestepsHorizon)
        
        self.beta = beta
        self.gamma = gamma

    def getNominalValues(self):
        """
        Return collector's area, efficiency, nominal cell temperature and 
        loss coefficient.
        """
        return (self.area, self.eta, self.temperature_nominal, self.alpha)

    def _computePower(self, current_values=True):
        """
        Compute PV electric output power

        Parameters
        ----------
        current_values : bool, optional
            If True, returns values of current horizon (default: True).
            If False, returns annual values.

        Returns
        -------
        res_tuple : tuple
            2d tuple holding power array in Watt and radiation array in W/m2
        """
        # Get radiation on a tilted surface
        radiation = self.environment.\
            weather.getRadiationTiltedSurface(beta=self.beta,
                                              gamma=self.gamma,
                                              update=True,
                                              current_values=current_values)

        # If no temperature coefficient is given, a simple PV model is applied
        if self.alpha == 0:
            power = self.area * self.eta * radiation[0]
        else:
            # Get ambient temperature
            getTemperature = self.environment.weather.getWeatherForecast
            t_ambient = getTemperature(getTAmbient=True)
            
            # NOCT conditions - see manufacturer's data sheets or 
            # Duffie, Beckman - Solar Engineering of Thermal Processes (4th 
            # ed.), page 759
            radiation_NOCT = 800 # W/m2
            t_ambient_NOCT = 20  # °C
            t_cell_NOCT = 45     # °C
            
            # Compute the cell temperature. 
            # Assumption: Wind velocity is 1 m/s (same as NOCT conditions)
            # The resulting equation is based on equation 23.3.3 (page 758,
            # Duffie, Beckman - Solar Engineering of Thermal Processes, 4th ed)
            # as well as equation 3 (Skroplaki, Palyvos - 2009 - On the 
            # temperature dependence of photovoltaic module electrical 
            # performance. A review of efficiency-power correlations.)
            
            # Introduce a few abbreviations
            a1 = (t_cell_NOCT - t_ambient_NOCT) * radiation[0] / radiation_NOCT
            denominator = 1 - a1 * self.alpha * self.eta / self.tau_alpha
            numerator = 1 - self.alpha * (t_ambient[0] - t_cell_NOCT + a1)
            eta = self.eta * numerator / denominator
        
            # Compute power
            power = self.area * eta * radiation[0]
        
        return (power, radiation[0])
    
    def getPower(self, currentValues=True, updatePower=True):
        """ 
        Get the PV generation. 

        Parameters
        ----------
        currentValues : Boolean, optional
            - True : Return the PV generation array for the current forecasting 
                     horizon
            - False : Return the entire PV generation array for all previous 
                      time steps
        updatePower : Boolean, optional
            - True: Compute the PV generation forecast for the upcoming horizon
            - False: Do not compute a new PV generation forecast
        """
        currentTimestep = self.environment.timer.currentTimestep
        timesteps = self.environment.timer.timestepsHorizon

        if updatePower:
            (currentPower, currentRadiation) = self._computePower\
                (current_values=currentValues)

            if currentValues:
                self.currentPower = currentPower

                self.totalPower[currentTimestep : (currentTimestep +
                                                   timesteps)] = currentPower
                self.totalRadiation[currentTimestep : (currentTimestep +
                                                   timesteps)] = currentRadiation
                return self.currentPower

            else:
                self.totalPower = currentPower
                self.totalRadiation = currentRadiation
                return self.totalPower
