#!/usr/bin/env python
# coding=utf-8
"""
Script to generate profile pool for parametrization of large number of
buildings with (stochastic) profiles (occupancy, electrical, dhw)

npz internal arrays should hold name labels:
- occ (600 second resolution)
- el (60 second resolution)
- dhw (60 second resolution)
"""

import os
import numpy as np

import pycity_base.classes.timer
import pycity_base.classes.weather
import pycity_base.classes.prices
import pycity_base.classes.environment
import pycity_base.classes.demand.occupancy as occ
import pycity_base.classes.demand.domestic_hot_water as dhw
import pycity_base.classes.demand.electrical_demand as ed


def create_path_if_not_exist(path):
    """
    Create path if not existent.

    Parameters
    ----------
    path : str
        Input path
    """
    if not os.path.exists(path):
        os.makedirs(path)


def generate_profile_pool(path=None, runs=100, timestep=60):
    """
    Generates profile pool in subfolder profile (if no profile pool exists)
    (occupancy, electrical, dhw)

    Parameters
    ----------
    path : str, optional
        Path to save profile pool to (default: None).
        If set to None, uses subfolder .../profiles/ to store profiles to
    runs : int, optional
        Number of loops used to generate profile pool (default: 100)
    timestep : int, optional
        Time discretization for environment in seconds (default: 60)
    """

    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(path, 'profiles')
    else:  # path is given by user
        #  Create path, if not existent
        create_path_if_not_exist(path)

    timesteps_total = 365 * 24 * 3600 / timestep

    #  Generate environment
    timer = pycity_base.classes.timer.Timer(time_discretization=timestep,
                                            timesteps_total=timesteps_total)
    weather = pycity_base.classes.weather.Weather(timer, use_TRY=True)
    prices = pycity_base.classes.prices.Prices()
    env = pycity_base.classes.environment.Environment(timer, weather, prices)

    for occ_index in range(1, 6):  # Loop from 1 to 5 occupants

        print('Number of occupants: ', occ_index)
        print('#####################################################')

        #  Filenames (Files are going to store 3 arrays ('occ', 'app', 'lig'))
        file_name = str(occ_index) + '_person_profiles.npz'
        path_profile_file = os.path.join(path, file_name)

        occupancy_profiles = None
        el_profiles = None
        dhw_profiles = None

        for i in range(runs):  # Loop over desired number of profiles

            print('Run number: ', i)

            #  Generate occupancy object
            occupancy = occ.Occupancy(environment=env, number_occupants=occ_index)

            #  Get profile
            occ_profile = occupancy.occupancy

            if occupancy_profiles is None:
                occupancy_profiles = occ_profile
            else:
                occupancy_profiles = np.vstack(
                    (occupancy_profiles, occ_profile))

            # Generate el. load profile
            el_dem_stochastic = \
                ed.ElectricalDemand(environment=env,
                                    method=2,
                                    total_nb_occupants=occ_index,
                                    randomize_appliances=True,
                                    light_configuration=10,
                                    occupancy=occupancy.occupancy)

            #  Get el. load profile
            el_profile = el_dem_stochastic.loadcurve

            if el_profiles is None:
                el_profiles = el_profile
            else:
                el_profiles = np.vstack((el_profiles, el_profile))

            # Generate hot water profile
            dhw_stochastical = \
                dhw.DomesticHotWater(environment=env,
                                     t_flow=60,
                                     thermal=True,
                                     method=2,
                                     supply_temperature=20,
                                     occupancy=occ_profile)

            #  Get dhw curve
            dhw_profile = dhw_stochastical.loadcurve

            if dhw_profiles is None:
                dhw_profiles = dhw_profile
            else:
                dhw_profiles = np.vstack((dhw_profiles, dhw_profile))

        # Save as npz file (3 arrays ('occ', 'el', 'dhw'))
        np.savez(path_profile_file, occ=occupancy_profiles,
                 el=el_profiles, dhw=dhw_profiles)
        print('#####################################################')
        print()


if __name__ == '__main__':
    #  Number of loop runs, which should be used to generate individual
    #  profiles
    runs = 100

    #  Run profile pool generator
    generate_profile_pool(runs=runs)
