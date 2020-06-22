#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cooling demand class
"""

from __future__ import division

import pycity_base.classes.demand.load as Load


class CoolingDemand(Load.Load):
    """
    Implementation of the cooling demand object
    """

    def __init__(self,
                 environment,
                 loadcurve=[],
                 method=0):
        """
        Constructor of CoolingDemand object

        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        method : Integer, optional
            - `0` : Provide load curve directly (for all timesteps!)
            (default: 0)
        loadcurve : Array-like, optional
            Load curve for all investigated time steps in Watt
            (default: []).
        """
        self._kind = "coolingdemand"

        if method not in [0]:
            msg = 'Method ' + str(method) + ' has not been implemented!'
            raise AssertionError(msg)

        if method == 0:
            super(CoolingDemand, self).__init__(environment=environment,
                                                loadcurve=loadcurve)

    @property
    def kind(self):
        return self._kind

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

        return self._getLoadcurve(currentValues)
