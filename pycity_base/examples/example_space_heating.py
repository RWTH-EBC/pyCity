#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example of the space heating class.
"""

from __future__ import division

import matplotlib.pyplot as plt

import pycity_base.classes.demand.space_heating as sh

import pycity_base.classes.timer
import pycity_base.classes.weather
import pycity_base.classes.environment
import pycity_base.classes.prices


def run_example(do_plot=False):
    timer = pycity_base.classes.timer.Timer()
    weather = pycity_base.classes.weather.Weather(timer, use_TRY=True)
    prices = pycity_base.classes.prices.Prices()

    environment = pycity_base.classes.environment.Environment(timer, weather, prices)

    #  Use standardized thermal load profile
    #  #---------------------------------------
    hd_slp = sh.SpaceHeating(environment,
                             method=1,  # Standard load profile
                             living_area=150,
                             specific_demand=100)

    results = hd_slp.get_power()

    print()
    print("Heat power curve: " + str(results))

    if do_plot:
        plt.plot(hd_slp.loadcurve, label="SLP [W]", color="b")
        plt.show()

    #  Use simulated profile
    #  #---------------------------------------
    sim_th_load = sh.SpaceHeating(environment,
                                  method=3,  # simulated profile
                                  living_area=150,
                                  specific_demand=100)

    sim_th_loadcurve = sim_th_load.loadcurve

    print('Thermal power load in W:', sim_th_loadcurve)

    if do_plot:
        plt.plot(sim_th_loadcurve, label="Simulated power curve [W]", color="b")
        plt.show()

        plt.plot(sim_th_loadcurve, label="Simulated power curve [W]")
        plt.plot(hd_slp.loadcurve, label="SLP [W]")
        plt.legend()
        plt.show()


if __name__ == '__main__':
    #  Run program
    run_example(do_plot=True)
