#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 14:25:16 2015

@author: tsz
"""

from __future__ import division
import numpy as np

import pycity_base.classes.supply.CHP as CHP

import pycity_base.classes.Timer
import pycity_base.classes.Weather
import pycity_base.classes.Prices
import pycity_base.classes.Environment

def run_test():
    # Create environment
    timer = pycity.classes.Timer.Timer()
    weather = pycity.classes.Weather.Weather(timer, useTRY=True)
    prices = pycity.classes.Prices.Prices()
    environment = pycity.classes.Environment.Environment(timer, weather, prices)

    # Create CHP
    lower_activation_limit = 0.5
    q_nominal = 10000
    t_max = 90
    p_nominal = 6000
    omega = 0.9
    heater = CHP.CHP(environment, p_nominal, q_nominal, omega, t_max,
                     lower_activation_limit)

    # Print results
    print()
    print(("Type: " + heater._kind))
    print()
    print(("Maximum electricity output: " + str(heater.pNominal)))
    print(("Total efficiency: "           + str(heater.omega)))
    print(("Power to heat ratio: "        + str(heater.sigma)))
    print(("Maximum heat output: "        + str(heater.qNominal)))
    print(("Maximum flow temperature: "   + str(heater.tMax)))
    print(("Lower activation limit: "     + str(heater.lowerActivationLimit)))

    print()
    print(("Nominals: " + str(heater.getNominalValues())))

    np.random.seed(0)
    result_p = np.random.rand(timer.timestepsUsedHorizon) * p_nominal
    result_q = np.random.rand(timer.timestepsUsedHorizon) * q_nominal
    result_schedule = np.random.randint(2, size=timer.timestepsUsedHorizon)
    heater.setResults(result_p, result_q, result_schedule)

    results = heater.getResults(True)
    print()
    print("Electricity output: " + str(results[0]))
    print()
    print("Heat output: " + str(results[1]))
    print()
    print("Schedule: " + str(results[2]))

if __name__ == '__main__':
    #  Run program
    run_test()
