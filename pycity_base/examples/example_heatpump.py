#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 13:44:16 2015

@author: Thomas
"""

from __future__ import division
import os
import numpy as np

import pycity_base.classes.supply.HeatPump as HP

import pycity_base.classes.Timer
import pycity_base.classes.Weather
import pycity_base.classes.Prices
import pycity_base.classes.Environment

import xlrd

def run_test():
    # Create environment
    timer = pycity.classes.Timer.Timer()
    weather = pycity.classes.Weather.Weather(timer, useTRY=True)
    prices = pycity.classes.Prices.Prices()
    environment = pycity.classes.Environment.Environment(timer, weather, prices)

    #  Heatpump data path
    src_path = os.path.dirname(os.path.dirname(__file__))
    hp_data_path = os.path.join(src_path, 'inputs', 'heat_pumps.xlsx')
    heatpumpData = xlrd.open_workbook(hp_data_path)
    dimplex_LA12TU = heatpumpData.sheet_by_name("Dimplex_LA12TU")

    # Size of the worksheet
    number_rows = dimplex_LA12TU._dimnrows
    number_columns = dimplex_LA12TU._dimncols
    # Flow, ambient and max. temperatures
    tFlow = np.zeros(number_columns-2)
    tAmbient = np.zeros(int((number_rows-7)/2))
    tMax = dimplex_LA12TU.cell_value(0,1)

    firstRowCOP = number_rows - len(tAmbient)

    qNominal = np.empty((len(tAmbient), len(tFlow)))
    cop = np.empty((len(tAmbient), len(tFlow)))

    for i in range(number_columns-2):
        tFlow[i] = dimplex_LA12TU.cell_value(3, 2+i)

    for col in range(len(tFlow)):
        for row in range(len(tAmbient)):
            qNominal[row, col] = dimplex_LA12TU.cell_value(int(4+row),
                                                           int(2+col))
            cop[row, col] = dimplex_LA12TU.cell_value(int(firstRowCOP+row),
                                                      int(2+col))

    pNominal = qNominal / cop

    # Create HP
    lower_activation_limit = 0.5

    heater = HP.Heatpump(environment, tAmbient, tFlow, qNominal, pNominal, cop,
                         tMax, lower_activation_limit)

    # Print results
    print()
    print(("Type: " + heater._kind))
    print()
    print(("Maximum flow temperature: " + str(heater.tMax)))
    print(("Lower activation limit: "   + str(heater.lowerActivationLimit)))

    np.random.seed(0)
    flowTemperature = np.random.rand(timer.timestepsHorizon) * 20 + 35

    nominals = heater.getNominalValues(flowTemperature)
    print()
    print(("Nominal electricity consumption: " + str(nominals[0])))
    print(("Nominal heat output: " + str(nominals[1])))
    print(("Maximum flow temperature: " + str(nominals[2])))
    print(("Lower activation limit: "   + str(nominals[3])))

    schedule = np.random.randint(2, size=timer.timestepsUsedHorizon)
    result_p = (nominals[0])[0:96] * schedule
    result_q = (nominals[1])[0:96] * schedule

    heater.setResults(result_p, result_q, schedule)

    results = heater.getResults(True)
    print()
    print("Electricity input: " + str(results[0]))
    print()
    print("Heat output: " + str(results[1]))
    print()
    print("Schedule: " + str(results[2]))

if __name__ == '__main__':
    #  Run program
    run_test()
