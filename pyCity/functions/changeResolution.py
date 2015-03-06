# -*- coding: utf-8 -*-
"""
Created on Wed Feb 11 11:00:03 2015

@author: tsz
"""

from __future__ import division

import pandas as pd

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
        ``"mean"`` : compute mean values while resampling.
        ``"sum"``  : compute sum values while resampling.
    """
    # Compute time indexes
    timeIndex = pd.date_range(0, periods=len(values), freq=str(oldResolution)+"s")

    # Construct original time series
    timeseriesOld = pd.Series(data=values, index=timeIndex)
    
    # Resample
    # When using "mean" for a timeseries that does not have sufficient entries 
    # (e.g. hourly data should be resampled on a daily scheme, but there are 
    # only 40 instead of 48 data points available), the final time period was 
    # averaged by the available data (16 instead of 24 hours).
    # Using "sum" and dividing/multiplying by the resolution worked fine.
    timeseriesNew = timeseriesOld.resample(rule=str(newResolution)+"s", how="sum", fill_method="pad")
    if method == "mean" and newResolution > oldResolution:
        timeseriesNew = timeseriesNew * oldResolution / newResolution

    # Get resampled values
    valuesResampled = timeseriesNew.get_values()
    
    return valuesResampled
    
