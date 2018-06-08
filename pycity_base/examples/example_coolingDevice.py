#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CoolingDevice example
"""

from __future__ import division
import pycity_base.classes.supply.coolingdevice as coolingdevice
import numpy as np

import pycity_base.classes.Timer
import pycity_base.classes.Weather
import pycity_base.classes.Prices
import pycity_base.classes.Environment


def run_test():
    # Create environment
    timer = pycity_base.classes.Timer.Timer()
    weather = pycity_base.classes.Weather.Weather(timer, useTRY=True)
    prices = pycity_base.classes.Prices.Prices()
    environment = pycity_base.classes.Environment.Environment(
        timer, weather, prices)

    # Create Cooling Device
    lower_activation_limit = 0.2
    q_nominal = 5000
    t_min = 5
    cooler = coolingdevice.CoolingDevice(environment,
                                         q_nominal,
                                         t_min,
                                         lower_activation_limit)
    np.random.seed(0)
    some_schedule = np.random.randint(
        low=0,
        high=2,
        size=environment.timer.timestepsUsedHorizon)

    # Print results
    print()
    print("Lower activation limit: " + str(cooler.lower_activation_limit))
    print("Nominal cooling output: " + str(cooler.q_nominal))
    print("Minimal flow temperature: " + str(cooler.t_min))
    print("Previous schedule: " + str(cooler._get_schedule(True)))

    cooler._set_schedule(some_schedule)
    print()
    print("Current schedule: " + str(cooler._get_schedule(True)))

if __name__ == '__main__':
    #  Run program
    run_test()
