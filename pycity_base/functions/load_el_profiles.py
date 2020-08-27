#!/usr/bin/env python
# coding=utf-8
"""
Script to load el. profiles
"""

import os
import copy
import numpy as np
import matplotlib.pyplot as plt


def load_non_res_load_data_weekly(path):
    """
    Load electrical load profiles for non-residential buildings
    (weekly profiles; Mo - Su)

    Parameters
    ----------
    path : str
        Path to load profile data file

    Returns
    -------
    data_array : np.array
        ND-Array with data
        900 seconds timestep; length for one week;
        starting on monday (00:00:00)
        first column: food production
        second column: metal company
        third column: restaurant (high cooling load)
        fourth column: sports hall
        fifth column: repair / metal shop
    """

    data_array = np.genfromtxt(path, delimiter='\t', skip_header=2, usecols=(3, 4, 5, 6, 7), encoding="utf-8")
    return data_array


def load_non_res_load_data_annual(path):
    """
    Load measured annual electrical load profiles for non-residential buildings

    Parameters
    ----------
    path : str
        Path to file

    Returns
    -------
    data_array : np.array
        ND-Array with data
        900 seconds timestep; length for one year (365 days)
        starting on monday (00:00:00)
        first column: metal 1 (smoother profile)
        second column: metal 2 (more fluctuation)
        third column: warehouse
    """

    data_array = np.genfromtxt(path, delimiter='\t', skip_header=2, usecols=(2, 3, 4), encoding="utf-8")
    return data_array


def gen_annual_el_load(data_array, type, start_wd, annual_demand=None):
    """
    Generate annual el. power curve depending on type and start weekday.
    Based on measured weekly, el. load profiles of non residential buildings.
    Weekly profiles are appended to annual profile. (900 seconds timestep)

    Parameters
    ----------
    data_array : np.array
        ND-Array with data
        (El. power in watt per company over timesteps;
        900 seconds timestep; length for one week;
        starting on monday (00:00:00)
        first column: food production
        second column: metal company
        third column: restaurant (high cooling load)
        fourth column: sports hall
        fifth column: repair / metal shop
    annual_demand : float
        Annual el. energy demand in kWh to rescale profile
    type : str
        Possible types of profiles. Options:
        - 'food_pro': Food production
        - 'metal': Metal company
        - 'rest': Restaurant
        - 'sports': Sports hall
        - 'repair': Repair / metal shop
    start_wd : int
        Integer to define start weekday of year, e.g. 1 means monday, 7 sunday
    annual_demand : float, optional
        Annual el. energy demand in kWh to rescale profile (default: None).
        If set to None, does not perform rescaling.

    Returns
    -------
    el_load_curve : np.array
        Numpy array with el. power curve in Watt
    """

    assert type in ['food_pro', 'metal', 'rest',
                    'sports', 'repair'], 'You need to define a valid type'
    assert start_wd >= 1
    assert start_wd <= 7

    #  Type dictionary; Type as key; column number as value
    dict_type = {'food_pro': 0, 'metal': 1, 'rest': 2, 'sports': 3,
                 'repair': 4}

    #  Weekday dictionary; Weekday int as key; row index as value
    dict_wd = {1: 0, 2: 1 * 24 * 4, 3: 2 * 24 * 4, 4: 3 * 24 * 4,
               5: 4 * 24 * 4, 6: 5 * 24 * 4,
               7: 6 * 24 * 4}

    #  Get column and row index
    column_idx = dict_type[type]
    row_idx = dict_wd[start_wd]

    #  Extract weekly array depending on type
    extr_array = copy.deepcopy(data_array[:, column_idx])

    #  Resort array to start with desired weekday
    start_array = extr_array[row_idx:]
    stop_array = extr_array[:row_idx]

    #  Stack arrays back together
    extr_array = np.append(start_array, stop_array)

    el_load_curve = np.array([])

    #  Append array for 52 weeks
    for i in range(52):
        el_load_curve = np.append(el_load_curve, extr_array)

    # Add missing values to el_load_curve
    el_load_curve = np.append(el_load_curve, extr_array[:96])

    #  Rescale profile
    if annual_demand is not None:
        assert annual_demand > 0, 'Annual el. demand must be larger than 0!'

        #  Convert to energy values in kWh
        energy_curve = el_load_curve * 900 / (3600 * 1000)

        #  Conversion factor
        con_fac = annual_demand / sum(energy_curve)

        el_load_curve *= con_fac

    return el_load_curve


def get_annual_el_load(data_array, type, annual_demand=None):
    """
    Get annual electrical load profile based on measurement data for
    non-residential buildings (900 seconds timestep)

    Parameters
    ----------
    data_array : np.array
        ND-Array with data
        900 seconds timestep; length for one year (365 days)
        starting on monday (00:00:00)
        first column: metal 1 (smoother profile)
        second column: metal 2 (more fluctuation)
        third column: warehouse
    type : str
        Type of chosen measured profile. Options:
        - 'metal_1' : Metal company with smooth profile
        - 'metal_2' : Metal company with fluctuation in profile
        - 'warehouse' : Warehouse
    annual_demand : float, optional
        Annual el. energy demand in kWh to rescale profile (default: None).
        If set to None, does not perform rescaling.

    Returns
    -------
    el_load_curve : np.array
        Numpy array with el. power curve in Watt
    """

    assert type in ['metal_1', 'metal_2', 'warehouse'], 'You need to define a valid type'

    #  Type dictionary; Type as key; column number as value
    dict_type = {'metal_1': 0, 'metal_2': 1, 'warehouse': 2}

    #  Get column index
    column_idx = dict_type[type]

    #  Extract weekly array depending on type
    el_load_curve = copy.deepcopy(data_array[:, column_idx])

    #  Rescale profile
    if annual_demand is not None:
        assert annual_demand > 0, 'Annual el. demand must be larger than 0!'

        #  Convert to energy values in kWh
        energy_curve = el_load_curve * 900 / (3600 * 1000)

        #  Conversion factor
        con_fac = annual_demand / sum(energy_curve)

        el_load_curve *= con_fac

    return el_load_curve


if __name__ == '__main__':
    #  User inputs
    #  #------------------------------------------------------------------
    #  Define filename
    filename = 'Non_res_weekly_el_profiles.txt'

    #  Define path to file
    this_path = os.path.dirname(os.path.abspath(__file__))
    pycity_path = os.path.dirname(this_path)
    input_path = os.path.join(pycity_path, 'inputs', 'measured_el_loads',
                              filename)

    #  Chosen type of non-residential
    type = 'metal'

    #  start weekday
    start_wd = 3  # 1 - Monday; 7 - Sunday

    #  Annual el. demand in kWh
    ann_demand = 4000

    #  #------------------------------------------------------------------

    #  Load weekly el. load profile data
    data_array = load_non_res_load_data_weekly(input_path)

    #  Generate el. load profile based on measurement data
    el_load_curve = gen_annual_el_load(data_array, type, start_wd,
                                       annual_demand=ann_demand)

    print('Electrical load profile:')
    print(el_load_curve)

    print('Energy demand in kWh:')
    print(sum(el_load_curve) * 900 / (3600 * 1000))

    plt.plot(el_load_curve[:672])
    plt.show()
