#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 08:43:12 2015
"""

from __future__ import division
import pycity.classes.demand.ElectricalDemand as ED

import pycity.classes.Timer
import pycity.classes.Weather
import pycity.classes.Environment
import pycity.classes.Prices

import pycity.classes.demand.Occupancy


def run_test():

    print('Generate slp profile')
    print('########################################################')

    timer = pycity.classes.Timer.Timer()
    weather = pycity.classes.Weather.Weather(timer)  # , useTRY=True)
    prices = pycity.classes.Prices.Prices()

    environment = pycity.classes.Environment.Environment(timer, weather,
                                                         prices)

    el_demand = ED.ElectricalDemand(environment,
                                    method=1,  # Standard load profile
                                    profileType="H0",
                                    annualDemand=3000)

    results = el_demand.loadcurve

    #  Convert to energy_curve in kWh
    energy_curve = results * timer.timeDiscretization / (3600 * 1000)

    energy_value = sum(energy_curve)

    print()
    print("Electrical power in W: " + str(results))

    print('Sum of consumed energy in kWh: ', energy_value)

    print()
    print('Generate stochastic, el. profile')
    print('########################################################')

    occupancy = pycity.classes.demand.Occupancy.Occupancy(environment,
                                                          number_occupants=3)

    el_dem_stochastic = ED.ElectricalDemand(environment,
                                            method=2,
                                            total_nb_occupants=3,
                                            randomizeAppliances=True,
                                            lightConfiguration=10,
                                            occupancy=occupancy.occupancy)

    results2 = el_dem_stochastic.loadcurve

    #  Convert to energy_curve in kWh
    energy_curve2 = results2 * timer.timeDiscretization / (3600 * 1000)

    energy_value2 = sum(energy_curve2)

    print()
    print("Electrical power in W: " + str(results))

    print('Sum of consumed energy in kWh: ', energy_value2)

    print()
    print('Generate normalized stochastic profile')
    print('########################################################')

    energy_input = 3000

    el_dem_stochastic2 = ED.ElectricalDemand(environment,
                                             method=2,
                                             annualDemand=energy_input,
                                             total_nb_occupants=3,
                                             randomizeAppliances=True,
                                             lightConfiguration=10,
                                             occupancy=occupancy.occupancy,
                                             do_normalization=True)

    results3 = el_dem_stochastic2.loadcurve

    #  Convert to energy_curve in kWh
    energy_curve3 = results3 * timer.timeDiscretization / (3600 * 1000)

    energy_value3 = sum(energy_curve3)

    print()
    print("Electrical power in W: " + str(results3))

    print('Sum of consumed energy in kWh: ', energy_value3)
    assert energy_input - energy_value3 <= 0.001 * energy_input


if __name__ == '__main__':
    #  Run program
    run_test()
