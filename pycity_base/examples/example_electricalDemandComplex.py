#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 08:43:12 2015
"""

from __future__ import division
import matplotlib.pyplot as plt
import numpy as np

import pycity_base.classes.demand.ElectricalDemandComplex as ED
import pycity_base.classes.Timer
import pycity_base.classes.Weather
import pycity_base.classes.Environment
import pycity_base.classes.Prices
import pycity_base.classes.demand.Occupancy


def run_test(do_plot=False, run_stoch=False):

    print('Generate slp profile')
    print('########################################################')

    timer = pycity_base.classes.Timer.Timer()
    weather = pycity_base.classes.Weather.Weather(timer)  # , useTRY=True)
    prices = pycity_base.classes.Prices.Prices()

    environment = pycity_base.classes.Environment.Environment(timer, weather,
                                                          prices)

    el_demand = ED.ElectricalDemandComplex(environment,
                                    method=1,  # Standard load profile
                                    profileType="H0",
                                    annualDemand=3000)

    results = el_demand.loadcurve
    results_q = el_demand.loadcurve_q

    #  Convert to energy_curve in kWh
    energy_curve = results * timer.timeDiscretization / (3600 * 1000)

    energy_value = sum(energy_curve)

    print()
    print("Electrical power in W: " + str(results))

    print('Sum of consumed energy in kWh: ', energy_value)

    if do_plot:
        plt.plot(results[:672], label='El. load P')
        plt.plot(results_q[:672], label='El. load Q')
        plt.legend()
        plt.show()

    if run_stoch:

        print()
        print('Generate stochastic, el. profile')
        print('########################################################')

        occupancy = pycity_base.classes.demand.Occupancy.Occupancy(environment,
                                                              number_occupants=3)

        el_dem_stochastic = ED.ElectricalDemandComplex(environment,
                                                method=2,
                                                total_nb_occupants=3,
                                                randomizeAppliances=True,
                                                lightConfiguration=0,
                                                occupancy=occupancy.occupancy,
                                                prev_heat_dev=True, reactive_power=True)

        results2 = el_dem_stochastic.loadcurve
        results2_q = el_dem_stochastic.loadcurve_q

        #  Convert to energy_curve in kWh
        energy_curve2 = results2 * timer.timeDiscretization / (3600 * 1000)

        energy_value2 = sum(energy_curve2)

        print()
        print("Electrical power in W: " + str(results2))

        print('Sum of consumed energy in kWh: ', energy_value2)

        if do_plot:
            plt.plot(results2[:672], label='El. load P')
            plt.plot(results2_q[:672], label='El. load Q')
            plt.legend()
            plt.show()

        print()
        print('Generate normalized stochastic profile')
        print('########################################################')

        energy_input = 3000

        el_dem_stochastic2 = ED.ElectricalDemandComplex(environment,
                                                 method=2,
                                                 annualDemand=energy_input,
                                                 total_nb_occupants=3,
                                                 randomizeAppliances=True,
                                                 lightConfiguration=10,
                                                 occupancy=occupancy.occupancy,
                                                 do_normalization=True, reactive_power=True)

        results3 = el_dem_stochastic2.loadcurve
        results3q = el_dem_stochastic2.loadcurve_q

        #  Convert to energy_curve in kWh
        energy_curve3 = results3 * timer.timeDiscretization / (3600 * 1000)

        energy_value3 = sum(energy_curve3)

        print()
        print("Electrical power in W: " + str(results3))

        print('Sum of consumed energy in kWh: ', energy_value3)
        assert energy_input - energy_value3 <= 0.001 * energy_input

        if do_plot:
            plt.plot(results3[:672], label='El. load P')
            plt.plot(results3q[:672], label='El. load Q')
            plt.legend()
            plt.show()

    print()
    print('Reading el. profile')
    print('########################################################')

    # generate a random loadcurve for active and reactive power
    profile_p = np.random.randn(35040)
    profile_q = profile_p*0.74

    el_dem_read = ED.ElectricalDemandComplex(environment,
                                                    method=0, loadcurve=profile_p, loadcurve_q=profile_q,
                                             reactive_power=True)

    results0_p = el_dem_read.loadcurve
    results0_q = el_dem_read.loadcurve_q

    if do_plot:
        plt.plot(results0_p[:672], label='El. load P')
        plt.plot(results0_q[:672], label='El. load Q')
        plt.legend()
        plt.show()

    print('Generate el. profile based on weekly measurement data')
    print('########################################################')

    el_demand = ED.ElectricalDemandComplex(environment,
                                    method=3,  # Weekly profile
                                    do_normalization=True,
                                    annualDemand=3000,
                                    method_3_type='metal')

    results4 = el_demand.loadcurve
    results4_q = el_demand.loadcurve_q

    #  Convert to energy_curve in kWh
    energy_curve4 = results4 * timer.timeDiscretization / (3600 * 1000)

    energy_value4 = sum(energy_curve4)

    print()
    print("Electrical power in W: " + str(results4))

    print('Sum of consumed energy in kWh: ', energy_value4)

    if do_plot:
        plt.plot(results4[:672], label='El. load P')
        plt.plot(results4_q[:672], label='El. load Q')
        plt.legend()
        plt.show()

    print('Generate el. profile based on annual measurement data')
    print('########################################################')

    el_demand = ED.ElectricalDemandComplex(environment,
                                    method=4,  # Annual measurement profiles
                                    do_normalization=True,
                                    annualDemand=5000,
                                    method_4_type='metal_2')

    results5 = el_demand.loadcurve
    results5_q = el_demand.loadcurve_q

    #  Convert to energy_curve in kWh
    energy_curve5 = results5 * timer.timeDiscretization / (3600 * 1000)

    energy_value5 = sum(energy_curve5)

    print()
    print("Electrical power in W: " + str(results5))

    print('Sum of consumed energy in kWh: ', energy_value5)

    if do_plot:
        plt.plot(results5[:672], label='El. load P')
        plt.plot(results5_q[:672], label='El. load Q')
        plt.legend()
        plt.show()

        plt.plot(results5)
        plt.show()

if __name__ == '__main__':
    #  Run program
    run_test(do_plot=True, run_stoch=True)
