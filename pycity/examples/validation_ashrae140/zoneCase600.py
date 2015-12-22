#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 16:02:31 2015

@author: tsz
"""

from __future__ import division

import os
import numpy as np

import pycity.classes.Timer
import pycity.classes.Sun
import pycity.classes.Weather
import pycity.classes.Prices
import pycity.classes.Environment

import pycity.classes.demand.SpaceHeating as sh
import pycity.classes.demand.ZoneParameters as zp

import pycity.examples.validation_ashrae140.plotCase600 as plotCase600


location = (39.76, -104.86)

altitude = 1609  # m, section 5.2.1.6.1, page 16
timeZone = -7

timer = pycity.classes.Timer.Timer(timeDiscretization=3600,
                                   timestepsHorizon=8760,
                                   timestepsUsedHorizon=8760,
                                   timestepsTotal=8760)
prices = pycity.classes.Prices.Prices()

#  Define src path
ashrae_path = os.path.dirname(os.path.abspath(__file__))

temp_name = 'weather_temperature.csv'
beam_name = 'weather_beam.csv'
diffuse_name = 'weather_diffuse.csv'
weather_temp_path = os.path.join(ashrae_path, temp_name)
weather_beam_path = os.path.join(ashrae_path, beam_name)
weather_diffuse_path = os.path.join(ashrae_path, diffuse_name)

weather = pycity.classes.Weather.Weather(timer,
                                         pathTemperature=weather_temp_path,
                                         pathDirectRadiation=weather_beam_path,
                                         pathDiffuseRadiation=weather_diffuse_path,
                                         timeDiscretization=3600,
                                         delimiter="\t",
                                         useTRY=False,
                                         location=location,
                                         altitude=altitude,
                                         timeZone=timeZone)

prices = pycity.classes.Prices.Prices()

environment = pycity.classes.Environment.Environment(timer, weather, prices)

# beta: slope angle, gamma: surface azimuth angle
# S, W, N, E, Roof
beta = [90, 90, 90, 90, 0]
gamma = [0, 90, 180, 270, 0]
albedo = 0.2  # Ground reflectance, section 5.2.1.1.2, page 16

internalGains = 200 * np.ones(timer.timestepsTotal)  # W, section 5.2.1.7, page 16

# Data from ASHRAE 140 : 2011
A_f = 48  # m2, section 5.2.1.3, page 16 (48 m2 floor area)
#          low mass building, same section

heightWalls = 2.7  # m, Figure 5.1, page 16
volume = A_f * heightWalls

# Material properties: Table 5.1
# Floor touches the ground
# No underfloor insulation

# Opaque surfaces: Table 5.3, page 18
solarAbsorptance = 0.6  # alpha
infraredEmittance = 0.9  # epsilon

# Index-Orientation: South, West, North, East, Roof, Floor
A_windows = np.array([12, 0, 0, 0, 0, 0])
length_SN = 8
length_WE = 6
A_walls_SN = length_SN * heightWalls  # South and North
A_walls_WE = length_WE * heightWalls  # West and East
A_walls = np.array([A_walls_SN, A_walls_WE, A_walls_SN, A_walls_WE, A_f, A_f])
A_walls = A_walls - A_windows
U_walls = np.array([0.514, 0.514, 0.514, 0.514, 0.318, 0.039])  # air-air
# U_walls = np.array([0.559, 0.559, 0.559, 0.559, 0.334, 0.040]) # surf-surf
U_windows = np.array([3, 3, 3, 3, 3, 3])  # table 5.6, page 19

g_gln = 0.789  # (solar heat gain coefficient) table 5.6, page 19

# Computation of the specific heat capacity of each wall
specificHeatCapacity = lambda d, rho, cp: np.sum(d * rho * cp)
# Data: Table 5.1, page 17
# Exterior wall (South, West, East, North)
d_extWall = np.array([0.012, 0.066, 0.009])
rho_extWall = np.array([950, 12, 530])
cp_extWall = np.array([840, 840, 900])
c_extWall = specificHeatCapacity(d_extWall, rho_extWall, cp_extWall)

# Floor
d_floor = np.array([0.025, 1.003])
rho_floor = np.array([650, 0])
cp_floor = np.array([1200, 0])
c_floor = specificHeatCapacity(d_floor, rho_floor, cp_floor)

# Roof
d_roof = np.array([0.0100, 0.1118, 0.019])
rho_roof = np.array([950, 12, 530])
cp_roof = np.array([840, 840, 900])
c_roof = specificHeatCapacity(d_roof, rho_roof, cp_roof)

R_se_op = [0.034, 0.034, 0.034, 0.034, 0.034, 0]  # Table 5.1, page 17
R_se_w = [0.0476, 0.0476, 0.0476, 0.0476, 0.0476, 0]  # Table 5.6, page 19

c = np.array([c_extWall, c_extWall, c_extWall, c_extWall, c_roof, c_floor])

zoneParameters = zp.ZoneParameters(A_f=A_f,
                                   A_w=A_windows,
                                   U_w=U_windows,
                                   g_gln=g_gln,
                                   epsilon_w=infraredEmittance,
                                   R_se_w=R_se_w,
                                   A_op=A_walls,
                                   U_op=U_walls,
                                   alpha_Sc=solarAbsorptance,
                                   R_se_op=R_se_op,
                                   epsilon_op=infraredEmittance,
                                   V=volume,
                                   samplingRate=timer.timeDiscretization,
                                   kappa_j=c,
                                   A_j=A_walls,
                                   simplifiedCapacity=False,
                                   albedo=albedo,
                                   beta=beta,
                                   gamma=gamma)

# Ventilation
ventilation = np.ones(timer.timestepsTotal) * 0.5  # section 5.2.1.6, page 16

ventilationFactor = 0.822  # Adjustment factor, see Table 5.2, page 18
ventilation = ventilation * ventilationFactor  # Final adjustment factor, see
# Footnote at Table 5.2, page 18
zoneParameters.updateVentilation(ventilationRate=ventilation,
                                 ventilationRateMinimum=0)


# Set points (section 5.2.1.13.1.1, page 19)
T_set_heating = np.ones(timer.timestepsTotal) * 20
T_set_cooling = np.ones(timer.timestepsTotal) * 27

# Initialize T_m
T_m_init = 20

spaceHeating = sh.SpaceHeating(environment,
                               method=2,
                               zoneParameters=zoneParameters,
                               T_m_init=T_m_init,
                               appliances=internalGains,
                               TCoolingSet=T_set_cooling,
                               THeatingSet=T_set_heating)

# Retrieve results
Q_HC = spaceHeating.loadcurve
solarOpaque = spaceHeating.zoneInputs.solarOpaque
solarWindow = spaceHeating.zoneInputs.solarWindow

# Pass results to the plotting script
from collections import namedtuple

keys = ["heatingLoad", "coolingLoad",
        "heatingPeak", "heatingPeakTime", "coolingPeak", "coolingPeakTime",
        "solarGainsSouth", "solarGainsWest", "solarGainsNorth",
        "solarGainsEast", "solarGainsHorizontal", "solarGainsWindowSouth",
        "solarSouthMarch5", "solarSouthJuly27",
        "solarWestMarch5", "solarWestJuly27", "january4"]
Results = namedtuple("Results", keys)

results = Results(heatingLoad=np.sum(Q_HC[Q_HC > 0]) / 1000000,  # in MWh
                  coolingLoad=-np.sum(Q_HC[Q_HC < 0]) / 1000000,  # in MWh
                  heatingPeak=np.max(Q_HC) / 1000,  # in kW
                  heatingPeakTime=np.argmax(Q_HC),  # time step in hours
                  coolingPeak=-np.min(Q_HC) / 1000,  # in kW
                  coolingPeakTime=np.argmin(Q_HC),  # time step in hours
                  solarGainsSouth=np.sum(solarOpaque[0]) / 1000,  # in kWh per m2
                  solarGainsWest=np.sum(solarOpaque[1]) / 1000,  # in kWh per m2
                  solarGainsNorth=np.sum(solarOpaque[2]) / 1000,  # in kWh per m2
                  solarGainsEast=np.sum(solarOpaque[3]) / 1000,  # in kWh per m2
                  solarGainsHorizontal=np.sum(solarOpaque[4]) / 1000,  # in kWh per m2
                  solarGainsWindowSouth=np.sum(solarWindow[0]) / 1000,  # in kWh per m2
                  solarSouthMarch5=solarOpaque[0][1513:1537],
                  solarSouthJuly27=solarOpaque[0][4969:4993],
                  solarWestMarch5=solarOpaque[1][1513:1537],
                  solarWestJuly27=solarOpaque[1][4969:4993],
                  january4=Q_HC[73:97] / 1000)


# Function to convert hour_of_the_year into [month, day, hour]
def transformTime(timestep):
    names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
             "Oct", "Nov", "Dec"]
    months = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
    monthsCum = np.cumsum(months)
    day_of_year = int(timestep / 24) + 1
    hour = timestep % 24
    temp = monthsCum - day_of_year
    try:
        day = -np.max(temp[temp < 0])  # does not work in January, max([])
    except:
        day = day_of_year
    month = names[np.argmin(temp < 0)]
    return [month, day, hour]


# print results
print()
print("Results Case 600")
print("Heating load: " + str(round(results.heatingLoad, 3)))
print("Reference: min: 4.296, max: 5.709, mean: 5.090")
print()
print("Cooling load: " + str(round(results.coolingLoad, 3)))
print("Reference: min: 6.137, max: 7.964, mean: 6.832")
print()
print()
print("Heating peak: " + str(round(results.heatingPeak, 3)))
print("Reference: min: 3.437, max: 4.354, mean: 4.000")
print("Heating peak time: " + str(transformTime(int(results.heatingPeakTime))))
print("Reference: 04-Jan,5; 01-Jan,5; 01-Jan,2; 01-Jan,6")
print()
print()
print("Cooling peak: " + str(round(results.coolingPeak, 3)))
print("Reference: min: 5.965, max: 6.827, mean: 6.461")
print("Cooling peak time: " + str(transformTime(int(results.coolingPeakTime))))
print("Reference: 17-Oct,13; 01-Nov,14; 16-Oct,14")
print()
print()
print("Solar gains North: " + str(round(results.solarGainsNorth)))
print("Reference: min: 367, max: 457, mean: 429")
print()
print("Solar gains East: " + str(round(results.solarGainsEast)))
print("Reference: min: 959, max: 1217, mean: 1080")
print()
print("Solar gains West: " + str(round(results.solarGainsWest)))
print("Reference: min: 857, max: 1090, mean: 1018")
print()
print("Solar gains South: " + str(round(results.solarGainsSouth)))
print("Reference: min: 1456, max: 1566, mean: 1490")
print()
print("Solar gains horizontal: " + str(round(results.solarGainsHorizontal)))
print("Reference: min: 1797, max: 1832, mean: 1827")
print()
print()
print("Solar gains windows (South): " + str(round(
    results.solarGainsWindowSouth)))
print("Reference: min: 914, max: 1051, mean: 962")


# plotCase600.plotResults(results)

plotCase600.plotWestSurface(results)
# plotCase600.plotSouthSurface(results)

# plotCase600.plotJanuary4(results)
