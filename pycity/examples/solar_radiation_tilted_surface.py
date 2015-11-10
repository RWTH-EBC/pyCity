#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 08 22:07:49 2015

@author: Thomas
"""

from __future__ import division
import pycity.classes.Timer
import pycity.classes.Weather
import pycity.classes.Environment


def run_example():
    # Create environment
    # Initialize the timer object for a full year computation, without rolling
    # horizon and hourly time discretization
    timer = pycity.classes.Timer.Timer(3600, 8760, 8760, 8760)
    weather = pycity.classes.Weather.Weather(timer)
    environment = pycity.classes.Environment.Environment(timer, weather, None)

    # Surface definition
    beta = 30 # Slope, degree (not radians)
    gamma = 0 # Azimuth angle, degree (not radians)

    # Compute solar radiation on a tilted surface
    function = weather.getRadiationTiltedSurface
    solar_radiation_tilted_surface = function(beta, gamma, update=True)

    # The result is a tuple with four entries:
    # 0. Total radiation on the given surface
    # 1. Diffuse radiation on the given surface
    # 2. Direct radiation on the given surface
    # 3. Reflected radiation from the ground on the given surface
    # (The total radiation (index 0) is the sum of the other three)

    total_radiation = solar_radiation_tilted_surface[0]
    diffuse_radiation = solar_radiation_tilted_surface[1]
    direct_radiation = solar_radiation_tilted_surface[2]
    reflected_radiation = solar_radiation_tilted_surface[3]

if __name__ == '__main__':
    run_example()