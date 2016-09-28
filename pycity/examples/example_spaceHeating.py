#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 11:29:11 2015

@author: tsz
"""

from __future__ import division
import matplotlib.pyplot as plt

import pycity.classes.demand.SpaceHeating as SpaceHeating

import pycity.classes.Timer
import pycity.classes.Weather
import pycity.classes.Environment
import pycity.classes.Prices


def run_test():
    timer = pycity.classes.Timer.Timer()
    weather = pycity.classes.Weather.Weather(timer, useTRY=True)
    prices = pycity.classes.Prices.Prices()

    environment = pycity.classes.Environment.Environment(timer, weather,
                                                         prices)

    #  Use standardized thermal load profile
    #  #---------------------------------------
    hd_slp = SpaceHeating.SpaceHeating(environment,
                                       method=1,  # Standard load profile
                                       livingArea=150,
                                       specificDemand=100)

    results = hd_slp.get_power()

    print()
    print("Heat power curve: " + str(results))

    plt.plot(hd_slp.loadcurve, label="SLP", color="b")
    plt.show()

    #  Use simulated profile
    #  #---------------------------------------
    sim_th_load = SpaceHeating.SpaceHeating(environment, method=3,
                                            # Sim profile
                                            livingArea=150,
                                            specificDemand=100)

    sim_th_loadcurve = sim_th_load.loadcurve

    print('Thermal power load in W:', sim_th_loadcurve)
    plt.plot(sim_th_loadcurve, label="Simulated power curve", color="b")
    plt.show()

    plt.plot(sim_th_loadcurve, label="Simulated power curve")
    plt.plot(hd_slp.loadcurve, label="SLP")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    #  Run program
    run_test()
