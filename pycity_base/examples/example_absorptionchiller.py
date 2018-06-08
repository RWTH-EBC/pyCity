#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example of the chiller class
"""

from __future__ import division
import numpy as np

import pycity_base.classes.Timer
import pycity_base.classes.Weather
import pycity_base.classes.Environment
import pycity_base.classes.Prices

import pycity_base.classes.supply.absorptionchiller as achill


def run_test():
    # Create environment
    timer = pycity_base.classes.Timer.Timer()
    weather = pycity_base.classes.Weather.Weather(timer, useTRY=True)
    prices = pycity_base.classes.Prices.Prices()
    environment = pycity_base.classes.Environment.Environment(
        timer, weather, prices)

    # Create Chiller
    lower_activation_limit = 0.3
    q_nominal = 10000
    t_min = 4
    epsilon = 0.6
    achiller = achill.AbsorptionChiller(
        environment, q_nominal, epsilon, t_min, lower_activation_limit)

    # Print results
    print()
    print(("Type: " + achiller._kind))
    print(("Efficiency: " + str(achiller.epsilon)))
    print(("Maximum cooling output: " + str(achiller.q_nominal)))
    print(("Minimal flow temperature: " + str(achiller.t_min)))
    print(("Lower activation limit: " + str(achiller.lower_activation_limit)))

    print()
    print(("Nominals: " + str(achiller.get_nominal_values())))

    np.random.seed(0)
    result_q = np.random.rand(timer.timestepsUsedHorizon) * q_nominal
    result_schedule = np.random.randint(2, size=timer.timestepsUsedHorizon)
    achiller.set_results(result_q, result_schedule)

    results = achiller.get_results(True)
    print()
    print("Cooling output: " + str(results[0]))
    print()
    print("Schedule: " + str(results[1]))


if __name__ == '__main__':
    #  Run program
    run_test()
