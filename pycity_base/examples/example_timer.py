#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example of the timer class.
"""

from __future__ import division
import pycity_base.classes.timer


def print_timer(time):
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


def run_example():

    timer = pycity_base.classes.timer.Timer()

    print_timer(timer)

    timer.reinit(1, 2, 3, 4, 5)
    print_timer(timer)

    timer.update()
    print_timer(timer)


if __name__ == '__main__':
    #  Run program
    run_example()
