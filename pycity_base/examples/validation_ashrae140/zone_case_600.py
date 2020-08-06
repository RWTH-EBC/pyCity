#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 16:02:31 2015

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

import pycity_base.classes.demand.space_heating as sh
import pycity_base.classes.demand.zone_parameters as zp

import pycity_base.examples.validation_ashrae140.plot_case_600 as plotCase600


def run_validation(do_plot=False):
    location = (39.76, -104.86)

    altitude = 1609  # m, section 5.2.1.6.1, page 16
    time_zone = -7

    timer = pycity_base.classes.timer.Timer(time_discretization=3600,
                                            timesteps_horizon=8760,
                                            timesteps_used_horizon=8760,
                                            timesteps_total=8760)
    prices = pycity_base.classes.prices.Prices()

    #  Define src path
    ashrae_path = os.path.dirname(os.path.abspath(__file__))

    temp_name = 'weather_temperature.csv'
    beam_name = 'weather_beam.csv'
    diffuse_name = 'weather_diffuse.csv'
    weather_temp_path = os.path.join(ashrae_path, temp_name)
    weather_beam_path = os.path.join(ashrae_path, beam_name)
    weather_diffuse_path = os.path.join(ashrae_path, diffuse_name)

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

    environment = pycity_base.classes.environment.Environment(timer, weather,
                                                              prices)

    # beta: slope angle, gamma: surface azimuth angle
    # S, W, N, E, Roof
    beta = [90, 90, 90, 90, 0]
    gamma = [0, 90, 180, 270, 0]
    albedo = 0.2  # Ground reflectance, section 5.2.1.1.2, page 16

    internalGains = 200 * np.ones(
        timer.timesteps_total)  # W, section 5.2.1.7, page 16

    # Data from ASHRAE 140 : 2011
    A_f = 48  # m^2, section 5.2.1.3, page 16 (48 m^2 floor area)
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
    A_walls = np.array(
        [A_walls_SN, A_walls_WE, A_walls_SN, A_walls_WE, A_f, A_f])
    A_walls = A_walls - A_windows
    U_walls = np.array([0.514, 0.514, 0.514, 0.514, 0.318, 0.039])  # air-air
    # U_walls = np.array([0.559, 0.559, 0.559, 0.559, 0.334, 0.040]) # surf-surf
    U_windows = np.array([3, 3, 3, 3, 3, 3])  # table 5.6, page 19

    g_gln = 0.789  # (solar heat gain coefficient) table 5.6, page 19

    # Computation of the specific heat capacity of each wall
    def specificHeatCapacity(d, d_iso, density, cp):
        """
        ISO 13786:2007 A.2
        Computation of (specific) heat capacity of each wall-type-surface

        Result is in J/m^2K
        """
        d_t = min(0.5 * np.sum(d), d_iso, 0.1)
        sum_d_i = d[0]
        i = 0
        kappa = 0
        while sum_d_i <= d_t:
            kappa += d[i] * density[i] * cp[i]
            i += 1
            sum_d_i += d[i]
        else:
            sum_d_i -= d[i]
            d_part = d_t - sum_d_i
            kappa += d_part * density[i] * cp[i]

        return kappa

    # Data: Table 5.1, page 17
    # Exterior wall (South, West, East, North)
    d_extWall = np.array([0.012, 0.066, 0.009])
    rho_extWall = np.array([950, 12, 530])
    cp_extWall = np.array([840, 840, 900])
    c_extWall = specificHeatCapacity(d_extWall, 0.012, rho_extWall, cp_extWall)

    U_extWall = 0.514

    # Floor
    d_floor = np.array([0.025, 1.003])
    rho_floor = np.array([650, 0])
    cp_floor = np.array([1200, 0])
    c_floor = specificHeatCapacity(d_floor, 0.025, rho_floor, cp_floor)

    U_floor = 0.039

    # Roof
    d_roof = np.array([0.0100, 0.1118, 0.019])
    rho_roof = np.array([950, 12, 530])
    cp_roof = np.array([840, 840, 900])
    c_roof = specificHeatCapacity(d_roof, 0.01, rho_roof, cp_roof)

    U_roof = 0.318

    R_se_op = [0.034, 0.034, 0.034, 0.034, 0.034, 0]  # Table 5.1, page 17
    R_se_w = [0.0476, 0.0476, 0.0476, 0.0476, 0.0476, 0]  # Table 5.6, page 19

    months = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
    monthsCum = np.cumsum(months)
    monthsCum0 = np.append(np.array([0]), monthsCum)
    T_aver_mon = []
    b_m = []  # Anpassungsfaktor ground p.44 ISO 13790

    for i in range(12):
        T_aver_mon = np.append(T_aver_mon,
                               sum(environment.weather.t_ambient[
                                   monthsCum0[i] * 24:monthsCum0[
                                                          i + 1] * 24]) /
                               months[i] / 24)
    T_i_year = 22.917
    # Heizperiode von Anfang Oktober bis Ende April
    for i in range(4):
        for k in range(months[i] * 24):
            b_m = np.append(b_m, (T_i_year - 9.71) / (20 - T_aver_mon[i]))
    for i in range(5):
        for k in range(months[4 + i] * 24):
            b_m = np.append(b_m, (T_i_year - 9.71) / (27 - T_aver_mon[4 + i]))
    for i in range(3):
        for k in range(months[9 + i] * 24):
            b_m = np.append(b_m, (T_i_year - 9.71) / (20 - T_aver_mon[9 + i]))

    # Abfangen von extrem großen/kleinen Korrekturfaktoren
    for i in range(8760):
        b_m[i] = np.minimum(b_m[i], 10)
        b_m[i] = np.maximum(b_m[i], -10)

    U_floor = 0.039

    U_floor_bm = np.multiply(U_floor, b_m)

    U_walls_ext_bm = [U_extWall, U_extWall, U_extWall, U_extWall, U_roof,
                      np.mean(U_floor_bm[i])]

    U_walls_ext_bm = []
    for i in range(8760):
        U_walls_ext_bm.append(np.array(
            [U_extWall, U_extWall, U_extWall, U_extWall, U_roof,
             U_floor_bm[i]]))  # air-air

    c = np.array([c_extWall, c_extWall, c_extWall, c_extWall, c_roof, c_floor])

    zone_parameters = zp.ZoneParameters(A_f=A_f,
                                       A_w=A_windows,
                                       U_w=U_windows,
                                       g_gln=g_gln,
                                       epsilon_w=infraredEmittance,
                                       R_se_w=R_se_w,
                                       A_op=A_walls,
                                       #                                   U_op=U_walls,
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
    ventilation = np.ones(
        timer.timesteps_total) * 0.5  # section 5.2.1.6, page 16

    ventilationFactor = 0.822  # Adjustment factor, see Table 5.2, page 18
    ventilation = ventilation * ventilationFactor  # Final adjustment factor, see
    # Footnote at Table 5.2, page 18
    zone_parameters.updateVentilation(ventilationRate=ventilation,
                                     ventilationRateMinimum=0.41)

    # Set points (section 5.2.1.13.1.1, page 19)
    T_set_heating = np.ones(timer.timesteps_total) * 20
    T_set_cooling = np.ones(timer.timesteps_total) * 27

    # Initialize T_m
    t_m_init = 20

    spaceHeating = sh.SpaceHeating(environment,
                                   method=2,
                                   zone_parameters=zone_parameters,
                                   t_m_init=t_m_init,
                                   appliances=internalGains,
                                   t_cooling_set=T_set_cooling,
                                   t_heating_set=T_set_heating)

    # Retrieve results
    Q_HC = spaceHeating.loadcurve
    solarOpaque = spaceHeating.zone_inputs.solar_opaque
    solarWindow = spaceHeating.zone_inputs.solar_window

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
                      solarGainsSouth=np.sum(solarOpaque[0]) / 1000,
                      # in kWh per m^2
                      solarGainsWest=np.sum(solarOpaque[1]) / 1000,
                      # in kWh per m^2
                      solarGainsNorth=np.sum(solarOpaque[2]) / 1000,
                      # in kWh per m^2
                      solarGainsEast=np.sum(solarOpaque[3]) / 1000,
                      # in kWh per m^2
                      solarGainsHorizontal=np.sum(solarOpaque[4]) / 1000,
                      # in kWh per m^2
                      solarGainsWindowSouth=np.sum(solarWindow[0]) / 1000,
                      # in kWh per m^2
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
    print("Heating peak time: " + str(
        transformTime(int(results.heatingPeakTime))))
    print("Reference: 04-Jan,5; 01-Jan,5; 01-Jan,2; 01-Jan,6")
    print()
    print()
    print("Cooling peak: " + str(round(results.coolingPeak, 3)))
    print("Reference: min: 5.965, max: 6.827, mean: 6.461")
    print("Cooling peak time: " + str(
        transformTime(int(results.coolingPeakTime))))
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
    print(
        "Solar gains horizontal: " + str(round(results.solarGainsHorizontal)))
    print("Reference: min: 1797, max: 1832, mean: 1827")
    print()
    print()
    print("Solar gains windows (South): " + str(round(
        results.solarGainsWindowSouth)))
    print("Reference: min: 914, max: 1051, mean: 962")

    if do_plot:
        plotCase600.plot_results(results)

        plotCase600.plot_west_surface(results)
        plotCase600.plot_south_surface(results)

        plotCase600.plot_january_4(results)


if __name__ == '__main__':
    run_validation(do_plot=True)
