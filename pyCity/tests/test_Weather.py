# -*- coding: utf-8 -*-
"""
Created on Wed Feb 11 14:12:12 2015

@author: tsz
"""

import classes.Timer
import classes.Weather

time = classes.Timer.Timer()

pathTRY = "inputs\\weather\\TRY2011\\TRY2010_01_Jahr.dat"
weather = classes.Weather.Weather(time, pathTRY=pathTRY, useTRY=True)

#(tamb, qdir, qdif, vw, phiamb, pamb) = weather.getWeatherForecast(True, True, True, True, True, True)
(tamb, qdif, vw, phiamb, pamb) = weather.getWeatherForecast(True, True, False, True, True, True)

print 
print "Ambient temperature: " + str(tamb)
