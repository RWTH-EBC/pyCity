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
    weather = pycity_base.classes.weather.Weather(timer, use_TRY=True)
    prices = pycity_base.classes.prices.Prices()
    environment = pycity_base.classes.environment.Environment(timer, weather, prices)

    # Create Heating Device
    lower_activation_limit = 0.5
    q_nominal = 5000
    t_max = 70
    heater = hd.HeatingDevice(environment, q_nominal, t_max, lower_activation_limit)

    np.random.seed(0)
    someSchedule = np.random.randint(low=0, high=2,
                                     size=environment.timer.timesteps_used_horizon)

    # Print results
    print()
    print("Lower activation limit: " + str(heater.lower_activation_limit))
    print("Nominal heat output: " + str(heater.q_nominal))
    print("Maximum flow temperature: " + str(heater.t_max))
    print("Previous schedule: " + str(heater._getSchedule(True)))

    heater._setSchedule(someSchedule)
    print()
    print("Current schedule: " + str(heater._getSchedule(True)))


if __name__ == '__main__':
    #  Run program
    run_example()
