#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example of the photovoltaic (PV) class.
"""

from __future__ import division

import os
import pycity_base.classes.supply.photovoltaic as pv

import numpy as np
import matplotlib.pyplot as plt
import xlrd

import pycity_base.classes.timer
import pycity_base.classes.weather
import pycity_base.classes.prices
import pycity_base.classes.environment


def run_example(do_plot=False):
    # Create environment
    timer = pycity_base.classes.timer.Timer()
    timer.reinit(3600, 8760, 8760, 8760, 0, True)
    weather = pycity_base.classes.weather.Weather(timer)
    prices = pycity_base.classes.prices.Prices()
    environment = pycity_base.classes.environment.Environment(timer, weather, prices)

    # Create PV
    src_path = os.path.dirname(os.path.dirname(__file__))
    pv_data_path = os.path.join(src_path, 'inputs', 'photovoltaic_modules.xlsx')
    pv_data = xlrd.open_workbook(pv_data_path)
    sw_290 = pv_data.sheet_by_name("SolarWorld_SW290")
    area = sw_290.cell_value(1, 2)  # m^2, 1 module
    eta = sw_290.cell_value(6, 2)
    t_cell = sw_290.cell_value(7, 2)
    alpha = sw_290.cell_value(8, 2)

    beta = 0  # Slope of the PV unit

    pv_simple = pv.PV(environment=environment, method=0, area=area, eta_noct=eta, beta=beta)
    pv_detailed = pv.PV(environment=environment, method=0, area=area, eta_noct=eta, t_cell_noct=t_cell,
                        alpha_noct=alpha, beta=beta)

    pvPower_simple = pv_simple.getPower()
    pvPower_detailed = pv_detailed.getPower()

    # Print results
    print()
    print(("Efficiency: " + str(pv_detailed.eta_noct)))
    print(("Area: " + str(pv_detailed.area)))
    print(("Cell temperature: " + str(pv_detailed.t_cell_noct)))
    print(("Loss coefficient: " + str(pv_detailed.alpha_noct)))

    print(("Nominal values: " + str(pv_detailed.getNominalValues())))

    print()
    print(("PV power (simple model): " + np.str(pvPower_simple)))
    print()
    print(("PV power (detailed model): " + np.str(pvPower_detailed)))

    if do_plot:
        # Plot PV power
        plot_time = list(range(environment.timer.timesteps_horizon))
        figure = plt.figure(figsize=(6, 6))
        from matplotlib import gridspec
        gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1])
        ax0 = plt.subplot(gs[0])
        ax0.plot(plot_time, pvPower_detailed, label="PV electricity (detailed)")
        ax0.plot(plot_time, pvPower_simple,   label="PV electricity (simple)")
        plt.ylabel("Power [W]", fontsize=12)
        plt.xlim((0, environment.timer.timesteps_horizon-1))
        plt.title("Simplified vs. Detailed PV Model")

        ax1 = plt.subplot(gs[1], sharex=ax0)
        ax1.plot(plot_time, pvPower_detailed - pvPower_simple)
        plt.xlabel("Time", fontsize=12)
        plt.ylabel("Error")
        plt.show()

    pv_area = pv.PV(environment=environment, method=0, area=area, eta_noct=eta, t_cell_noct=t_cell,
                    alpha_noct=alpha, beta=beta)
    pv_kWp = pv.PV(environment=environment, method=1, peak_power=0.25, eta_noct=eta, t_cell_noct=t_cell,
                   alpha_noct=alpha, beta=beta)

    pvPower_area = pv_area.getPower()
    pvPower_kWp = pv_kWp.getPower()

    print()
    print(("PV power (based on area model): " + np.str(pvPower_area)))
    print()
    print(("PV power (based on peak power model): " + np.str(pvPower_kWp)))

    if do_plot:
        # Plot PV power
        plot_time = list(range(environment.timer.timesteps_horizon))
        figure = plt.figure(figsize=(6, 6))
        from matplotlib import gridspec
        gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1])
        ax0 = plt.subplot(gs[0])
        ax0.plot(plot_time, pvPower_area, label="PV electricity (based on area)")
        ax0.plot(plot_time, pvPower_kWp,   label="PV electricity (based on peak power)")
        plt.ylabel("Power [W]", fontsize=12)
        plt.xlim((0, environment.timer.timesteps_horizon-1))
        plt.title("Area vs. Peak Power PV Model")

        ax1 = plt.subplot(gs[1], sharex=ax0)
        ax1.plot(plot_time, pvPower_area - pvPower_kWp)
        plt.xlabel("Time", fontsize=12)
        plt.ylabel("Error")
        plt.show()


if __name__ == '__main__':
    #  Run program
    run_example(do_plot=True)
