#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 20:26:30 2015

@author: tsz
"""

from __future__ import division


class Environment(object):
    """
    This class keeps track of the simulation time and the weather conditions.
    """

    def __init__(self, timer, weather, prices, location=(50.76, 6.07)):
        """
        Parameters
        ----------
        timer : Timer object
            Handles current timestep, time discretization and horizon lengths.
        weather : Weather object
            Includes ambient temperature, solar radiation (diffuse, direct),
            relative humidity, air pressure and wind velocity
        prices : Prices object
            Definition of electricity price, remuneration ...
        location : Tuple, optional
            (longitude, latitude) of the simulated system's position. Standard
            values (50.76, 6.07) represent Aachen, Germany.
        """
        self._kind = "environment"
        self.timer = timer
        self.weather = weather
        self.prices = prices
        self.location = location

    @property
    def kind(self):
        return self._kind
    
    def update(self):
        """
        Increase the current timestep and the current day.
        """
        self.timer.update()
        self.weather.update()
