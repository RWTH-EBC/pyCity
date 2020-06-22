#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example of the absorption chiller class.
"""

from __future__ import division

import numpy as np

import pycity_base.classes.timer
import pycity_base.classes.weather
import pycity_base.classes.environment
import pycity_base.classes.prices

import pycity_base.classes.supply.absorption_chiller as achill


def run_example():
    # Create environment
    timer = pycity_base.classes.timer.Timer()
    weather = pycity_base.classes.weather.Weather(timer, use_TRY=True)
    prices = pycity_base.classes.prices.Prices()
    environment = pycity_base.classes.environment.Environment(
        timer, weather, prices)

    # Create Chiller
    lower_activation_limit = 0.3
    q_nominal = 10000
    t_min = 4
    epsilon = 0.6
    achiller = achill.AbsorptionChiller(environment, q_nominal, epsilon, t_min, lower_activation_limit)

    # Print results
    print()
    print(("Type: " + achiller.kind))
    print(("Efficiency: " + str(achiller.epsilon)))
    print(("Maximum cooling output: " + str(achiller.q_nominal)))
    print(("Minimal flow temperature: " + str(achiller.t_min)))
    print(("Lower activation limit: " + str(achiller.lower_activation_limit)))

    print()
    print(("Nominals: " + str(achiller.get_nominal_values())))

    np.random.seed(0)
    result_q = np.random.rand(timer.timesteps_used_horizon) * q_nominal
    result_schedule = np.random.randint(2, size=timer.timesteps_used_horizon)
    achiller.set_results(result_q, result_schedule)

    results = achiller.get_results(True)
    print()
    print("Cooling output: " + str(results[0]))
    print()
    print("Schedule: " + str(results[1]))


if __name__ == '__main__':
    #  Run program
    run_example()
