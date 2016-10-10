#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 14:32:46 2015

@author: tsz
"""

from __future__ import division
import numpy as np

import pycity.classes.Timer
import pycity.classes.Weather
import pycity.classes.Environment
import pycity.classes.Prices

import pycity.classes.supply.Boiler as Boiler

def run_test():
    # Create environment
    timer = pycity.classes.Timer.Timer()
    weather = pycity.classes.Weather.Weather(timer, useTRY=True)
    prices = pycity.classes.Prices.Prices()
    environment = pycity.classes.Environment.Environment(timer, weather, prices)

    # Create Boiler
    lower_activation_limit = 0.5
    q_nominal = 10000
    t_max = 90
    eta = 0.9
    heater = Boiler.Boiler(environment, q_nominal, eta, t_max,
                           lower_activation_limit)

    # Print results
    print()
    print(("Type: " + heater._kind))
    print(("Efficiency: "                 + str(heater.eta)))
    print(("Maximum heat output: "        + str(heater.qNominal)))
    print(("Maximum flow temperature: "   + str(heater.tMax)))
    print(("Lower activation limit: "     + str(heater.lowerActivationLimit)))


    print()
    print(("Nominals: " + str(heater.getNominalValues())))

    np.random.seed(0)
    result_q = np.random.rand(timer.timestepsUsedHorizon) * q_nominal
    result_schedule = np.random.randint(2, size=timer.timestepsUsedHorizon)
    heater.setResults(result_q, result_schedule)

    results = heater.getResults(True)
    print()
    print("Heat output: " + str(results[0]))
    print()
    print("Schedule: " + str(results[1]))

if __name__ == '__main__':
    #  Run program
    run_test()