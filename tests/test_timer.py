#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 22:20:15 2015

@author: Thomas
"""

from __future__ import division
import classes.Timer


timer = classes.Timer.Timer()

def printTimer(time):
    print()
    print(("Time discretization: " + str(time.timeDiscretization)))
    print(("Time steps horizon: " + str(time.timestepsHorizon)))
    print(("Time steps used horizon: " + str(time.timestepsUsedHorizon)))
    print(("Time steps total: " + str(time.timestepsTotal)))
    print(("Current time step: " + str(time.currentTimestep)))
    print(("Current optimization period: " + str(time.currentOptimizationPeriod)))
    print(("Current day: " + str(time.currentDay)))
    print(("Current weekday: " + str(time.currentWeekday)))
    print(("Is the current day on a weekend? " + str(time.currentDayWeekend)))
    
printTimer(timer)

timer.reinit(1, 2, 3, 4, 5)
printTimer(timer)

timer.update()
printTimer(timer)