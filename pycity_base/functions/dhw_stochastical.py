#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 12:18:14 2015

@author: tsz
"""

from __future__ import division
import os
import numpy as np
import xlrd
import math
import random
import pycity_base.functions.changeResolution as cr


def load_profiles(filename):
    """
    """
    # Initialization
    profiles = {"we":{}, "wd":{}} 
    book = xlrd.open_workbook(filename)
    
    # Iterate over all sheets    
    for sheetname in book.sheet_names():
        sheet = book.sheet_by_name(sheetname)
        
        # Read values
        values = [sheet.cell_value(i,0) for i in range(1440)]

        # Store values in dictionary
        if sheetname in ("wd_mw", "we_mw"):
            profiles[sheetname] = np.array(values)
        elif sheetname[1] == "e":
            profiles["we"][int(sheetname[2])] = np.array(values)
        else:
            profiles["wd"][int(sheetname[2])] = np.array(values)
    
    # Return results
    return profiles

def compute_daily_demand(probability_profiles, average_profile, occupancy,
                         current_day, temperature_difference=35):
    """
    Parameters
    ----------
    probability_profiles : array_like
        Minute-wise sampled probability distribution.
        "Haushaltewd" and "Haushaltewe" in Lion's thesis.
        This input should also be equivalent to "pwd" and "pwe", because only 
        one household is taken into account.
    average_profile : array_like
        Minute-wise sampled average tap water profiles (in liters per hour).
        "mwwd" and "mwwe" in Lion's thesis.
    occupancy : array_like
        10-Minute-wise sampled occupancy of the considered building/apartment.
    current_day : integer
        Current day of the year (January 1st -> 0, February 1st -> 31, ...)
    temperature_difference : float
        How much does the tap water has to be heated up? Either enter a float
        or an array with the same dimension as probability_profiles.
    
    Returns
    -------
    water : array_like
        Tap water volume flow in liters per hour.
    heat : array_like
        Resulting minute-wise sampled heat demand in Watt.
        The heat capacity of water is assumed to be 4180 J/(kg.K) and the
        density is assumed to be 980 kg/m3
    """
    # Initialization
    water = []
    timesteps = 1440
    time = np.arange(timesteps)
    
    # Compute seasonal factor
    # Introduce abbreviation to stay below 80 characters per line
    arg = math.pi * (2 / 365 * (current_day + time / timesteps) - 1 / 4)
    probability_season = 1 + 0.1 * np.cos(arg)
    
    # Iterate over all time steps
    for t in time:
        # Compute the product of occupancy and probability_profiles
        current_occupancy = occupancy[int(t/10)]
        if current_occupancy > 0:
            probability_profile = probability_profiles[current_occupancy][t]
        else:
            probability_profile = 0
    
        # Compute probability for tap water demand at time t
        probability = probability_profile * probability_season[t]

        # Check if tap water demand occurs at time t
        if random.random() < probability:
            # Compute amount of tap water consumption. This consumption has 
            # to be positive!
            water.append(abs(random.gauss(average_profile[t], sigma=114.33)))
        else:
            water.append(0)

    # Transform to array and compute resulting heat demand
    water = np.array(water) # l/h
    c = 4180                # J/(kg.K)
    rho = 980 / 1000        # kg/l
    sampling_time = 3600    # s
    heat = water * rho * c * temperature_difference / sampling_time  # W
    
    # Return results
    return (water, heat)

def full_year_computation(occupancy, 
                          profiles, 
                          time_dis=3600,
                          initial_day=0, 
                          temperature_difference=35):
    """
    Parameters
    ----------
    occupancy : array_like
        Full year, 10-minute-wise sampled occupancy profile. All values have
        to be integers.
    profiles : dictionary
        All probability distributions. The dictionary has to have the 
        following structure: 
            - Top level: [`wd_mw`, `we_mw`, `wd`, `we`] (strings)
            - Within `we` and `wd`: [`1`, `2`, `3`, `4`, `5`, `6`] (integers)
    time_dis : integer
        Time discretization in seconds.
    initial_day : integer
        - 0 : Monday
        - 1 : Tuesday
        - 2 : Wednesday
        - 3 : Thursday
        - 4 : Friday
        - 5 : Saturday
        - 6 : Sunday
    temperature_difference : float
        How much does the tap water has to be heated up? Either enter a float
        or an array with the same dimension as probability_profiles.
    
    Returns
    -------
    water : array_like
        Tap water volume flow in liters per hour.
    heat : array_like
        Resulting minute-wise sampled heat demand in Watt.
        The heat capacity of water is assumed to be 4180 J/(kg.K) and the
        density is assumed to be 980 kg/m3
    """
    # Initialization
    number_days = int(len(occupancy) / 144)
    
    water = np.zeros(len(occupancy) * 10)
    heat = np.zeros(len(occupancy) * 10)
    
    for day in range(number_days):
        # Is the current day on a weekend?
        if (day + initial_day) % 7 >= 5:
            probability_profiles = profiles["we"]
            average_profile = profiles["we_mw"]
        else:
            probability_profiles = profiles["wd"]
            average_profile = profiles["wd_mw"]
        
        # Get water and heat demand for the current day
        res = compute_daily_demand(probability_profiles, 
                                   average_profile,
                                   occupancy[day*144 : (day+1)*144],
                                   day, 
                                   temperature_difference)
        (current_water, current_heat) = res
        
        # Include current_water and current_heat in water and heat
        water[day*1440 : (day+1)*1440] = current_water
        heat[day*1440 : (day+1)*1440] = current_heat
    
    # Change sampling time to the given input
    water = cr.changeResolution(water, 60, time_dis, "sum") / time_dis * 60
    heat = cr.changeResolution(heat, 60, time_dis, "sum") / time_dis * 60

    # Return results
    return (water, heat)

if __name__ == "__main__":

    #  Define src path
    src_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'dhw_stochastical.xlsx'
    input_path = os.path.join(src_path, 'inputs', filename)

    # Load profiles
    profiles = load_profiles(input_path)
    
    # Compute active occupants for one year
    # Max. occupancy is 5 people simultaneously
    occupancy = np.random.geometric(p=0.8, size=6*24*365)-1
    occupancy = np.minimum(5, occupancy)
    
    # Set initial_day
    initial_day = 0
    
    # Run simulation
    (water, heat) = full_year_computation(occupancy, profiles, 
                                          time_dis=60,
                                          initial_day=initial_day)
    
    # Change time resolution to 15 minutes
    dt = 15
    hd = cr.changeResolution(heat, 60, dt*60, "sum") / dt

    # Plot heat demand
    import matplotlib.pyplot as plt
    ax1=plt.subplot(2,1,1)
    plt.plot(np.arange(len(heat))/60, heat, color="b", linewidth=2)
    plt.step((np.arange(len(hd)) * dt+dt)/60, hd, color="r", linewidth=2)
    plt.ylabel("Heat demand in Watt")
    plt.xlim((0,8760))
    
    plt.subplot(2,1,2, sharex=ax1)
    plt.step((np.arange(len(occupancy)) * 10+10)/60, occupancy, linewidth=2)
    plt.ylabel("Active occupants")
    offset = 0.2
    plt.ylim((-offset, max(occupancy)+offset))
    plt.yticks(list(range(int(max(occupancy)+1))))
    
    plt.show()
    