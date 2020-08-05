# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 11:16:49 2016

@author: tsz
"""

from __future__ import division

import os
import numpy as np

import pycity_base.classes.timer
import pycity_base.classes.sun
import pycity_base.classes.weather
import pycity_base.classes.prices
import pycity_base.classes.environment

import pycity_base.classes.demand.occupancy
import pycity_base.classes.demand.electrical_demand as ED
import pycity_base.classes.demand.domestic_hot_water as DomesticHotWater

import pycity_base.classes.demand.space_heating as sh
import pycity_base.classes.demand.zone_parameters as zp


# Location: Denver (weather inputs from ASHRAE 140 verification)
location = (39.76, -104.86)

altitude = 1609  # m
time_zone = -7

timer = pycity_base.classes.timer.Timer(time_discretization=3600,
                                        timesteps_horizon=8760,
                                        timesteps_used_horizon=8760,
                                        timesteps_total=8760)
prices = pycity_base.classes.prices.Prices()

#  Define src path
ashrae_path = os.path.dirname(os.path.abspath(__file__))

weather_temp_path = os.path.join(ashrae_path, 'weather_temperature.csv')
weather_beam_path = os.path.join(ashrae_path, 'weather_beam.csv')
weather_diffuse_path = os.path.join(ashrae_path, 'weather_diffuse.csv')

weather = pycity_base.classes.weather.Weather(timer,
                                              path_temperature=weather_temp_path,
                                              path_direct_radiation=weather_beam_path,
                                              path_diffuse_radiation=weather_diffuse_path,
                                              time_discretization=3600,
                                              delimiter="\t",
                                              use_TRY=False,
                                              location=location,
                                              altitude=altitude,
                                              time_zone=time_zone)

prices = pycity_base.classes.prices.Prices()

environment = pycity_base.classes.environment.Environment(timer, weather, prices)


# Occupancy and electrical demand
occupancy = pycity_base.classes.demand.occupancy.Occupancy(environment,
                                                           number_occupants=3)

energy_input = 3000

el_dem_stochastic = ED.ElectricalDemand(environment,
                                        method=2,
                                        annual_demand=energy_input,
                                        total_nb_occupants=3,
                                        randomize_appliances=True,
                                        light_configuration=10,
                                        occupancy=occupancy.occupancy,
                                        do_normalization=True)

demand_electricity = el_dem_stochastic.loadcurve

# Domestic hot water demand
dhw_stochastical = DomesticHotWater.DomesticHotWater(environment,
                                                     t_flow=60,
                                                     thermal=True,
                                                     method=2,
                                                     supply_temperature=20,
                                                     occupancy=occupancy.occupancy)

demand_hot_water = dhw_stochastical.loadcurve

# Building model
# beta: slope angle, gamma: surface azimuth angle
# S, W, N, E, Roof
beta = [90, 90, 90, 90, 0]
gamma = [0, 90, 180, 270, 0]
albedo = 0.2

internalGains = 0.3 * demand_electricity

# Heated floor area
A_f = 150  # m^2

heightWalls = 3.0  # m
volume = A_f * heightWalls

# Material properties
# Opaque surfaces
solarAbsorptance = 0.7  # alpha
infraredEmittance = 0.9  # epsilon

# Index-Orientation: South, West, North, East, Roof, Floor
A_windows = np.array([7.5, 7.5, 7.5, 7.5, 0, 0])
A_walls_ext = np.array([42.25, 42.25, 42.25, 42.25, 99.75, 99.75])
A_walls = A_walls_ext - A_windows

A_walls_int = [375, 75, 75] #m²; [intWall, intCeiling, intFloor]
A_walls = np.append(A_walls_ext, A_walls_int)

g_gln = 0.67 / 0.9  # solar heat gain coefficient

# Computation of the specific heat capacity of each wall
def specificHeatCapacity(d, d_iso, density, cp):
    """ 
    ISO 13786:2007 A.2
    Computation of (specific) heat capacity of each wall-type-surface
    
    Result is in J/m^2K
    """
    d_t = min(0.5 * np.sum(d), d_iso , 0.1)
    sum_d_i = d[0]
    i = 0 
    kappa = 0       
    while sum_d_i <= d_t:
        kappa += d[i] * density[i] * cp[i]
        i += 1
        sum_d_i += d[i]
    else:
        sum_d_i -=  d[i]
        d_part = d_t - sum_d_i          
        kappa += d_part * density[i] * cp[i]

    return kappa

# Data
# Exterior wall (South, West, East, North)
d_extWall = np.array([0.0125, 0.1])
rho_extWall = np.array([800, 30])
cp_extWall = np.array([1000, 1000])
c_extWall = specificHeatCapacity(d_extWall, 0.0125, rho_extWall, cp_extWall)

lambda_extWall = np.array([0.25, 0.04]) # [inside, ..., outside] [W/(mK)]
alpha_extWall = np.array([7.7, 25.0])    # [inside, outside] [W/(m²K)]
U_extWall = 1 / (1 / alpha_extWall[0] + sum(d_extWall / lambda_extWall) + 1 / alpha_extWall[1])

# Floor
d_floor = np.array([0.04, 0.03, 0.02, 0.15])
rho_floor = np.array([2000, 30, 600, 50])
cp_floor = np.array([1000, 1000, 1700, 1000])
c_floor = specificHeatCapacity(d_floor, 0.04, rho_floor, cp_floor)

lambda_floor = np.array([1.4, 0.04, 0.17, 0.12])
alpha_floor = np.array([6.7])
U_floor = 0.039

# Roof
d_roof = np.array([0.0125, 0.15, 0.03])
rho_roof = np.array([800, 105, 1800])
cp_roof = np.array([1000, 1000, 1000])
c_roof = specificHeatCapacity(d_roof, 0.0125, rho_roof, cp_roof)

lambda_roof = np.array([0.25, 0.05, 0.7])
alpha_roof = np.array([6.7, 25])
U_roof = 1 / (1 / alpha_roof[0] + sum(d_roof / lambda_roof) + 1 / alpha_roof[1])

R_se_op = [0.04, 0.04, 0.04, 0.04, 0.04, 0]
R_se_w  = [0.04, 0.04, 0.04, 0.04, 0.04, 0]


months = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
monthsCum = np.cumsum(months)
monthsCum0 = np.append(np.array([0]),monthsCum)
T_aver_mon = []
b_m = []
Po_m = []

for i in range(12):
    T_aver_mon = np.append(T_aver_mon, 
                           sum(weather.t_ambient[monthsCum0[i]*24:monthsCum0[i+1]*24]) / months[i] / 24 )
T_i_year = 22.917 
# Heating period starts in October and ends in April
for i in range(4):
    for k in range(months[i]*24):
        b_m = np.append(b_m, (T_i_year - 9.71)/(20 - T_aver_mon[i]))
for i in range(5):
    for k in range(months[4+i]*24):
        b_m = np.append(b_m, (T_i_year - 9.71)/(27 - T_aver_mon[4+i]))
for i in range(3):
    for k in range(months[9+i]*24):
        b_m = np.append(b_m, (T_i_year - 9.71)/(20 - T_aver_mon[9+i]))
        
U_floor = 1 / (1 / alpha_floor[0] + sum(d_floor / lambda_floor))
U_floor_bm = np.multiply(U_floor, b_m)


# Interior wall
d_intWall   = np.array([   0.0125, 0.07, 0.0125])
rho_intWall = np.array([ 790.0, 20.0, 790.0])
cp_intWall  = np.array([1000, 1000, 1000])
c_intWall   = specificHeatCapacity(d_intWall, 10, rho_intWall, cp_intWall) 

# Interior ceiling
d_intCeiling  = np.array([  0.15 , 0.02, 0.03,0.04])
rho_intCeiling = np.array([ 50.0, 600.0, 30.0,2000.0])
cp_intCeiling  = np.array([1000, 1700, 1000, 1000])
c_intCeiling   = specificHeatCapacity(d_intCeiling, 10, rho_intCeiling, cp_intCeiling)

## Interior floor
d_intFloor   = np.array([   0.04, 0.03, 0.02, 0.15])
rho_intFloor = np.array([ 2000.0, 30.0, 600.0, 50.0])
cp_intFloor  = np.array([1000, 1000, 1700, 1000])
c_intFloor   = specificHeatCapacity(d_intFloor, 10, rho_intFloor, cp_intFloor)

# Windows
d_window   = np.array([ 0.024])
lambda_window = np.array([0.067])
alpha_window = np.array([7.7, 25.0])
U_window = 1 / (1 / alpha_window[0] + sum(d_window / lambda_window) + 1 / alpha_window[1])


U_walls_ext_bm = []
for i in range(timer.timesteps_total):
    U_walls_ext_bm.append(np.array([U_extWall, U_extWall, U_extWall, U_extWall, U_roof, U_floor_bm[i]]))
U_windows = np.array([U_window, U_window, U_window, U_window, U_window, U_window])

R_se_op = [0.04,  0.04,  0.04,  0.04,  0.04,  0]
R_se_w  = [0.04, 0.04, 0.04, 0.04, 0.04, 0]

c = np.array([c_extWall, c_extWall, c_extWall, c_extWall, c_roof, c_floor, c_intWall, c_intCeiling, c_intFloor])


zone_parameters = zp.ZoneParameters(A_f=A_f,
                                   A_w=A_windows,
                                   U_w=U_windows,
                                   g_gln=g_gln,
                                   epsilon_w=infraredEmittance,
                                   R_se_w=R_se_w,
                                   A_op=A_walls_ext,
                                   U_op=U_walls_ext_bm,
                                   alpha_Sc=solarAbsorptance,
                                   R_se_op=R_se_op,
                                   epsilon_op=infraredEmittance,
                                   V=volume,
                                   sampling_rate=timer.time_discretization,
                                   kappa_j=c,
                                   A_j=A_walls,
                                   simplified_capacity=False,
                                   albedo=albedo,
                                   beta=beta,
                                   gamma=gamma)

# Ventilation
ventilation = np.ones(timer.timesteps_total) * 0.5

ventilationFactor = 0.822
ventilation = ventilation * ventilationFactor

zone_parameters.updateVentilation(ventilationRate=ventilation,
                                 ventilationRateMinimum=0.41)


# Set points
T_set_cooling = np.ones(timer.timesteps_total) * 27

heating_mode = 20
setback_mode = 18
dt = len(occupancy.occupancy) // timer.timesteps_total
occupancy_reshaped = np.array([np.mean(occupancy.occupancy[dt*i: dt*(i+1)]) 
                               for i in range(timer.timesteps_total)])

T_set_heating = np.ones(timer.timesteps_total) * setback_mode
T_set_heating[occupancy_reshaped>0] += occupancy_reshaped[occupancy_reshaped>0] * (heating_mode - setback_mode)
T_set_heating = np.minimum(T_set_heating, heating_mode)


# Initialize T_m
t_m_init = 20

spaceHeating = sh.SpaceHeating(environment,
                               method=2,
                               zone_parameters=zone_parameters,
                               t_m_init=t_m_init,
                               appliances=internalGains,
                               t_cooling_set=T_set_cooling,
                               t_heating_set=T_set_heating)

demand_spaceheating = spaceHeating.loadcurve

demands = {"electricity": demand_electricity,
           "domestic hot water": demand_hot_water,
           "space heating": demand_spaceheating}
