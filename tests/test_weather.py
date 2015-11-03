#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 11 14:12:12 2015

@author: tsz
"""

import classes.Timer
import classes.Weather

time = classes.Timer.Timer()
weather = classes.Weather.Weather(time, useTRY=True)

(tamb, qdif, vw, phiamb, pamb) = weather.getWeatherForecast(getTAmbient=True,
                                                            getQDirect=True,
                                                            getQDiffuse=False,
                                                            getVWind=True,
                                                            getPhiAmbient=True,
                                                            getPAmbient=True)

print 
print "Ambient temperature: " + str(tamb)
print
print "Diffuse radiation: " + str(weather.getPreviousWeather(fromTimestep=0, 
                                                             getQDiffuse=True))
print
print ("Total radiation on a tilted surface: " + 
       str((weather.getRadiationTiltedSurface(beta=30, gamma=45, 
                                              update=True))[0]))