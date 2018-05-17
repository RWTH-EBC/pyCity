#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CoolingDevice example
"""

from __future__ import division
import pycity_base.classes.supply.CoolingDevice as CoolingDevice
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
    lowerActivationLimit = 0.2
    qNominal = 5000
    tMin = 5
    cooler = CoolingDevice.CoolingDevice(environment,
                                         qNominal,
                                         tMin,
                                         lowerActivationLimit)
    np.random.seed(0)
    someSchedule = np.random.randint(
        low=0,
        high=2,
        size=environment.timer.timestepsUsedHorizon)

    # Print results
    print()
    print("Lower activation limit: " + str(cooler.lowerActivationLimit))
    print("Nominal cooling output: " + str(cooler.qNominal))
    print("Minimal flow temperature: " + str(cooler.tMin))
    print("Previous schedule: " + str(cooler._getSchedule(True)))

    cooler._setSchedule(someSchedule)
    print()
    print("Current schedule: " + str(cooler._getSchedule(True)))

if __name__ == '__main__':
    #  Run program
    run_test()
