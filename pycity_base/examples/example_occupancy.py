# coding=utf-8
"""
Example script for occupancy usage.
"""

import numpy as np
import matplotlib.pyplot as plt

import pycity_base.classes.timer
import pycity_base.classes.weather
import pycity_base.classes.environment
import pycity_base.classes.prices

import pycity_base.classes.demand.occupancy


def run_example(do_plot=False):
    time_discretization = 60
    timer = pycity_base.classes.timer.Timer(
        time_discretization=time_discretization,
        timesteps_total=int(8760 * 3600 / time_discretization)
    )
    weather = pycity_base.classes.weather.Weather(timer)
    prices = pycity_base.classes.prices.Prices()

    environment = pycity_base.classes.environment.Environment(timer, weather, prices)

    occupancy_object = pycity_base.classes.demand.occupancy.Occupancy(
        environment,
        number_occupants=1
    )
    occupancy_profile = occupancy_object.occupancy
    print('Occupancy profile:')
    print(occupancy_profile)

    print('Maximum number of occupants:')
    print(np.max(occupancy_profile))

    counter = 0
    for i in range(len(occupancy_profile)):
        if occupancy_profile[i] == 1:
            counter += 1
    print('Number of timesteps in year, in which one person is inside the apartment:')
    print(counter)
    print('Time share per year, in which one person is inside the apartment:')
    print(counter / len(occupancy_profile))
    print()

    print('Return occupancy profile with adjusted timestep of 3600 seconds'
          '(without integer conversion):')
    occ_profile = \
        occupancy_object.get_occ_profile_in_curr_timestep(timestep=3600,
                                                          int_con=False)
    print(occ_profile)
    print()

    print('Return occupancy profile with adjusted timestep of 3600 seconds'
          '(with integer conversion):')
    occ_profile = \
        occupancy_object.get_occ_profile_in_curr_timestep(timestep=3600,
                                                          int_con=True)
    print(occ_profile)
    print()

    if do_plot:
        plt.figure()
        plt.plot(occupancy_object.occupancy[:200])
        plt.ylabel('Occupancy')
        plt.show()


if __name__ == '__main__':
    #  Run program
    run_example(do_plot=True)
