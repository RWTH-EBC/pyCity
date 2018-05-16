#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cooling demand class
"""

from __future__ import division
import numpy as np


class CoolingDemand(pycity_base.classes.demand.Load.Load):
    """
    Implementation of the cooling demand object
    """

    def __init__(self,
                 environment,
                 loadcurve=[]):
        """
        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances

        method : Integer, optional
            - `0` : Provide load curve directly (for all timesteps!)

        loadcurve : Array-like
            Load curve for all investigated time steps

        """

        src_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

        if method == 0:
            super(CoolingDemand, self).__init__(environment, loadcurve)

    def get_power(self, currentValues=True):
        """
        Return cooling power curve

        Parameters
        ----------
        currentValues : bool, optional
            Return only current values (True) or the entire load (False)
            (default: True)

        Return
        ------
        loadcurve : np.array
            Cooling power curve
        """
        if self.method in (0, 1, 2, 3, 4):
            return self._getLoadcurve(currentValues)
