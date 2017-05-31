# coding=utf-8
"""
Example script for occupancy usage
"""

import numpy as np
import matplotlib.pyplot as plt

import pycity.classes.Timer
import pycity.classes.Weather
import pycity.classes.Environment
import pycity.classes.Prices

import pycity.classes.demand.occupancy as occ


def exampe_occupancy():
    time_discretization = 60
    timer = pycity.classes.Timer.Timer(timeDiscretization=time_discretization,
                                 timestepsTotal=int(8760*3600/time_discretization))
    weather = pycity.classes.Weather.Weather(timer)  # , useTRY=True)
    prices = pycity.classes.Prices.Prices()
    
    environment = pycity.classes.Environment.Environment(timer, weather,
                                                         prices)
    
    occupancy_object = occ.Occupancy(environment, number_occupants=1)
    occupancy_profile = occupancy_object.occupancy
    print('Occupancy profile:')
    print(occupancy_profile)
    
    print('Maximum number of occupants:')
    print(np.max(occupancy_profile))
    
    counter = 0
    for i in range(len(occupancy_profile)):
        if occupancy_profile[i] == 1:
            counter += 1
    print('Number of timesteps in year, when 1 person is within apartment:')
    print(counter)
    print('Time share per year, when one person is within apartment:')
    print(counter/len(occupancy_profile))
    
    plt.figure()
    plt.plot(occupancy_object.occupancy[:200])
    plt.ylabel('Occupancy')
    plt.show()

if __name__ == '__main__':
    #  Run program
    exampe_occupancy()