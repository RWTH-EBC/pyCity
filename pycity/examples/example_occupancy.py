# coding=utf-8
"""
Example script for occupancy usage
"""

import matplotlib.pyplot as plt

import pycity.classes.Timer
import pycity.classes.Weather
import pycity.classes.Environment
import pycity.classes.Prices

import pycity.classes.demand.Occupancy as occup


def exampe_occupancy():
    timer = pycity.classes.Timer.Timer(timeDiscretization=600)
    weather = pycity.classes.Weather.Weather(timer)  # , useTRY=True)
    prices = pycity.classes.Prices.Prices()

    environment = pycity.classes.Environment.Environment(timer, weather,
                                                         prices)

    occupancy_object = pycity.classes.demand.Occupancy.Occupancy(environment,
                                                          number_occupants=3)

    print('Occupancy profile:')
    print(occupancy_object.occupancy)

    fig = plt.figure()
    plt.plot(occupancy_object.occupancy[:200])
    plt.ylabel('Occupancy')
    plt.show()

if __name__ == '__main__':
    #  Run program
    exampe_occupancy()