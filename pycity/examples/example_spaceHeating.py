#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 11:29:11 2015

@author: tsz
"""

from __future__ import division

import pycity.classes.demand.SpaceHeating as SpaceHeating

import pycity.classes.Timer
import pycity.classes.Weather
import pycity.classes.Environment
import pycity.classes.Prices

def run_test():
    timer = pycity.classes.Timer.Timer()
    weather = pycity.classes.Weather.Weather(timer, useTRY=True)
    prices = pycity.classes.Prices.Prices()

    environment = pycity.classes.Environment.Environment(timer, weather, prices)

    hd_slp = SpaceHeating.SpaceHeating(environment,
                                       method=1, # Standard load profile
                                       livingArea=146,
                                       specificDemand=166)

    results = hd_slp.get_power()

    print()
    print("Heat demand: " + str(results))

    import matplotlib.pyplot as plt
    plt.plot(hd_slp.loadcurve, label="SLP", color="b")

if __name__ == '__main__':
    #  Run program
    run_test()
