#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 17:39:01 2015

@author: tsz
"""

from __future__ import division

import numpy as np


class PV(object):
    """
    Implementation of the PV class.
    """
    
    def __init__(self, environment, method, area=0.0, peak_power=0.0, eta_noct=0.18, radiation_noct=1000.0,
                 t_cell_noct=45.0, t_ambient_noct=20.0, alpha_noct=0, beta=0, gamma=0, tau_alpha=0.9):
        """
        Parameters
        ----------
        environment : environment object
            Common to all other objects. Includes time and weather instances
        method : integer
            - `0` : Calculate PV power based on an area in m^2 equipped with PV panels
            - `1` : Calculate PV power based on the installed PV peak power in kWp
        area : float, optional
            PV unit installation area in m^2
            Requires ``method=0``
        peak_power : float, optional
            PV peak power installation in kWp
            Requires ``method=1``
        eta_noct : float, optional
            Electrical efficiency at NOCT conditions (without unit)
            NOCT conditions: See manufacturer's data sheets or
            Duffie, Beckman - Solar Engineering of Thermal Processes (4th ed.), page 759
            Requires ``method=0``
        radiation_noct : float, optional
            Nominal solar radiation at NOCT conditions (in W/m^2)
            NOCT conditions: See manufacturer's data sheets or
            Duffie, Beckman - Solar Engineering of Thermal Processes (4th ed.), page 759
        t_cell_noct : float, optional
            Nominal cell temperature at NOCT conditions (in degree Celsius)
            NOCT conditions: See manufacturer's data sheets or
            Duffie, Beckman - Solar Engineering of Thermal Processes (4th ed.), page 759
        t_ambient_noct : float, optional
            Nominal ambient air temperature at NOCT conditions (in degree Celsius)
            NOCT conditions: See manufacturer's data sheets or
            Duffie, Beckman - Solar Engineering of Thermal Processes (4th ed.), page 759
        alpha_noct : float, optional
            Temperature coefficient at NOCT conditions (without unit)
            NOCT conditions: See manufacturer's data sheets or
            Duffie, Beckman - Solar Engineering of Thermal Processes (4th ed.), page 759
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
        self.method = method

        self.area = area
        self.peak_power = peak_power

        self.eta_noct = eta_noct
        self.radiation_noct = radiation_noct
        self.t_cell_noct = t_cell_noct
        self.t_ambient_noct = t_ambient_noct
        self.alpha_noct = alpha_noct

        self.beta = beta
        self.gamma = gamma
        self.tau_alpha = tau_alpha
        
        self.total_power = np.zeros(environment.timer.timesteps_total)
        self.total_radiation = np.zeros(environment.timer.timesteps_total)
        self.current_power = np.zeros(environment.timer.timesteps_horizon)

    @property
    def kind(self):
        return self._kind

    def getNominalValues(self):
        """
        Return collector's area, efficiency, nominal cell temperature and 
        loss coefficient.
        """
        return (self.eta_noct, self.radiation_noct, self.t_cell_noct, self.t_ambient_noct, self.alpha_noct)

    def _computePowerArea(self, currentValues=True):
        """
        Compute PV electric output power based on a certain area equipped with PV panels

        Parameters
        ----------
        currentValues : bool, optional
            If True, returns values of current horizon (default: True).
            If False, returns annual values.

        Returns
        -------
        res_tuple : tuple
            2d tuple holding power array in Watt and radiation array in W/m^2
        """
        # Get radiation on a tilted surface
        radiation = self.environment.weather.getRadiationTiltedSurface(beta=self.beta,
                                                                       gamma=self.gamma,
                                                                       update=True,
                                                                       currentValues=currentValues)

        # If no temperature coefficient is given, a simple PV model is applied
        if self.alpha_noct == 0:
            power = self.area * self.eta_noct * radiation[0]
        else:
            # Get ambient temperature
            getTemperature = self.environment.weather.getWeatherForecast
            t_ambient = getTemperature(getTAmbient=True, currentValues=currentValues)

            # Compute the cell temperature. 
            # Assumption: Wind velocity is 1 m/s (same as NOCT conditions)
            # The resulting equation is based on equation 23.3.3 (page 758,
            # Duffie, Beckman - Solar Engineering of Thermal Processes, 4th ed)
            # as well as equation 3 (Skroplaki, Palyvos - 2009 - On the 
            # temperature dependence of photovoltaic module electrical 
            # performance. A review of efficiency-power correlations.)
            
            # Introduce a few abbreviations
            a1 = (self.t_cell_noct - self.t_ambient_noct) * radiation[0] / self.radiation_noct
            denominator = 1 - a1 * self.alpha_noct * self.eta_noct / self.tau_alpha
            numerator = 1 - self.alpha_noct * (t_ambient[0] - self.t_cell_noct + a1)
            eta = self.eta_noct * numerator / denominator
        
            # Compute power
            power = self.area * eta * radiation[0]
        
        return (power, radiation[0])

    def _computePowerPeakInstallation(self, currentValues=True):
        """
        Compute PV electric output power based on a given PV peak power installation

        Parameters
        ----------
        currentValues : bool, optional
            If True, returns values of current horizon (default: True).
            If False, returns annual values.

        Returns
        -------
        res_tuple : tuple
            2d tuple holding power array in Watt and radiation array in W/m^2
        """
        # Get radiation on a tilted surface
        radiation = self.environment.weather.getRadiationTiltedSurface(beta=self.beta,
                                                                       gamma=self.gamma,
                                                                       update=True,
                                                                       currentValues=currentValues)

        # Get ambient temperature
        getTemperature = self.environment.weather.getWeatherForecast
        t_ambient = getTemperature(getTAmbient=True, currentValues=currentValues)

        # Calculation of PV power output according to:
        # "A novel model for photovoltaic array performance prediction"
        # Wei Zhou et. al., in Applied Energy 84 (2007), pp. 1187-1198

        # Constants:
        q = 1.602 * np.power(10.0, -19.0)
        n = 1.3
        K = 1.38 * np.power(10.0, -23.0)
        Kelvin = 273.15

        # Reference module parameters (monocrystalline module):
        P_max_mp = 250.0
        V_mp = 31.1
        I_mp = 8.05
        R_s = 0.012
        Alpha_module = 1.21
        Beta_module = 0.058
        Gamma_module = 0.012

        # Variables:
        I_sc = 0.0  # Short circuit current
        V_oc = 0.0  # Open circuit voltage
        V_oc_norm = 0.0  # Normalized open circuit voltage
        FF_o = 0.0  # Fill factor at ideal PV module
        FF = 0.0  # Fill factor
        P_module = np.zeros(len(radiation[0]))  # PV power output per module

        # Straight forward calculation of PV power:
        for i in range(len(radiation[0])):
            if radiation[0][i] <= 0.0:
                I_sc = 0.0
            else:
                I_sc = I_mp * np.power((radiation[0][i] / self.radiation_noct), Alpha_module)

            if (t_ambient[0][i] + Kelvin) == 0.0 or radiation[0][i] <= 0.0:
                V_oc = 0.0
            else:
                if (1 + Beta_module * np.log(self.radiation_noct / radiation[0][i])) == 0.0:
                    V_oc = 0.0
                else:
                    V_oc = (V_mp / (1 + Beta_module * np.log(self.radiation_noct / radiation[0][i]))) * \
                           np.power(((self.t_ambient_noct + Kelvin) / (t_ambient[0][i] + Kelvin)), Gamma_module)

            if (t_ambient[0][i] + Kelvin) == 0.0:
                V_oc_norm = 0.0
            else:
                V_oc_norm = (V_oc / (n * K * (t_ambient[0][i] + Kelvin) / q))

            if (1 + V_oc_norm) == 0.0:
                FF_o = 0.0
            else:
                FF_o = (V_oc_norm - np.log(V_oc_norm + 0.72)) / (1 + V_oc_norm)

            if V_oc == 0.0 or I_sc == 0.0:
                FF = 0.0
            else:
                FF = FF_o * (1 - (R_s / (V_oc / I_sc)))

            P_module[i] = FF * V_oc * I_sc

        n_modules = int(1000.0*self.peak_power/P_max_mp)
        power = np.array(P_module)*n_modules

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
        current_timestep = self.environment.timer.current_timestep
        timesteps = self.environment.timer.timesteps_horizon

        if self.method in (0, 1):
            if updatePower:
                if self.method == 0:
                    (current_power, currentRadiation) = self._computePowerArea(currentValues=currentValues)
                elif self.method == 1:
                    (current_power, currentRadiation) = self._computePowerPeakInstallation(currentValues=currentValues)

                if currentValues:
                    self.current_power = current_power

                    self.total_power[current_timestep:(current_timestep + timesteps)] = current_power
                    self.total_radiation[current_timestep:(current_timestep + timesteps)] = currentRadiation
                    return self.current_power

                else:
                    self.total_power = current_power
                    self.total_radiation = currentRadiation
                    return self.total_power
