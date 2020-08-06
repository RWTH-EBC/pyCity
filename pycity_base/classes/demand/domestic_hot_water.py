#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 08 22:39:15 2015

@author: tsz
"""

from __future__ import division

import os
import numpy as np
import pycity_base.classes.demand.load
from pycity_base.functions import change_resolution as chres
from pycity_base.functions import dhw_stochastical as dhw_sto


class DomesticHotWater(pycity_base.classes.demand.load.Load):
    """
    Implementation of the domestic hot water (DHW) object
    """

    loaded_profile = False
    loaded_dhw_sto = False
    water = None
    a42 = []  # Tap water consumption profiles given in Annex 42
    dhw_sto_profiles = {}

    def __init__(self,
                 environment,
                 t_flow,
                 thermal=True,
                 method=0,
                 loadcurve=[],
                 daily_consumption=0,
                 supply_temperature=0,
                 occupancy=[]):
        """
        Parameters
        ----------
        environment : environment object
            Common to all other objects. Includes time and weather instances
        t_flow : float
            Flow temperature of domestic hot water in degree Celsius.
        thermal : boolean, optional
            Is the DHW provided electrically (False) or via thermal energy
            storage (True)
        method : integer, optional
            - `0` : Provide load curve directly (for all timesteps!)
            - `1` : Load profile from Annex 42
            - `2` : Stochastical method
        loadcurve : array-like, optional
            Load curve for all investigated time steps (in Watt).
            This parameter is required when using ``method=0``.
        daily_consumption : float, optional
            Average, total domestic hot water consumption in liters/day.
            This parameter is required when using ``method=1``.
        supply_temperature : float, optional
            Supply temperature in degree Celsius. This parameter is necessary
            to compute the heat load that results from each liter consumption.
            This parameter is required when using ``method=1``.

        Info
        ----
        The load profiles from Annex 42 can be found here:
        http://www.ecbcs.org/annexes/annex42.htm
        """
        self.method = method
        if method == 0:
            super(DomesticHotWater, self).__init__(environment, loadcurve)
        elif method == 1:
            timeDis = environment.timer.time_discretization
            # If not already done, load the Annex 42 profile
            if not DomesticHotWater.loaded_profile:
                src_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                filename = os.path.join(src_path, 'inputs', 'standard_load_profile', 'dhw_annex42.csv')
                DomesticHotWater.a42 = np.loadtxt(filename,
                                                  skiprows=1, delimiter="\t")
                DomesticHotWater.loaded_profile = True

            # Adjust time resolution. Annex 42 data is sampled at 900 sec.
            if timeDis != 900:
                res = []
                changeResol = chres.changeResolution
                for i in range(3):
                    res.append(changeResol(DomesticHotWater.a42[:, i],
                                           oldResolution=900,
                                           newResolution=timeDis,
                                           method="mean"))
                a42 = np.transpose(np.array(res))
            else:
                a42 = DomesticHotWater.a42

            # Compute tap water profile (based on average daily consumption)
            if daily_consumption <= 150:
                tapProfile = a42[:, 0] * daily_consumption / 100
            elif daily_consumption <= 250 and daily_consumption > 150:
                tapProfile = a42[:, 1] * daily_consumption / 200
            elif daily_consumption > 250:
                tapProfile = a42[:, 2] * daily_consumption / 300

            # Compute equivalent heat demand in Watt
            c_water = 4180  # J/kgK
            flowFactor = 1 / 3600  # l/h -> kg/s
            deltaTemperature = t_flow - supply_temperature
            loadcurve = c_water * tapProfile * flowFactor * deltaTemperature
            super(DomesticHotWater, self).__init__(environment, loadcurve)
        elif method == 2:
            # Load profiles
            if not DomesticHotWater.loaded_dhw_sto:
                src_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                loc = os.path.join(src_path, 'inputs', 'dhw_stochastical.xlsx')
                DomesticHotWater.dhw_sto_profiles = dhw_sto.load_profiles(loc)
                DomesticHotWater.loaded_dhw_sto = True

            # Compute dhw demand
            profiles = DomesticHotWater.dhw_sto_profiles
            initial_day = environment.timer.current_day
            timeDis = environment.timer.time_discretization
            tempDiff = t_flow - supply_temperature
            (water, heat) = dhw_sto.full_year_computation(occupancy, profiles,
                                                          timeDis, initial_day,
                                                          tempDiff)

            self.water = water
            super(DomesticHotWater, self).__init__(environment, heat)

        self._kind = "domestichotwater"
        self.t_flow = t_flow
        self.thermal = thermal

    @property
    def kind(self):
        return self._kind

    def get_power(self, currentValues=True, returnTemperature=True):
        """
        Get the domestic hot water power curve
        (and the required flow temperature).

        Parameters
        ----------
        currentValues : Boolean, optional
            Return only current values (True) or the entire load (False)
            (default: True)
        returnTemperature : Boolean, optional
            Also return the required flow temperature (True)
            (default: True)

        Returns
        -------
        If returnTemperature is True:
        result_tuple : tuple (load, t_flow)
            Result tuple with thermal power curve and return temperature curve

        else (returnTemperature is False):
        load : np.array
            Thermal hot water power curve
        """
        if self.method in (0, 1, 2):
            load = self._getLoadcurve(currentValues)

        if returnTemperature:
            t_flow = np.zeros_like(load)
            t_flow[load > 0] = self.t_flow

            return (load, t_flow)
        else:
            return load
