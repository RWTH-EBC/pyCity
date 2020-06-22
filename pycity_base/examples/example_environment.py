#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example of the environment class.
"""

from __future__ import division

import pycity_base.classes.timer
import pycity_base.classes.weather
import pycity_base.classes.prices
import pycity_base.classes.environment


def run_example():
    timer = pycity_base.classes.timer.Timer()
    weather = pycity_base.classes.weather.Weather(timer, use_TRY=True)
    prices = pycity_base.classes.prices.Prices()
    env = pycity_base.classes.environment.Environment(timer, weather, prices)

    def print_results(e):
        print(("Current timestep: " + str(e.timer.current_timestep)))
        print(("Ambient temperature for entire horizon: " +
              str(e.weather.getWeatherForecast(getTAmbient=True))))

    print()
    print("Original environment (0 horizons passed)")
    print_results(env)

    env.update()
    print()
    print("Updated environment (1 horizon passed)")
    print_results(env)


if __name__ == '__main__':
    #  Run program
    run_example()
