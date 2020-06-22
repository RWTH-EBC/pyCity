#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example of the thermal energy storage (TES) class.
"""

from __future__ import division

import numpy as np
import pycity_base.classes.supply.thermal_energy_storage as tes

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

    # Create heating device
    t_init = 20  # °C
    capacity = 1000  # kg
    t_max = 95  # °C
    t_surroundings = 20  # °C
    k_losses = 3  # W/K
    thermal_storage = tes.ThermalEnergyStorage(environment,
                                               t_init,
                                               capacity,
                                               t_max,
                                               t_surroundings,
                                               k_losses)

    (tes_capacity, tes_t_max, tes_t_surroundings, tes_k_losses) = thermal_storage.getNominalValues()

    # Print results
    print()
    print(("Initial temperature: " + str(thermal_storage.t_init)))
    print(("Water mass: " + str(tes_capacity)))
    print(("Maximum temperature: " + str(tes_t_max)))
    print(("Surroundings temperature: " + str(tes_t_surroundings)))
    print(("Loss factor: " + str(tes_k_losses)))

    np.random.seed(0)
    result = (np.random.rand(timer.timesteps_used_horizon) * (t_max - t_surroundings) + t_surroundings)
    thermal_storage.setResults(result)

    print()
    print(("Storage temperature: " + str(thermal_storage.getResults(True))))


if __name__ == '__main__':
    #  Run program
    run_example()
