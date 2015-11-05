#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 11 11:00:03 2015

@author: tsz
"""

import pandas as pd
import numpy as np
import math
from __future__ import division


def changeResolutionPD(values, oldResolution, newResolution, method="mean"):
    """
    Change the temporal resolution of values that have a constant sampling rate
    
    Parameters
    ----------
    values : array-like
        data points
    oldResolution : integer
        temporal resolution of the given values. oldResolution=3600 means
        hourly sampled data
    newResolution : integer
        temporal resolution of the given data shall be converted to
    method : ``{"mean"; "sum"}``, optional
        - ``"mean"`` : compute mean values while resampling (e.g. for power).
        - ``"sum"``  : compute sum values while resampling (e.g. for energy).
    """
    # Compute time indexes
    timeIndex = pd.date_range(0, periods=len(values), 
                              freq=str(oldResolution)+"s")

    # Construct original time series
    timeseriesOld = pd.Series(data=values, index=timeIndex)
    
    # Resample
    # When using "mean" for a timeseries that does not have sufficient entries 
    # (e.g. hourly data should be resampled on a daily scheme, but there are 
    # only 40 instead of 48 data points available), the final time period was 
    # averaged by the available data (16 instead of 24 hours).
    # Using "sum" and dividing/multiplying by the resolution worked fine.
    timeseriesNew = timeseriesOld.resample(rule=str(newResolution)+"s", 
                                           how="sum", fill_method="pad")
    if method == "mean" and newResolution > oldResolution:
        timeseriesNew = timeseriesNew * oldResolution / newResolution

    elif method == "sum" and newResolution < oldResolution:
        pass

    # Get resampled values
    valuesResampled = timeseriesNew.get_values()
    
    return valuesResampled
    
def changeResolution(values, oldResolution, newResolution, method="mean"):
    """
    Change the temporal resolution of values that have a constant sampling rate
    
    Parameters
    ----------
    values : array-like
        data points
    oldResolution : integer
        temporal resolution of the given values. oldResolution=3600 means
        hourly sampled data
    newResolution : integer
        temporal resolution of the given data shall be converted to
    method : ``{"mean"; "sum"}``, optional
        - ``"mean"`` : compute mean values while resampling (e.g. for power).
        - ``"sum"``  : compute sum values while resampling (e.g. for energy).
    """
    # Compute original time indexes
    timeOld = np.arange(len(values)) * oldResolution
    
    # Compute new time indexes
    length = math.ceil(len(values) * oldResolution / newResolution)
    timeNew = np.arange(length) * newResolution

    # Sample means or sum values
    if method == "mean":
        # Interpolate
        valuesResampled = np.interp(timeNew, timeOld, values)        
    else:
        # If values have to be summed up, use cumsum to modify the given data
        # Add one dummy value to later use diff (which reduces the number of
        # indexes by one)
        values = np.cumsum(np.concatenate(([0], values)))
        timeOld = np.concatenate((timeOld, [timeOld[-1]+oldResolution]))
        timeNew = np.concatenate((timeNew, [timeNew[-1]+newResolution]))
        
        # Interpolate
        valuesResampled = np.interp(timeNew, timeOld, values)
        
        # "Undo" the cumsum
        valuesResampled = np.diff(valuesResampled)        

    return valuesResampled
    
if __name__ == "__main__":
    values_old = np.arange(2000)
    dt_old = 60
    dt_new = 600
    values_new = changeResolution(values_old, dt_old, dt_new)
    
    # Temperature - mean values
    f_TRY = "inputs/weather/TRY2010_05_Jahr.dat"
    temp = np.loadtxt(f_TRY, skiprows=38, usecols=(8,))
    dt_temp_old = 3600
    dt_temp_short = 900
    dt_temp_long = 7200
    temp_long = changeResolution(temp, dt_temp_old, dt_temp_long)
    temp_short = changeResolution(temp, dt_temp_old, dt_temp_short)
    
    # Energy - sum values
    np.random.seed(0)
    profile = np.sort(np.random.rand(1440)) # minute wise sampling
    dt_prof_old = 60
    dt_prof_short = 20
    dt_prof_long = 900
    dt_prof_huge = 3600
    prof_short = changeResolution(profile, dt_prof_old, dt_prof_short)
    prof_long = changeResolution(profile, dt_prof_old, dt_prof_long)
    prof_huge = changeResolution(profile, dt_prof_old, dt_prof_huge)
    
    slp = np.loadtxt("inputs/standard_load_profile/slp_el_h0.txt")
    dt_slp = 900
    dt_slp_short = 450
    dt_slp_long = 3600
    slp_short = changeResolution(slp, dt_slp, dt_slp_short, "sum")
    slp_long = changeResolution(slp, dt_slp, dt_slp_long, "sum")
    