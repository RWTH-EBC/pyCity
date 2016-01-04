#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 14:19:59 2015

@author: tsz
"""

from __future__ import division
import pycity.classes.supply.HeatingDevice as HeatingDevice
import numpy as np

import pycity.classes.Timer
import pycity.classes.Weather
import pycity.classes.Prices
import pycity.classes.Environment

def run_test():
    # Create environment
    timer = pycity.classes.Timer.Timer()
    weather = pycity.classes.Weather.Weather(timer, useTRY=True)
    prices = pycity.classes.Prices.Prices()
    environment = pycity.classes.Environment.Environment(timer, weather, prices)

    # Create Heating Device
    lowerActivationLimit = 0.5
    qNominal = 5000
    tMax = 70
    heater = HeatingDevice.HeatingDevice(environment,
                                         qNominal,
                                         tMax,
                                         lowerActivationLimit)

    np.random.seed(0)
    someSchedule = np.random.randint(low=0, high=2,
                                     size=environment.timer.timestepsUsedHorizon)

    # Print results
    print()
    print("Lower activation limit: " + str(heater.lowerActivationLimit))
    print("Nominal heat output: " + str(heater.qNominal))
    print("Maximum flow temperature: " + str(heater.tMax))
    print("Previous schedule: "      + str(heater._getSchedule(True)))

    heater._setSchedule(someSchedule)
    print()
    print("Current schedule: " + str(heater._getSchedule(True)))

if __name__ == '__main__':
    #  Run program
    run_test()
