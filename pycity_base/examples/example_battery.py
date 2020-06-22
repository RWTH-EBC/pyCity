#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example of the battery class.
"""

from __future__ import division

import numpy as np

import pycity_base.classes.supply.battery as bat
import pycity_base.classes.timer
import pycity_base.classes.weather
import pycity_base.classes.prices
import pycity_base.classes.environment


def run_example():

    # Create environment
    timer = pycity_base.classes.timer.Timer()
    weather = pycity_base.classes.weather.Weather(timer)
    prices = pycity_base.classes.prices.Prices()
    environment = pycity_base.classes.environment.Environment(timer, weather, prices)

    # Create Boiler
    capacity = 4 * 3600 * 1000 # 4 kWh = 4 * 3600*1000 J
    soc_init = 0.5 * capacity
    self_discharge = 0.02
    eta_charge = 0.96
    eta_discharge = 0.95
    battery = bat.Battery(environment, soc_init, capacity, self_discharge, eta_charge, eta_discharge)

    # Print results
    print()
    print(("Initial state of charge: " + str(battery.soc_init)))
    print(("Rate of self discharge: " + str(battery.self_discharge)))
    print(("Efficiency at discharging: " + str(battery.eta_discharge)))
    print(("Efficiency at charging: " + str(battery.eta_charge)))
    print(("Battery's total capacity: " + str(battery.capacity)))

    print()
    print(("Nominals: " + str(battery.getNominalValues())))

    np.random.seed(0)
    soc = np.random.rand(timer.timesteps_used_horizon)
    charge = np.random.rand(timer.timesteps_used_horizon) * capacity / 3600.0
    discharge = np.random.rand(timer.timesteps_used_horizon) * capacity / 3600.0
    battery.setResults(soc, charge, discharge)

    results = battery.getResults(True)
    print()
    print(("SOC: " + str(results[0])))
    print()
    print(("Charging power: " + str(results[1])))
    print()
    print(("Disharging power: " + str(results[2])))


if __name__ == '__main__':
    #  Run program
    run_example()
