#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 16:44:44 2015

@author: tsz
"""

from __future__ import division
import numpy as np
import math
import xlrd
import functions.changeResolution as cr


# Sources:
# [1] BDEW/VKU/GEODE-Leitfaden. Abwicklung von Standardlastprofilen Gas (2014)
#     https://www.bdew.de/internet.nsf/id/33EEC2362FA39C3AC1257D04004ED1C2/$file/14-06-30_KOV%20VII_LF_Abwicklung_von_SLP_Gas.pdf

def calculate(temperature, initial_day, profiles, weekly_factors, 
              hourly_factors, total_demand):
    """
    Parameters
    ----------
    temperature : array_like
        Full year temperature profile with hourly discretization.
    initial_day : integer
        - 0 : Monday
        - 1 : Tuesday
        - 2 : Wednesday
        - 3 : Thursday
        - 4 : Friday
        - 5 : Saturday
        - 6 : Sunday
    profiles : array_like
        Dictionary containing all profile factors (A, B, C, D) for all types
        of houses.
        Index order: 0 - A, 1 - B, 2 - C, 3 - D
    weekly_factors : array_like
        Week day modifiers for each day. Indexes correspond to the description
        of initial_day (0 - Monday, ..., 6 - Sunday)
    hourly_factors : dictionary
        Dictionary containing all hourly profile factors for types of houses.
        First dimension holds the day of the week (see ``initial_day``), the
        second dimension holds the temperature range 
        (-15; -10; -5; 0; 5; 10; 15; 20; 25; else). The values at this level 
        are arrays containing the factors for one day, starting with the
        time interval from 00:00 until 01:00.
    house_type : string
        - `HEF` : Single family household
        - `HMF` : Multi family household
        - `GBA` : Bakeries
        - `GBD` : Other services
        - `GBH` : Accomodations
        - `GGA` : Restaurants
        - `GGB` : Gardening
        - `GHA` : Retailers
        - `GHD` : Summed load profile business, trade and services
        - `GKO` : Banks, insurances, public institutions
        - `GMF` : Household similar businesses
        - `GMK` : Automotive
        - `GPD` : Paper and printing
        - `GWA` : Laundries
    total_demand : float
        Total yearly demand in kWh
    """
    # Compute average daily temperatures. [1], page 17, section 3.5.2
    timesteps_day = len(hourly_factors[list(hourly_factors.keys())[0]])
    t_average = _average_temperature(temperature, timesteps_day)

    # Compute h-factors. [1], page 38
    theta_0 = 40 # [1], page 38
    A = profiles[0]
    B = profiles[1]
    C = profiles[2]
    D = profiles[3]
    
    h = np.array([D + A / ((B / (t - theta_0))**C + 1) for t in t_average])
    
    # Compute weekday factors
    F_factors = np.tile(weekly_factors, math.ceil(len(t_average) / 7))
    F = F_factors[initial_day : initial_day+ len(t_average)]
    
    # Compute customer's value. [1], page 78
    KW = total_demand / np.sum(h * F)
    
    # Compute daily load profiles
    result = _daily_profiles(t_average, KW, h, F, hourly_factors, initial_day)
    
    # Transform to W instead of kWh
    time_discretization = 86400 / timesteps_day
    return result * 1000 * 3600 / time_discretization


def _average_temperature(temperature, timesteps_day=24):
    """
    """
    t_ambient_average = []
    t = 0
    day = 0
    while t+timesteps_day <= len(temperature):
        if day < 3:
            t_ambient_average.append(np.mean(temperature[t : t+timesteps_day]))
        else:
            t_prev = np.zeros(4)
            for d in range(4):
                index_from = t-d*timesteps_day
                index_to = t-(d-1)*timesteps_day
                t_prev[d] = np.mean(temperature[index_from : index_to])
            
            weights = np.array([1.0 / 2**(i) for i in range(4)])
            
            t_ambient_average.append(np.dot(weights, t_prev) / np.sum(weights))
        
        t += timesteps_day
        day += 1
    
    return t_ambient_average

        
def _daily_profiles(temperatures, KW, h, F, hourly_factors, initial_day):
    """
    temperatures : array_like
        Average ambient temperatures for each day
    KW : float
        Customer demand in kWh per day
    hourly_factors : dictionary
        Dictionary containing all hourly profile factors for types of houses.
        First dimension holds the day of the week (see ``initial_day``), the
        second dimension holds the temperature range 
        (-15, -10, -5, 0, 5, 10, 15, 20, 25, else). The values at this level 
        are arrays containing the factors for one day, starting with the
        time interval from 00:00 until 01:00.
    initial_day : integer
        - 0 : Monday
        - 1 : Tuesday
        - 2 : Wednesday
        - 3 : Thursday
        - 4 : Friday
        - 5 : Saturday
        - 6 : Sunday
    """
    # Initialization
    result = []
    temperature_range = [-15, -10, -5, 0, 5, 10, 15, 20, 25, 100]
    
    for day in range(len(temperatures)):
        # Get the relative day (Monday, Tuesday... Sunday)
        relative_day = (initial_day + day) % 7
        
        # Get the appropriate temperature interval
        for tr in temperature_range:
            if temperatures[day] <= tr:
                break
        
        # Get hourly profile 
        profile = hourly_factors[relative_day, tr]
        
        # Compute thermal demand profile
        result.append(profile * KW * h[day] * F[day])
    
    # Transform result into 1-d array
    return np.reshape(result, -1)

def load_week_day_factors(filename):
    """
    """
    # Initialization
    profiles = {} 
    book_weekday = xlrd.open_workbook(filename)
    
    # Iterate over all sheets    
    for sheetname in book_weekday.sheet_names():
        sheet = book_weekday.sheet_by_name(sheetname)
        
        # Read values
        values = [sheet.cell_value(1,d) for d in range(7)]

        # Store values in dictionary
        profiles[sheetname] = np.array(values)
    
    # Return results
    return profiles
    
def load_hourly_factors(filename, time_discretization=3600):
    """
    """
    # Initialization
    hourly_factors = {}
    temperature_range = [-15, -10, -5, 0, 5, 10, 15, 20, 25, 100]
    book_hourly = xlrd.open_workbook(filename)
    
    # Iterate over all sheets
    for sheetname in book_hourly.sheet_names():
        sheet = book_hourly.sheet_by_name(sheetname)
        
        temp_factors = {} # Create temporary dictionary for each sheet
        for d in range(7):
            for t in range(len(temperature_range)):
                # Read values
                values = [sheet.cell_value(d*11+t+1, hour+1) 
                          for hour in range(24)]
                if time_discretization != 3600:
                    values = cr.changeResolution(values, 3600, 
                                                 time_discretization, "sum")
                temp_factors[d, temperature_range[t]] = np.array(values)
        
        # Store values
        hourly_factors[sheetname] = temp_factors
    
    # Return final results
    return hourly_factors
    
def load_profile_factors(filename):
    """
    """
    # Initialization
    profile_factors = {}
    book_profiles = xlrd.open_workbook(filename)
    
    # Iterate over all sheets
    for sheetname in book_profiles.sheet_names():
        sheet = book_profiles.sheet_by_name(sheetname)
        
        temp_factors = {} # Create temporary dictionary for each sheet
        for demand in range(5): # Iterate over all demand types (1-5)
            # Read values. 
            # Note: Demand types are stored in the wrong order (5-1)
            # Note: Letters: 0 - A, 1 - B, 2 - C, 3 - D
            values = [sheet.cell_value(5-demand, letter+1) 
                    for letter in range(4)]
            
            temp_factors[demand+1] = np.array(values)
        
        # Store values
        profile_factors[sheetname] = temp_factors
    
    # Return final results
    return profile_factors
    
# Test script
if __name__ == "__main__":
    # Load temperatures
    f_TRY = "inputs/weather/TRY2010_05_Jahr.dat"
    temperature = np.loadtxt(f_TRY, skiprows=38, usecols=(8,))

    # Set initial day
    initial_day = 0
    
    # Load hourly_factors, profile_factors and week_day_factors
    f_hour = "inputs/standard_load_profile/slp_thermal_hourly_factors.xlsx"
    f_prof = "inputs/standard_load_profile/slp_thermal_profile_factors.xlsx"
    f_week = "inputs/standard_load_profile/slp_thermal_week_day_factors.xlsx"
    hourly_factors = load_hourly_factors(f_hour)
    profile_factors = load_profile_factors(f_prof)
    week_day_factors = load_week_day_factors(f_week)
    
    # Exemplary building
    annual_demand = 20000 # kWh
    profile_type = "HEF" # Single family dwelling
    profile = 3
    
    result = calculate(temperature,
                       initial_day,
                       profile_factors[profile_type][profile],
                       week_day_factors[profile_type],
                       hourly_factors[profile_type],
                       annual_demand)
