#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cooling demand class
"""

from __future__ import division
import pycity_base.classes.supply.coolingdevice as coolingdevice


class Chiller(coolingdevice.CoolingDevice):
    """
    Implementation of the chiller
    """

    def __init__(self,
                 environment,
                 q_nominal,
                 epsilon,
                 t_min=4,
                 lower_activation_limit=1):
        """
        Parameter
        ---------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        q_nominal : array of float
            nominal cooling output in Watt
        epsilon : array of float
            efficiency (without unit)
        t_min : Integer, optional
            minimum provided temperature in °C
        lower_activation_limit : Float (0 <= lower_activation_limit <= 1)
            Define the lower activation limit. For example, heat pumps are
            typically able to operate between 50 % part load and rated load.
            In this case, lower_activation_limit would be 0.5
            Two special cases:
            Linear behavior: lower_activation_limit = 0
            Two-point controlled: lower_activation_limit = 1
        """

        super(Chiller, self).__init__(environment,
                                      q_nominal,
                                      t_min,
                                      lower_activation_limit)
        self._kind = "chiller"
        self.epsilon = epsilon

    def get_results(self, current_values=True):
        """
        Return results.

        Parameter
        ---------
        current_values : boolean, optional
            - True : Return only values for this scheduling period
            - False : Return values for all scheduling periods

        Order
        -----
        q_output : array_like
            cooling production of the chiller
        schedule : array_like
            Operational schedule
        """
        return (self._get_q_output(current_values),
                self._get_schedule(current_values))

    def set_results(self, q_output, schedule):
        """
        Save resulting cooling output and operational schedule.
        """
        self._set_schedule(schedule)
        self._set_q_output(q_output)

    def get_nominal_values(self):
        """
        Get the chiller's efficiency, nominal cooling output, minimal flow
        temperature and lower activation limit.
        """
        return (
            self.epsilon,
            self.q_nominal,
            self.t_min,
            self.lower_activation_limit)
