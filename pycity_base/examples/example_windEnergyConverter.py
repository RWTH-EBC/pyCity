#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 03 15:50:08 2015

@author: tsz
"""

from __future__ import division
import os
import pycity_base.classes.supply.WindEnergyConverter as WindEnergyConverter

import numpy as np
import matplotlib.pyplot as plt
import xlrd

import pycity_base.classes.Timer
import pycity_base.classes.Weather
import pycity_base.classes.Prices
import pycity_base.classes.Environment

def run_test(do_plot=False):
    # Create environment
    timer = pycity_base.classes.Timer.Timer()
    weather = pycity_base.classes.Weather.Weather(timer, useTRY=True)
    prices = pycity_base.classes.Prices.Prices()
    environment = pycity_base.classes.Environment.Environment(timer, weather, prices)

    # Create Wind Energy Converter (ENERCON E-126)
    src_path = os.path.dirname(os.path.dirname(__file__))
    wind_data_path = os.path.join(src_path, 'inputs', 'wind_energy_converters.xlsx')
    wecDatasheets = xlrd.open_workbook(wind_data_path)
    ENERCON_E_126 = wecDatasheets.sheet_by_name("ENERCON_E_126")
    hubHeight = ENERCON_E_126.cell_value(0,1)
    mapWind = []
    mapPower = []
    counter = 0
    while ENERCON_E_126._dimnrows > 3+counter:
        mapWind.append(ENERCON_E_126.cell_value(3+counter,0))
        mapPower.append(ENERCON_E_126.cell_value(3+counter,1))
        counter += 1

    mapWind = np.array(mapWind)
    mapPower = np.array(mapPower) * 1000

    wec = WindEnergyConverter.WindEnergyConverter(environment, mapWind,
                                                  mapPower, hubHeight)

    (currentWind,) = weather.getWeatherForecast(getVWind=True) # in m/s
    currentPower = wec.getPower() / 1000 # in kW

    if do_plot:
        # Plot wind and WEC power
        figure = plt.figure(figsize=(8,6))
        ax1 = plt.subplot(211)
        ax1.plot(list(range(environment.timer.timestepsHorizon)), currentWind)
        plt.xlim((0,environment.timer.timestepsHorizon-1))
        plt.ylim((0,12))
        plt.ylabel("Wind velocity in m/s", fontsize=12)
        ax2 = plt.subplot(212)
        ax2.plot(list(range(environment.timer.timestepsHorizon)), currentPower)
        plt.xlim((0,environment.timer.timestepsHorizon-1))
        plt.xlabel("Timesteps", fontsize=12)
        plt.ylabel("Electricity generation in kW", fontsize=12)
        plt.show()

if __name__ == '__main__':
    #  Run program
    run_test(do_plot=True)
