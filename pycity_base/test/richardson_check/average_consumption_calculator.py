# coding=utf-8
"""
Code to calculate average electrical energy consumption of multiple
apartments with stochastic, electrical load profiles
"""

from __future__ import division

import numpy as np
import timeit

import pycity_base.classes.demand.electrical_demand as ed

import pycity_base.classes.timer
import pycity_base.classes.weather
import pycity_base.classes.environment
import pycity_base.classes.prices

import pycity_base.classes.demand.occupancy


def run_single_calc(number_of_occupants, randomize_appliances, environment,
                    prev_heat_dev=False, app_filename=None,
                    light_filename=None):
    """

    Parameters
    ----------
    number_of_occupants
    randomize_appliances
    environment
    prev_heat_dev : bool, optional
        Defines, if heating devices should be prevented within chosen
        appliances (default: False). If set to True, DESWH, E-INST,
        Electric shower, Storage heaters and Other electric space heating
        are set to zero. Only relevant for method == 2
    app_filename : str, optional
        Path to Appliances file
        (default: None). If set to None, uses default file Appliances.csv
        in \inputs\stochastic_electrical_load\.
        Only relevant, if method == 2.
    light_filename : str, optional
        Path to Lighting configuration file
        (default: None). If set to None, uses default file Appliances.csv
        in \inputs\stochastic_electrical_load\.
        Only relevant, if method == 2.
    """

    occupancy = pycity_base.classes.demand.occupancy.Occupancy(environment,
                                                               number_occupants=number_of_occupants)

    el_load = ed.ElectricalDemand(environment,
                                  method=2,
                                  total_nb_occupants=number_of_occupants,
                                  randomize_appliances=randomize_appliances,
                                  light_configuration=10,
                                  occupancy=occupancy.occupancy,
                                  prev_heat_dev=prev_heat_dev,
                                  app_filename=app_filename,
                                  light_filename=light_filename)

    return el_load


def run_multiple_calc(number_of_occupants, randomize_appliances,
                      nb_of_apartments, prev_heat_dev=False,
                      app_filename=None, light_filename=None):
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
    prev_heat_dev : bool, optional
        Defines, if heating devices should be prevented within chosen
        appliances (default: False). If set to True, DESWH, E-INST,
        Electric shower, Storage heaters and Other electric space heating
        are set to zero. Only relevant for method == 2
    app_filename : str, optional
        Path to Appliances file
        (default: None). If set to None, uses default file Appliances.csv
        in \inputs\stochastic_electrical_load\.
        Only relevant, if method == 2.
    light_filename : str, optional
        Path to Lighting configuration file
        (default: None). If set to None, uses default file Appliances.csv
        in \inputs\stochastic_electrical_load\.
        Only relevant, if method == 2.

    Returns
    -------
    av_el_demand : float
        Average electric energy demand in kWh/a
    """

    timer = pycity_base.classes.timer.Timer(time_discretization=60,
                                            timesteps_total=365*24*60,
                                            initial_day=1)
    weather = pycity_base.classes.weather.Weather(timer)  # , use_TRY=True)
    prices = pycity_base.classes.prices.Prices()

    environment = pycity_base.classes.environment.Environment(timer, weather,
                                                              prices)

    total_el_demand = 0  # Dummy value

    for i in range(nb_of_apartments):
        el_load_object = \
            run_single_calc(number_of_occupants=number_of_occupants,
                            randomize_appliances=randomize_appliances,
                            environment=environment,
                            prev_heat_dev=prev_heat_dev,
                            app_filename=app_filename,
                            light_filename=light_filename)

        #  Convert to demand in kWh
        el_demand_curve = el_load_object.loadcurve * timer.time_discretization \
                          / (3600 * 1000)

        #  Current demand in kWh
        curr_demand = np.sum(el_demand_curve)

        #  Add value to total_el_demand
        total_el_demand += curr_demand

    av_el_demand = total_el_demand / nb_of_apartments

    return av_el_demand


def process_multiple_occupant_numbers(randomize_appliances, nb_of_apartments,
                                      prev_heat_dev=False,
                                      app_filename=None, light_filename=None):
    """

    Parameters
    ----------
    randomize_appliances : bool
        Boolean to define, if appliances should be placed randomly or
        be loaded from csv file
    nb_of_apartments : int
        Total number of apartments for which profiles should be generated
    prev_heat_dev : bool, optional
        Defines, if heating devices should be prevented within chosen
        appliances (default: False). If set to True, DESWH, E-INST,
        Electric shower, Storage heaters and Other electric space heating
        are set to zero. Only relevant for method == 2
    app_filename : str, optional
        Path to Appliances file
        (default: None). If set to None, uses default file Appliances.csv
        in \inputs\stochastic_electrical_load\.
        Only relevant, if method == 2.
    light_filename : str, optional
        Path to Lighting configuration file
        (default: None). If set to None, uses default file Appliances.csv
        in \inputs\stochastic_electrical_load\.
        Only relevant, if method == 2.

    Returns
    -------
    occ_en_dict : dict
    """

    occ_en_dict = {}  # Empty dictionary

    for i in range(1, 6):
        av_el_demand =\
            run_multiple_calc(number_of_occupants=i,
                              randomize_appliances=randomize_appliances,
                              nb_of_apartments=nb_of_apartments,
                              prev_heat_dev=prev_heat_dev,
                              app_filename=app_filename,
                              light_filename=light_filename
                              )

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
    nb_of_apartments = 5
    randomize_appliances = True
    prev_heat_dev = False  # Prevent hot water and space heating el. devices
    app_filename = None
    light_filename = None

    #  Run program
    occ_en_dict = \
        process_multiple_occupant_numbers(
            randomize_appliances=randomize_appliances,
            nb_of_apartments=nb_of_apartments,
            prev_heat_dev=prev_heat_dev,
            app_filename=app_filename,
            light_filename=light_filename)

    print('Occupants - energy dict:')
    print(occ_en_dict)

    print('Randomization of appliances activated?', randomize_appliances)

    stop = timeit.default_timer()

    print('Required runtime in seconds:', stop - start)
