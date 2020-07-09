#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example of the space cooling class.
"""

from __future__ import division

import numpy as np
import matplotlib.pyplot as plt

import pycity_base.classes.demand.space_cooling as sc
import pycity_base.classes.demand.space_heating as sh

import pycity_base.classes.timer
import pycity_base.classes.weather
import pycity_base.classes.environment
import pycity_base.classes.prices


def run_example(do_plot=False):
    timer = pycity_base.classes.timer.Timer(time_discretization=900,
                                            timesteps_horizon=35040,
                                            timesteps_used_horizon=35040,
                                            timesteps_total=35040,
                                            initial_day=1)
    weather = pycity_base.classes.weather.Weather(timer, use_TRY=True)
    prices = pycity_base.classes.prices.Prices()

    environment = pycity_base.classes.environment.Environment(timer, weather, prices)

    #  Use standardized thermal load profile for space heating and then 'convert' it to a cooling load (inverted load).
    #  #---------------------------------------
    hd_slp = sh.SpaceHeating(environment,
                             method=1,  # Standard load profile
                             living_area=150,
                             specific_demand=50)

    cd_slp = sc.SpaceCooling(environment,
                             method=0,
                             loadcurve=np.ones(environment.timer.timesteps_total)*max(hd_slp.get_power()) - hd_slp.
                             get_power())

    results = cd_slp.get_power()

    print()
    print("Cooling power curve: " + str(results))

    if do_plot:
        plt.plot(cd_slp.get_power(), label="Cooling Power [W]", color="b")
        plt.show()


if __name__ == '__main__':
    #  Run program
    run_example(do_plot=True)
