#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example of the timer class.
"""

from __future__ import division
import pycity_base.classes.timer


def print_timer(time):
    print()
    print(("Time discretization: " + str(time.time_discretization)))
    print(("Time steps horizon: " + str(time.timesteps_horizon)))
    print(("Time steps used horizon: " + str(time.timesteps_used_horizon)))
    print(("Time steps total: " + str(time.timesteps_total)))
    print(("Current time step: " + str(time.current_timestep)))
    print(("Current day: " + str(time.current_day)))
    print(("Current weekday: " + str(time.current_weekday)))
    print(("Is the current day on a weekend? " + str(time.current_day_weekend)))


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
