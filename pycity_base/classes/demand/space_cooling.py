#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 09 08:42:07 2020

@author: ssw
"""

from __future__ import division

import warnings
import numpy as np
import pycity_base.classes.demand.load


class SpaceCooling(pycity_base.classes.demand.load.Load):
    """
    Implementation of the space cooling object
    """

    loaded_slp = False
    slp_hour = []
    slp_prof = []
    slp_week = []

    loaded_sim_profile = False
    sim_prof_data = None

    def __init__(self, environment, method=0, loadcurve=[],
                 living_area=0, specific_demand=0, profile_type='HEF'):
        """
        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        method : integer, optional
            - `0` : Provide load curve directly
            - `1` : Use thermal standard load profile (not implemented yet!)
        loadcurve : Array-like, optional
            Load curve for all investigated time steps
            Requires ``method=0``
        living_area : Float, optional
            Living area of the apartment in m^2
            Requires ``method=1``
        specific_demand : Float, optional
            Specific thermal demand of the building in kWh/(m^2 a)
            Requires ``method=1``
        profile_type : str, optional
            Thermal SLP profile name
            Requires ``method=1``
            - `HEF` : Single family household
            - `HMF` : Multi family household
            - `GBA` : Bakeries
            - `GBD` : Other services
            - `GBH` : Accomodations
            - `GGA` : Restaurants
            - `GGB` : Gardening
            - `GHA` : Retailers
            - `GHD` : Summed load profile business, trade and services
            - `GKO` : Banks, insurances, public institutions
            - `GMF` : Household similar businesses
            - `GMK` : Automotive
            - `GPD` : Paper and printing
            - `GWA` : Laundries
        """
        self.method = method

        if method == 0:
            #  Hand over own power curve
            super(SpaceCooling, self).__init__(environment, loadcurve)

        elif method == 1:
            #  Generate standardized thermal load profile (SLP)
            if living_area > 0 or specific_demand > 0:
                warnings.warn("SLP functionality for space cooling objects not implemented yet."
                              "Using a zero cooling load profile instead.")
            super(SpaceCooling, self).__init__(environment, np.zeros(environment.timer.timesteps_total))

        self._kind = "spacecooling"

    @property
    def kind(self):
        return self._kind

    def get_power(self, currentValues=True):
        """
        Return space cooling power curve

        Parameters
        ----------
        currentValues : bool, optional
            Return only current values (True) or the entire load (False)
            (default: True)

        Returns
        -------
        loadcurve : np.array
            Power curve of space cooling
        """
        if self.method in (0, 1):
            return self._getLoadcurve(currentValues)
