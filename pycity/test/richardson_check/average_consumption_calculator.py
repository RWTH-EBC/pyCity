# coding=utf-8
"""
Code to calculate average electrical energy consumption of multiple
apartments with stochastic, electrical load profiles
"""

from __future__ import division
import numpy as np
import timeit

import pycity.classes.demand.ElectricalDemand as ED

import pycity.classes.Timer
import pycity.classes.Weather
import pycity.classes.Environment
import pycity.classes.Prices

import pycity.classes.demand.Occupancy


def run_single_calc(number_of_occupants, randomize_appliances, environment):

    occupancy = pycity.classes.demand.Occupancy.Occupancy(environment,
                                        number_occupants=number_of_occupants)

    el_load = ED.ElectricalDemand(environment,
                                    method=2,
                                    total_nb_occupants=number_of_occupants,
                                    randomizeAppliances=randomize_appliances,
                                    lightConfiguration=10,
                                    occupancy=occupancy.occupancy)

    return el_load

def run_multiple_calc(number_of_occupants, randomize_appliances, nb_of_apartments):
    """
    Returns average, electrical consumption for multiple apartments.

    Parameters
    ----------
    number_of_occupants : int
        Number of occupants (per apartment)
    randomize_appliances : bool
        Boolean to define, if appliances should be placed randomly or
        be loaded from csv file
    nb_of_apartments : int
        Total number of apartments for which profiles should be generated

    Returns
    -------
    av_el_demand : float
        Average electric energy demand in kWh/a
    """

    timer = pycity.classes.Timer.Timer(timeDiscretization=60,
                                       timestepsTotal=365*24*60,
                                       initialDay=1)
    weather = pycity.classes.Weather.Weather(timer)  # , useTRY=True)
    prices = pycity.classes.Prices.Prices()

    environment = pycity.classes.Environment.Environment(timer, weather,
                                                         prices)

    total_el_demand = 0  # Dummy value

    for i in range(nb_of_apartments):
        el_load_object = run_single_calc(number_of_occupants,
                                         randomize_appliances, environment)

        #  Convert to demand in kWh
        el_demand_curve = el_load_object.loadcurve * timer.timeDiscretization \
                          / (3600 * 1000)

        #  Current demand in kWh
        curr_demand = np.sum(el_demand_curve)

        #  Add value to total_el_demand
        total_el_demand += curr_demand

    av_el_demand = total_el_demand / nb_of_apartments

    return av_el_demand

def process_multiple_occupant_numbers(randomize_appliances, nb_of_apartments):

    occ_en_dict = {}  # Empty dictionary

    for i in range(1, 6):
        av_el_demand = run_multiple_calc(number_of_occupants=i,
                          randomize_appliances=randomize_appliances,
                          nb_of_apartments=nb_of_apartments)

        print('Number of occupants:')
        print(i)

        print('Average electrical energy demand:')
        print(av_el_demand)

        #  Add value to dict (key: number of occupants)
        occ_en_dict[i] = av_el_demand

    return occ_en_dict

if __name__ == '__main__':
    start = timeit.default_timer()

    #  User inputs
    nb_of_apartments = 100
    randomize_appliances = True

    #  Run program
    occ_en_dict = process_multiple_occupant_numbers(randomize_appliances,
                                                     nb_of_apartments)

    print('Occupants - energy dict:')
    print(occ_en_dict)

    print('Randomization of appliances activated?', randomize_appliances)

    stop = timeit.default_timer()

    print('Required runtime in seconds:', stop - start)
