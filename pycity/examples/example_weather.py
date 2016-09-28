#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 11 14:12:12 2015

@author: tsz
"""

from __future__ import division

import pycity.classes.Timer
import pycity.classes.Weather


def run_test():
    time = pycity.classes.Timer.Timer()
    weather = pycity.classes.Weather.Weather(time, useTRY=True)

    (tamb, qdif, vw, phiamb, pamb) = weather.getWeatherForecast(
        getTAmbient=True,
        getQDirect=True,
        getQDiffuse=False,
        getVWind=True,
        getPhiAmbient=True,
        getPAmbient=True)

    print()
    print("Ambient temperature: " + str(tamb))
    print()
    print("Diffuse radiation: " +
          str(weather.getPreviousWeather(fromTimestep=0, getQDiffuse=True)))
    print()
    print(("Total radiation on a tilted surface: " +
           str((weather.getRadiationTiltedSurface(beta=30, gamma=45,
                                                  update=True))[0])))

    w2 = pycity.classes.Weather.Weather(time, useTRY=False, useTMY3=True)
    (tamb2, qdif2, vw2, phiamb2, pamb2) = w2.getWeatherForecast(
        getTAmbient=True,
        getQDirect=True,
        getQDiffuse=False,
        getVWind=True,
        getPhiAmbient=True,
        getPAmbient=True)


if __name__ == '__main__':
    #  Run program
    run_test()
