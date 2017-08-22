#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 21:24:23 2015

@author: Thomas
"""

from __future__ import division
import numpy as np
import numpy.linalg as linalg


def _solve(A, b):
    return linalg.solve(A,b)

def _calculateNoHeat(zoneParameters, zoneInputs, T_m_init, q=0, timestep=0):
    """
    Calculate the temperatures (T_op, T_m, T_air, T_s) if neither heating nor
    cooling devices are activated. 
    This is necessary to enable a deadband between cooling and heating mode.
    
    Parameters
    ----------
    zoneParameters : ZoneParameters
        Resistances and capacity
    zoneInputs : ZoneInputs
        External inputs (solar, internal gains, set temperatures)
    T_m_init : float
        Initial temperature of the thermal mass in degree Celsius.
    q : float, optional
        Heating (positive) or cooling (negative) power provided to the zone.
    timestep : integer, optional
        Define which index is relevant (zoneInputs, H_ve)
        
    Returns
    -------
    T_op : float
        .
    T_m : float
        .
    T_air : float
        .
    T_s : float
        .
    """
    
    # Note: If not stated differently, all equations, pages and sections
    # refer to DIN EN ISO 13790:2008 (the official German version of 
    # ISO 13790:2008).
    
    # Extract parameters
    A_m     = zoneParameters.A_m            # in m2
    A_t     = zoneParameters.A_t            # in m2
    H_tr_is = zoneParameters.H_tr_is        # in W/K
    H_tr_ms = zoneParameters.H_tr_ms        # in W/K
    H_tr_w  = zoneParameters.H_tr_w         # in W/K
    H_ve    = zoneParameters.H_ve[timestep] # in W/K
    C_m     = zoneParameters.C_m            # in J/K
    
    if len(zoneParameters.H_tr_em) > 1:
        H_tr_em = zoneParameters.H_tr_em[timestep] # in W/K
    else:
        H_tr_em = zoneParameters.H_tr_em            # in W/K

    dt      = zoneParameters.samplingRate # in s
    
    Phi_int = zoneInputs.Phi_int[timestep]
    Phi_sol = zoneInputs.Phi_sol[timestep]
    T_e     = zoneInputs.T_e[timestep]
    T_sup   = zoneInputs.T_sup[timestep]
    
    # Compute internal and solar heat sources
    # Equations C1-C3, section C2, page 110
    Phi_ia = 0.5 * Phi_int
    Phi_m  = A_m / A_t * (0.5 * Phi_int + Phi_sol)
    Phi_st = (1 - A_m / A_t - H_tr_w / (9.1 * A_t)) * (0.5 * Phi_int + Phi_sol)
    
    # Initialize A*x = b
    # x: T_m, T_s, T_air (T_i), Q_HC
    A = np.zeros((3,3))
    b = np.zeros(3)
    
    # Row wise entering
    A[0,0] = H_tr_em + H_tr_ms + C_m / dt
    A[0,1] = - H_tr_ms
    A[1,0] = - H_tr_ms
    A[1,1] = H_tr_ms + H_tr_is + H_tr_w
    A[1,2] = - H_tr_is
    A[2,1] = - H_tr_is
    A[2,2] = H_ve + H_tr_is
    
    b[0] = Phi_m + H_tr_em * T_e + C_m * T_m_init / dt
    b[1] = Phi_st + H_tr_w * T_e
    b[2] = Phi_ia + H_ve * T_sup + q

    # Solve for "x"
    x = _solve(A, b)
    
    T_i = x[2]
    T_s = x[1]
    T_m = x[0]
        
    weight = 0.3
    T_op = weight * T_i + (1 - weight) * T_s
    return (T_op, T_m, T_i, T_s)
    
    
def _calculateHeat(zoneParameters, zoneInputs, T_m_init, T_set, timestep=0):
    """
    Calculate the temperatures (Q_HC, T_op, T_m, T_air, T_s) that result when
    reaching a given set temperature T_set. 
    
    Parameters
    ----------
    zoneParameters : ZoneParameters
        Resistances and capacity
    zoneInputs : ZoneInputs
        External inputs (solar, internal gains, set temperatures)
    T_m_init : float
        Initial temperature of the thermal mass in degree Celsius.
    T_set : float
        Set temperature in degree Celsius.
    timestep : integer, optional
        Define which index is relevant (zoneInputs, H_ve)
        
    Returns
    -------
    Q_HC : float
        Heating (positive) or cooling (negative) load for the current time 
        step in Watt.
    T_op : float
        .
    T_m : float
        .
    T_air : float
        .
    T_s : float
        .
    """
    
    # Note: If not stated differently, all equations, pages and sections
    # refer to DIN EN ISO 13790:2008 (the official German version of 
    # ISO 13790:2008).
    
    # Extract parameters
    A_m     = zoneParameters.A_m            # in m2
    A_t     = zoneParameters.A_t            # in m2
    H_tr_is = zoneParameters.H_tr_is        # in W/K
    H_tr_ms = zoneParameters.H_tr_ms        # in W/K
    H_tr_w  = zoneParameters.H_tr_w         # in W/K
    H_ve    = zoneParameters.H_ve[timestep] # in W/K
    C_m     = zoneParameters.C_m            # in J/K

    if len(zoneParameters.H_tr_em) > 1:
        H_tr_em = zoneParameters.H_tr_em[timestep] # in W/K
    else:
        H_tr_em = zoneParameters.H_tr_em            # in W/K

    dt      = zoneParameters.samplingRate # in s
    
    Phi_int = zoneInputs.Phi_int[timestep]
    Phi_sol = zoneInputs.Phi_sol[timestep]
    T_e     = zoneInputs.T_e[timestep]
    T_sup   = zoneInputs.T_sup[timestep]
    
    # Compute internal and solar heat sources
    # Equations C1-C3, section C2, page 110
    Phi_ia = 0.5 * Phi_int
    Phi_m  = A_m / A_t * (0.5 * Phi_int + Phi_sol)
    Phi_st = (1 - A_m / A_t - H_tr_w / (9.1 * A_t)) * (0.5 * Phi_int + Phi_sol)
    
    # Initialize A*x = b
    # x: T_m, T_s, T_air (T_i), Q_HC
    A = np.zeros((4,4))
    b = np.zeros(4)
    
    # Row wise entering
    A[0,0] = H_tr_em + H_tr_ms + C_m / dt
    A[0,1] = - H_tr_ms
    A[1,0] = - H_tr_ms
    A[1,1] = H_tr_ms + H_tr_is + H_tr_w
    A[1,2] = - H_tr_is
    A[2,1] = - H_tr_is
    A[2,2] = H_ve + H_tr_is
    A[2,3] = -1
#    A[3,2] = 0.3
#    A[3,1] = 1 - A[3,2]
    A[3,2] = 1
    
    b[0] = Phi_m + H_tr_em * T_e + C_m * T_m_init / dt
    b[1] = Phi_st + H_tr_w * T_e
    b[2] = Phi_ia + H_ve * T_sup
    b[3] = T_set

    # Solve for "x"
    x = _solve(A, b)
    
    T_i  = x[2]
    T_s  = x[1]
    T_m  = x[0]
    Q_HC = x[3]
        
    weight = 0.3
    T_op = weight * T_i + (1 - weight) * T_s
    return (Q_HC, T_op, T_m, T_i, T_s)
   
   
def calc(zoneParameters, zoneInputs, TCoolingSet, THeatingSet,
         limitHeating=np.inf, limitCooling=-np.inf, beQuiet=False):
    """
    Compute heating/cooling demand for the thermal zone. 
    Deadbands between heating and cooling temperatures are considered.
    
    Parameters
    ----------
    zoneParameters : ZoneParameters
        Resistances and capacity
    zoneInputs : ZoneInputs
        External inputs (solar, internal gains, set temperatures)
    TCoolingSet : array_like
        Cooling set temperatures in degC.
    THeatingSet : array_like
        Heating set temperatures in degC.
    limitHeating : float, optional
        Maximum available heating power in Watt.
    limitCooling : float, optional
        Maximum available cooling power in Watt.
    beQuiet : Boolean, optional
        Print current progress (False) or be quiet (True)
    
    Returns
    -------
    Q_HC : array_like
        Heating/cooling demand. Positive values indicate heating demand,
        negative values cooling demand.
    T_op : array_like
        Operating temperature inside the thermal zone in degC. This 
        temperature serves as actual temperature for the zone controller.        
    T_m : array_like
        Temperature of the thermal mass in degC.
    T_i : array_like
        Air temperature in degC.
    T_s : array_like
        Average temperature of internal components in degC (radiative 
        temperature).
    """
    numberTimesteps = len(zoneInputs.T_e)

    # Initialize results
    T_i  = np.zeros(numberTimesteps)
    T_s  = np.zeros(numberTimesteps)
    T_m  = np.zeros(numberTimesteps)
    Q_HC = np.zeros(numberTimesteps)
    
    for t in range(numberTimesteps):

        if t == 0:
            t_previous = zoneInputs.T_m_init
        else:
            t_previous = T_m[t-1]
        
        # Compute what happens without heating (deadband)
        (t_op, t_m, t_i, t_s) = _calculateNoHeat(zoneParameters, zoneInputs, 
                                                 t_previous, q=0, timestep=t)
        if t_op < THeatingSet[t]:
            # Compute heat demand
            (q_hc, t_op, t_m, t_i, t_s) = _calculateHeat(zoneParameters, 
                                                         zoneInputs, 
                                                         t_previous, 
                                                         THeatingSet[t], 
                                                         timestep=t)

            if q_hc > limitHeating:
                q_hc = limitHeating
                (t_op, t_m, t_i, t_s) = _calculateNoHeat(zoneParameters, 
                                                         zoneInputs, 
                                                         t_previous, 
                                                         q=limitHeating, 
                                                         timestep=t)
                
        elif t_op > TCoolingSet[t]:
            # Compute cooling demand
            (q_hc, t_op, t_m, t_i, t_s) = _calculateHeat(zoneParameters, 
                                                         zoneInputs, 
                                                         t_previous, 
                                                         TCoolingSet[t], 
                                                         timestep=t)
            
            if q_hc < limitCooling:
                q_hc = limitCooling
                (t_op, t_m, t_i, t_s) = _calculateNoHeat(zoneParameters, 
                                                         zoneInputs, 
                                                         t_previous, 
                                                         q=limitCooling, 
                                                         timestep=t)
                                                         
        else:
            # Nothing to do
            q_hc = 0
    
        # Insert results for current time step
        Q_HC[t] = q_hc
        T_m[t]  = t_m
        T_i[t]  = t_i
        T_s[t]  = t_s
        
        # Print progress
        if not beQuiet:
            interval = int(numberTimesteps / 20)
            if t % interval == 0:
                print(("Timestep: " + str(t) + ". Progress: " + 
                       str(t / numberTimesteps) + "."))
    
    # Compute operating temperature
    T_op = 0.3 * T_i + 0.7 * T_s        

    # Return results
    return (Q_HC, T_op, T_m, T_i, T_s)
    
def calculate(zoneParameters, zoneInputs, T_set):
    """
    Compute heating/cooling demand. 
    There is no difference between heating and cooling set temperatures. No 
    deadband is considered.
 
    Parameters
    ----------
    zoneParameters : ZoneParameters
        Resistances and capacity
    zoneInputs : ZoneInputs
        External inputs (solar, internal gains, set temperatures)
    T_set : array_like
        Set value for operating temperature in degC.
    """
    
    # Note: If not stated differently, all equations, pages and sections
    # refer to DIN EN ISO 13790:2008 (the official German version of 
    # ISO 13790:2008).
    
    # Extract parameters
    A_m     = zoneParameters.A_m        # in m2
    A_t     = zoneParameters.A_t        # in m2
    H_tr_is = zoneParameters.H_tr_is    # in W/K
    H_tr_ms = zoneParameters.H_tr_ms    # in W/K
    H_tr_em = zoneParameters.H_tr_em    # in W/K
    H_tr_w  = zoneParameters.H_tr_w     # in W/K
    H_ve    = zoneParameters.H_ve       # in W/K
    C_m     = zoneParameters.C_m        # in J/K

    dt      = zoneParameters.samplingRate # in s
    
    Phi_int = zoneInputs.Phi_int
    Phi_sol = zoneInputs.Phi_sol
    T_e     = zoneInputs.T_e
    T_sup   = zoneInputs.T_sup
    
    numberTimesteps = len(T_e)
    
    # Compute internal and solar heat sources
    # Equations C1-C3, section C2, page 110
    Phi_ia = 0.5 * Phi_int
    Phi_m  = A_m / A_t * (0.5 * Phi_int + Phi_sol)
    Phi_st = (1 - A_m / A_t - H_tr_w / (9.1 * A_t)) * (0.5 * Phi_int + Phi_sol)
    
    # Initialize results
    T_i  = np.zeros(numberTimesteps)
    T_s  = np.zeros(numberTimesteps)
    T_m  = np.zeros(numberTimesteps)
    Q_HC = np.zeros(numberTimesteps)
    

    # Initialize A*x = b
    # x: T_m, T_s, T_air (T_i), Q_HC
    A = np.zeros((4,4))
    b = np.zeros(4)    
    
    # Row wise entering
    # Set the time-invariant components of A
    A[0,0] = H_tr_em + H_tr_ms + C_m / dt
    A[0,1] = - H_tr_ms
    A[1,0] = - H_tr_ms
    A[1,1] = H_tr_ms + H_tr_is + H_tr_w
    A[1,2] = - H_tr_is
    A[2,1] = - H_tr_is
    A[2,3] = -1
    A[3,2] = 0.3
    A[3,1] = 1 - A[3,2]    
    
    # Only the right hand side (b) changes. This is done for each time step:
    for t in range(numberTimesteps):
        if t == 0:
            T_m_previous = zoneInputs.getTInit()
        else:
            T_m_previous = T_m[t-1]
        
        # Set the time-variable components of A
        A[2,2] = H_ve[t] + H_tr_is
        
        b[0] = Phi_m[t] + H_tr_em * T_e[t] + C_m * T_m_previous / dt
        b[1] = Phi_st[t] + H_tr_w * T_e[t]
        b[2] = Phi_ia[t] + H_ve[t] * T_sup[t]
        b[3] = T_set[t]
        
        # Solve for "x"
        x = _solve(A, b)
        
        T_i[t] = x[2]
        T_s[t] = x[1]
        T_m[t] = x[0]
        Q_HC[t] = x[3]
        
    T_op = A[3,2] * T_i + A[3,1] * T_s
    
    return (Q_HC, T_i, T_s, T_m, T_op)