#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example of the inverter class.
"""

from __future__ import division

import numpy as np

import pycity_base.classes.supply.inverter as inv

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

    # Create Inverter
    p_nominal = 10000
    eta = 0.98
    inverter = inv.Inverter(environment, eta, p_nominal)

    # Print results
    print()
    print(("Efficiency: " + str(inverter.eta)))
    print(("Maximum electrical input: " + str(inverter.p_nominal)))
    print(("Inverter input AC: " + str(inverter)))

    print()
    print(("Nominals: " + str(inverter.getNominalValues())))

    np.random.seed(0)
    results_p_in = np.random.rand(timer.timesteps_used_horizon) * p_nominal
    results_p_out = results_p_in * inverter.eta
    inverter.setResults(results_p_in, results_p_out)

    results = inverter.getResults(True)
    print()
    print("Electricity input: " + str(results[0]))
    print()
    print("Electricity output: " + str(results[1]))


if __name__ == '__main__':
    #  Run program
    run_example()
