"""
Script to generate city district
"""

from __future__ import division
import sys
import os
import numpy as np
import pickle

import sympy.geometry.point as point

import pycity.classes.Timer
import pycity.classes.Weather
import pycity.classes.Prices
import pycity.classes.Environment

import pycity.classes.demand.Apartment as Apartment
import pycity.classes.demand.DomesticHotWater as DomesticHotWater
import pycity.classes.demand.ElectricalDemand as ElectricalDemand
import pycity.classes.demand.SpaceHeating as SpaceHeating
import pycity.classes.HeatingCurve as HeatingCurve
import pycity.classes.Building as Building
import pycity.classes.CityDistrict as CityDistrict

import pycity.classes.supply.PV as PV


def run_city_generator():

    #  Generate timer, weather and price objects
    timer = pycity.classes.Timer.Timer()
    weather = pycity.classes.Weather.Weather(timer)
    prices = pycity.classes.Prices.Prices()

    #  Generate environment
    environment = pycity.classes.Environment.Environment(timer, weather, prices)



if __name__ == '__main__':

    #  User inputs  #########################################################################

    #  Choose generation mode
    #  0 - Use csv/txt input to generate city district
    generation_mode = 0

    #  Define input data filename
    filename = 'test_data.txt'
    #  filename = 'wm_total_input.txt'

    #  Define ouput data filename (pickled city object)
    pickle_city_filename = 'myCity.p'

    run_city_generator()
