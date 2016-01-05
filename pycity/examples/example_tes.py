#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 14:37:31 2015

@author: tsz
"""

from __future__ import division

import numpy as np
import pycity.classes.supply.ThermalEnergyStorage as ThermalEnergyStorage

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
    t_init = 20 # °C
    capacity = 1000 # kg
    t_max = 95 # °C
    t_surroundings = 20 # °C
    k_losses = 3 # W/K
    tes = ThermalEnergyStorage.ThermalEnergyStorage(environment,
                                                    t_init,
                                                    capacity,
                                                    t_max,
                                                    t_surroundings,
                                                    k_losses)

    (tesCapacity, tesTMax, tesTSurroundings, tesKLosses) = tes.getNominalValues()

    # Print results
    print()
    print(("Initial temperature: "      + str(tes.tInit)))
    print(("Water mass: "               + str(tesCapacity)))
    print(("Maximum temperature: "      + str(tesTMax)))
    print(("Surroundings temperature: " + str(tesTSurroundings)))
    print(("Loss factor: "              + str(tesKLosses)))

    np.random.seed(0)
    result = (np.random.rand(timer.timestepsUsedHorizon) * (t_max - t_surroundings)
              + t_surroundings)
    tes.setResults(result)

    print()
    print(("Storage temperature: " + str(tes.getResults(True))))

if __name__ == '__main__':
    #  Run program
    run_test()
