# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 14:10:10 2015

@author: tsz
"""

import classes.Timer

# Create a standard timer
standard_timer = classes.Timer.Timer()

# Create a modified timer
timeDiscretization = 3600
timestepsHorizon = 48
timestepsUsedHorizon = 24
timestepsTotal = 8760
modified_timer = classes.Timer.Timer(timeDiscretization, timestepsHorizon, timestepsUsedHorizon, timestepsTotal)

# Print results:
def print_results(timer):
    print("time discretization: " + str(timer.getTimeDiscretization()))
    print("number of timesteps in one horizon: " + str(timer.getTimestepsHorizon()))
    print("number of timesteps really used in the horizon: " + str(timer.getTimestepsUsedHorizon()))
    print("total number of time steps: " + str(timer.getTimestepsTotal()))

print
print("Values of the standard timer")
print_results(standard_timer)

print
print("Values of the modified timer")
print_results(modified_timer)