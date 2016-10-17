#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 13 11:01:43 2015

@author: tsz
env."""

from __future__ import division
import pycity.classes.Timer
import pycity.classes.Weather
import pycity.classes.Prices
import pycity.classes.Environment

def run_test():
    timer = pycity.classes.Timer.Timer()
    weather = pycity.classes.Weather.Weather(timer, useTRY=True)
    prices = pycity.classes.Prices.Prices()
    env = pycity.classes.Environment.Environment(timer, weather, prices)

    def printResults(env):
        print(("Current timestep: " + str(env.timer.currentTimestep)))
        print(("Ambient temperature for entire horizon: " +
              str(env.weather.getWeatherForecast(getTAmbient=True))))

    print()
    print("Original environment (0 horizons passed)")
    printResults(env)

    env.update()
    print()
    print("Updated environment (1 horizon passed)")
    printResults(env)

if __name__ == '__main__':
    #  Run program
    run_test()