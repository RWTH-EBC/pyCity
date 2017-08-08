#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 14:55:09 2015

@author: tsz
"""

from __future__ import division
import numpy as np

import pycity_base.classes.supply.Inverter as Inverter

import pycity_base.classes.Timer
import pycity_base.classes.Weather
import pycity_base.classes.Prices
import pycity_base.classes.Environment

def run_test():
    # Create environment
    timer = pycity_base.classes.Timer.Timer()
    weather = pycity_base.classes.Weather.Weather(timer, useTRY=True)
    prices = pycity_base.classes.Prices.Prices()
    environment = pycity_base.classes.Environment.Environment(timer, weather, prices)

    # Create Inverter
    p_nominal = 10000
    eta = 0.98
    inverter = Inverter.Inverter(environment, eta, p_nominal)

    # Print results
    print()
    print(("Efficiency: "               + str(inverter.eta)))
    print(("Maximum electrical input: " + str(inverter.pNominal)))
    print(("Inverter input AC: "        + str(inverter)))

    print()
    print(("Nominals: " + str(inverter.getNominalValues())))

    np.random.seed(0)
    results_p_in = np.random.rand(timer.timestepsUsedHorizon) * p_nominal
    results_p_out = results_p_in * inverter.eta
    inverter.setResults(results_p_in, results_p_out)

    results = inverter.getResults(True)
    print()
    print("Electricity input: " + str(results[0]))
    print()
    print("Electricity output: " + str(results[1]))

if __name__ == '__main__':
    #  Run program
    run_test()
