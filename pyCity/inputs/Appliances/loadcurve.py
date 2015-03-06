# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 18:08:46 2015

@author: tsz
"""
from __future__ import division
import numpy as np
import math

def extend_loadcurve(time, power):
    """
    Make a 1-second sampling time
    """
    
    extended_time = np.array(range(max(time)))
    extended_power = np.zeros(extended_time.shape)
    
    extended_power[0] = power[0]    
    
    i = 0 # index extended
    j = 0 # index normal
    
    while i < len(extended_time):
        if extended_time[i] < time[j]:
            extended_power[i] = power[j]
            i += 1
        else:
            j += 1
    
    return (extended_time, extended_power)

def create_loadcurve(time, power, discretization):
    """
    """

    (time, power) = extend_loadcurve(time, power)
    
    res_time = np.array(range(int(math.ceil(max(time)/discretization))))
    res_power = np.zeros(res_time.shape)
    
    i = 0 # res_time
    j = 0 # time
    
    while i < len(res_time)-1:
        try:
            res_power[i] = np.sum(power[j:j+discretization])
        except:
            print i
            print j
        i += 1
        j += discretization
    res_power[-1] = np.sum(power[j:len(power)])
    
    return (res_time*discretization, res_power/discretization)
    
def get_electrical_thermal(power, dishwasher=True):
    """
    """
    electrical = np.zeros_like(power)
    thermal    = np.zeros_like(power)
    
    if dishwasher:
        # Retrieve all time steps during which the thermal heater is active:
        threshold = 500        
        times_peak = power > threshold
        times_baseload = times_peak == False

        # Determine electrical baseload:
        baseload_power = power[times_baseload]
        baseload_electrical = np.mean(baseload_power)
        
        # Determine thermal load
        thermal_temp = np.zeros_like(power)
        thermal_temp[times_peak] = power[times_peak] - baseload_electrical
        # Only the first 5800 are relevant (last peaks are drying -> no water usage)
        relevant_timesteps = 5800
        thermal[0:relevant_timesteps] = thermal_temp[0:relevant_timesteps]
        
        electrical = power - thermal
    else:
        threshold = 1000
        times_peak = power > threshold
        times_baseload = times_peak == False

        # Determine electrical baseload:
        baseload_power = power[times_baseload]
        baseload_electrical = np.mean(baseload_power)
        
        # Determine thermal load
        thermal[times_peak] = power[times_peak] - baseload_electrical
        electrical = power - thermal
    return (electrical, thermal)
        

#
dw_p = dw_power[:,0]
dw_t = dw_time[:,0]
wm_p = wm_power[:,0]
wm_t = wm_time[:,0]
#dw_p = dw_power[:]
#dw_t = dw_time[:]
#wm_p = wm_power[:]
#wm_t = wm_time[:]

#(ext_time, ext_power) = extend_loadcurve(dw_t, dw_p)
discretization = 1
(dw_res_time, dw_res_power) = create_loadcurve(dw_t, dw_p, discretization)
(wm_res_time, wm_res_power) = create_loadcurve(wm_t, wm_p, discretization)

(dw_electrical, dw_thermal) = get_electrical_thermal(dw_res_power)
(wm_electrical, wm_thermal) = get_electrical_thermal(wm_res_power, False)

np.savetxt("dishwasher_purely_electrical.txt", np.transpose(np.concatenate(([dw_res_time],[dw_res_power]))),  fmt="%.0f", delimiter="\t")
np.savetxt("dishwasher_mixed_electrical.txt",  np.transpose(np.concatenate(([dw_res_time],[dw_electrical]))), fmt="%.0f", delimiter="\t")
np.savetxt("dishwasher_mixed_thermal.txt",     np.transpose(np.concatenate(([dw_res_time],[dw_thermal]))),    fmt="%.0f", delimiter="\t")
np.savetxt("waschingmachine_purely_electrical.txt", np.transpose(np.concatenate(([wm_res_time],[wm_res_power]))) , fmt="%.0f", delimiter="\t")
np.savetxt("washingmachine_mixed_electrical.txt",   np.transpose(np.concatenate(([wm_res_time],[wm_electrical]))), fmt="%.0f", delimiter="\t")
np.savetxt("washingmachine_mixed_thermal.txt",      np.transpose(np.concatenate(([wm_res_time],[wm_thermal]))),    fmt="%.0f", delimiter="\t")