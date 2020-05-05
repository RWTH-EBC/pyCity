#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example of the heating device class.
"""

from __future__ import division

import pycity_base.classes.supply.heating_device as hd
import numpy as np

import pycity_base.classes.timer
import pycity_base.classes.weather
import pycity_base.classes.prices
import pycity_base.classes.environment


def run_example():
    # Create environment
    timer = pycity_base.classes.timer.Timer()
    weather = pycity_base.classes.weather.Weather(timer, useTRY=True)
    prices = pycity_base.classes.prices.Prices()
    environment = pycity_base.classes.environment.Environment(timer, weather, prices)

    # Create Heating Device
    lowerActivationLimit = 0.5
    qNominal = 5000
    tMax = 70
    heater = hd.HeatingDevice(environment, qNominal, tMax, lowerActivationLimit)

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
    run_example()
