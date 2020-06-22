#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example of the weather class.
"""

from __future__ import division

import os
import numpy as np
import matplotlib.pylab as plt
import pycity_base.classes.timer
import pycity_base.classes.weather


def run_example_simple():
    time = pycity_base.classes.timer.Timer()
    weather = pycity_base.classes.weather.Weather(time, use_TRY=True)

    (tamb, qdif, vw, phiamb, pamb) = weather.getWeatherForecast(getTAmbient=True,
                                                                getQDirect=True,
                                                                getQDiffuse=False,
                                                                getVWind=True,
                                                                getPhiAmbient=True,
                                                                getPAmbient=True)

    print()
    print("Ambient temperature: " + str(tamb))
    print()
    print("Diffuse radiation: " + str(weather.getPreviousWeather(fromTimestep=0,
                                                                 getQDiffuse=True)))
    print()
    print(("Total radiation on a tilted surface: " +
           str((weather.getRadiationTiltedSurface(beta=30, gamma=45,
                                                  update=True))[0])))

    w2 = pycity_base.classes.weather.Weather(time, use_TRY=False, use_TMY3=True)
    (tamb2, qdif2, vw2, phiamb2, pamb2) = w2.getWeatherForecast(getTAmbient=True,
                                                                getQDirect=True,
                                                                getQDiffuse=False,
                                                                getVWind=True,
                                                                getPhiAmbient=True,
                                                                getPAmbient=True)


def run_example_advanced(do_plot=True):
    #  Define source path
    src_path = os.path.dirname(os.path.dirname(__file__))

    #  Initialize timer object
    timer = pycity_base.classes.timer.Timer(time_discretization=3600)

    #  Initialize default weather object
    weather = pycity_base.classes.weather.Weather(timer=timer)

    print('Outdoor temperature in degree Celsius:')
    print(weather.t_ambient)

    path_try_cold = os.path.join(src_path,
                                 'inputs',
                                 'weather',
                                 'TRY2010_05_Wint.dat')

    #  Initialize cold weather object
    weather_cold = pycity_base.classes.weather.Weather(timer=timer, path_TRY=path_try_cold)

    path_try_warm = os.path.join(src_path,
                                 'inputs',
                                 'weather',
                                 'TRY2010_05_Somm.dat')

    #  Initialize warm weather object
    weather_warm = pycity_base.classes.weather.Weather(timer=timer, path_TRY=path_try_warm)

    print('Average temperature TRY regular (2010) in degree Celsius:')
    print(np.mean(weather.t_ambient))
    print()
    print('Average temperature TRY cold (2010) in degree Celsius:')
    print(np.mean(weather_cold.t_ambient))
    print()
    print('Average temperature TRY warm (2010) in degree Celsius:')
    print(np.mean(weather_warm.t_ambient))
    print()

    print('Average direct + diffuse radiation TRY regular (2010) in kW/m^2:')
    print(np.mean(weather.q_direct + weather.q_diffuse))
    print()
    print('Average direct + diffuse radiation TRY cold (2010) in kW/m^2:')
    print(np.mean(weather_cold.q_direct + weather_cold.q_diffuse))
    print()
    print('Average direct + diffuse radiation TRY warm (2010) in kW/m^2:')
    print(np.mean(weather_warm.q_direct + weather_warm.q_diffuse))
    print()

    if do_plot:
        fig1 = plt.figure()
        plt.plot(weather.t_ambient, label='TRY regular (2010)')
        plt.plot(weather_cold.t_ambient, label='TRY cold (2010)')
        plt.plot(weather_warm.t_ambient, label='TRY warm (2010)')
        plt.xlabel('Time in hours')
        plt.ylabel('Outdoor temperature\nin degree Celsius')
        plt.legend()
        plt.show()
        plt.close()

        fig2 = plt.figure()
        plt.plot(weather.q_direct + weather.q_diffuse, label='TRY regular (2010)')
        plt.plot(weather_cold.q_direct + weather_cold.q_diffuse,
                 label='TRY cold (2010)')
        plt.plot(weather_warm.q_direct + weather_warm.q_diffuse,
                 label='TRY warm (2010)')
        plt.xlabel('Time in hours')
        plt.ylabel('Outdoor temperature\nin degree Celsius')
        plt.legend()
        plt.show()
        plt.close()

    #  2035 TRY
    #  #########################################

    path_try = os.path.join(src_path,
                            'inputs',
                            'weather',
                            'TRY2035_05_Jahr.dat')

    #  Initialize weather object
    weather = pycity_base.classes.weather.Weather(timer=timer, path_TRY=path_try)

    path_try_cold = os.path.join(src_path,
                                 'inputs',
                                 'weather',
                                 'TRY2035_05_Wint.dat')

    #  Initialize cold weather object
    weather_cold = pycity_base.classes.weather.Weather(timer=timer, path_TRY=path_try_cold)

    path_try_warm = os.path.join(src_path,
                                 'inputs',
                                 'weather',
                                 'TRY2035_05_Somm.dat')

    #  Initialize warm weather object
    weather_warm = pycity_base.classes.weather.Weather(timer=timer, path_TRY=path_try_warm)

    print('Average temperature TRY regular (2035) in degree Celsius:')
    print(np.mean(weather.t_ambient))
    print()
    print('Average temperature TRY cold (2035) in degree Celsius:')
    print(np.mean(weather_cold.t_ambient))
    print()
    print('Average temperature TRY warm (2035) in degree Celsius:')
    print(np.mean(weather_warm.t_ambient))
    print()

    print('Average direct + diffuse radiation TRY regular (2035) in kW/m^2:')
    print(np.mean(weather.q_direct + weather.q_diffuse))
    print()
    print('Average direct + diffuse radiation TRY cold (2035) in kW/m^2:')
    print(np.mean(weather_cold.q_direct + weather_cold.q_diffuse))
    print()
    print('Average direct + diffuse radiation TRY warm (2035) in kW/m^2:')
    print(np.mean(weather_warm.q_direct + weather_warm.q_diffuse))
    print()

    if do_plot:
        fig3 = plt.figure()
        plt.plot(weather.t_ambient, label='TRY regular (2035)')
        plt.plot(weather_cold.t_ambient, label='TRY cold (2035)')
        plt.plot(weather_warm.t_ambient, label='TRY warm (2035)')
        plt.xlabel('Time in hours')
        plt.ylabel('Outdoor temperature\nin degree Celsius')
        plt.legend()
        plt.show()
        plt.close()

        fig4 = plt.figure()
        plt.plot(weather.q_direct + weather.q_diffuse, label='TRY regular (2035)')
        plt.plot(weather_cold.q_direct + weather_cold.q_diffuse,
                 label='TRY cold (2035)')
        plt.plot(weather_warm.q_direct + weather_warm.q_diffuse,
                 label='TRY warm (2035)')
        plt.xlabel('Time in hours')
        plt.ylabel('Outdoor temperature\nin degree Celsius')
        plt.legend()
        plt.show()
        plt.close()


def run_example():
    run_example_simple()
    run_example_advanced(do_plot=False)


if __name__ == '__main__':
    #  Run program
    run_example_simple()
    run_example_advanced()
