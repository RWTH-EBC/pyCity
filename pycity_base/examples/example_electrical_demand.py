#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example of the electrical demand class.
"""

from __future__ import division

import matplotlib.pyplot as plt

import pycity_base.classes.demand.electrical_demand as ed
import pycity_base.classes.timer
import pycity_base.classes.weather
import pycity_base.classes.environment
import pycity_base.classes.prices
import pycity_base.classes.demand.occupancy


def run_example(do_plot=False, run_stoch=False):

    print('Generate slp profile')
    print('########################################################')

    timer = pycity_base.classes.timer.Timer()
    weather = pycity_base.classes.weather.Weather(timer)  # , use_TRY=True)
    prices = pycity_base.classes.prices.Prices()

    environment = pycity_base.classes.environment.Environment(timer, weather,
                                                              prices)

    el_demand = ed.ElectricalDemand(environment,
                                    method=1,  # Standard load profile
                                    profile_type="H0",
                                    annual_demand=3000)

    results = el_demand.loadcurve

    #  Convert to energy_curve in kWh
    energy_curve = results * timer.time_discretization / (3600 * 1000)

    energy_value = sum(energy_curve)

    print()
    print("Electrical power in W: " + str(results))

    print('Sum of consumed energy in kWh: ', energy_value)

    if do_plot:
        plt.plot(results[:672])
        plt.show()

    if run_stoch:

        print()
        print('Generate stochastic, el. profile')
        print('########################################################')

        occupancy = pycity_base.classes.demand.occupancy.Occupancy(environment,
                                                                   number_occupants=3)

        el_dem_stochastic = ed.ElectricalDemand(environment,
                                                method=2,
                                                total_nb_occupants=3,
                                                randomize_appliances=True,
                                                light_configuration=10,
                                                occupancy=occupancy.occupancy,
                                                prev_heat_dev=True)

        results2 = el_dem_stochastic.loadcurve

        #  Convert to energy_curve in kWh
        energy_curve2 = results2 * timer.time_discretization / (3600 * 1000)

        energy_value2 = sum(energy_curve2)

        print()
        print("Electrical power in W: " + str(results))

        print('Sum of consumed energy in kWh: ', energy_value2)

        if do_plot:
            plt.plot(results2[:672])
            plt.show()

        print()
        print('Generate normalized stochastic profile')
        print('########################################################')

        energy_input = 3000

        el_dem_stochastic2 = ed.ElectricalDemand(environment,
                                                 method=2,
                                                 annual_demand=energy_input,
                                                 total_nb_occupants=3,
                                                 randomize_appliances=True,
                                                 light_configuration=10,
                                                 occupancy=occupancy.occupancy,
                                                 do_normalization=True)

        results3 = el_dem_stochastic2.loadcurve

        #  Convert to energy_curve in kWh
        energy_curve3 = results3 * timer.time_discretization / (3600 * 1000)

        energy_value3 = sum(energy_curve3)

        print()
        print("Electrical power in W: " + str(results3))

        print('Sum of consumed energy in kWh: ', energy_value3)
        assert energy_input - energy_value3 <= 0.001 * energy_input

        if do_plot:
            plt.plot(results3[:672])
            plt.show()

    print('Generate el. profile based on weekly measurement data')
    print('########################################################')

    el_demand = ed.ElectricalDemand(environment,
                                    method=3,  # Weekly profile
                                    do_normalization=True,
                                    annual_demand=3000,
                                    method_3_type='metal')

    results4 = el_demand.loadcurve

    #  Convert to energy_curve in kWh
    energy_curve4 = results4 * timer.time_discretization / (3600 * 1000)

    energy_value4 = sum(energy_curve4)

    print()
    print("Electrical power in W: " + str(results4))

    print('Sum of consumed energy in kWh: ', energy_value4)

    if do_plot:
        plt.plot(results4[:672])
        plt.show()

    print('Generate el. profile based on annual measurement data')
    print('########################################################')

    el_demand = ed.ElectricalDemand(environment,
                                    method=4,  # Annual measurement profiles
                                    do_normalization=True,
                                    annual_demand=5000,
                                    method_4_type='metal_2')

    results5 = el_demand.loadcurve

    #  Convert to energy_curve in kWh
    energy_curve5 = results5 * timer.time_discretization / (3600 * 1000)

    energy_value5 = sum(energy_curve5)

    print()
    print("Electrical power in W: " + str(results5))

    print('Sum of consumed energy in kWh: ', energy_value5)

    if do_plot:
        plt.plot(results5[:672])
        plt.show()

        plt.plot(results5)
        plt.show()


if __name__ == '__main__':
    #  Run program
    run_example(do_plot=True, run_stoch=True)
