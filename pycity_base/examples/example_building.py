#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example of the building class.
"""

from __future__ import division

import os
import xlrd
import numpy as np
import matplotlib.pyplot as plt

import pycity_base.classes.timer as time
import pycity_base.classes.weather as we
import pycity_base.classes.prices as pr
import pycity_base.classes.environment as env
import pycity_base.classes.demand.apartment as ap
import pycity_base.classes.demand.domestic_hot_water as dhw
import pycity_base.classes.demand.electrical_demand as ed
import pycity_base.classes.demand.space_heating as sh
import pycity_base.classes.supply.building_energy_system as build_es
import pycity_base.classes.supply.heat_pump as hp
import pycity_base.classes.heating_curve as hc
import pycity_base.classes.building as build


def run_example(do_plot=False):
    timestep = 900  # in seconds

    nb_timesteps = int(365 * 24 * 3600 / timestep)

    #  Generate environment with timer, weather, and prices objects
    timer = time.Timer(timeDiscretization=timestep,
                       timestepsTotal=nb_timesteps)
    weather = we.Weather(timer)
    prices = pr.Prices()
    environment = env.Environment(timer, weather, prices)

    heat_demand = sh.SpaceHeating(environment,
                                  method=1,  # Standard load profile
                                  livingArea=146,
                                  specificDemand=166)

    el_demand = ed.ElectricalDemand(environment,
                                    method=1,  # Standard load profile
                                    annualDemand=3000)

    dhw_annex42 = dhw.DomesticHotWater(environment,
                                       tFlow=60,
                                       thermal=True,
                                       method=1,  # Annex 42
                                       dailyConsumption=70,
                                       supplyTemperature=25)
    #  Annotation: The usage of the deterministic IEA Annex 42 hot water
    #  profile is fine for a single apartment. However, try to use stochastic
    #  dhw profiles (method = 2 --> Requires occupancy input profile) on
    #  city district scale. The usage of Annex 42 profiles on city district
    #  scale will produce illogical peak loads / peak loads at the same point
    #  in time!

    #  Initialize apartment object
    apartment = ap.Apartment(environment=environment,
                             net_floor_area=120,  # Net floor area in m^2
                             occupancy=None)
    #  Occuants object (optional)

    #  Add heat demand as entity to apartment
    apartment.addEntity(heat_demand)

    #  Add multiple entities (el_demand, dhw_annex2) to apartment object
    apartment.addMultipleEntities([el_demand, dhw_annex42])

    #  Heatpump data path
    src_path = os.path.dirname(os.path.dirname(__file__))
    hp_data_path = os.path.join(src_path, 'inputs', 'heat_pumps.xlsx')
    heatpumpData = xlrd.open_workbook(hp_data_path)
    dimplex_LA12TU = heatpumpData.sheet_by_name("Dimplex_LA12TU")

    # Size of the worksheet
    number_rows = dimplex_LA12TU._dimnrows
    number_columns = dimplex_LA12TU._dimncols

    # Flow, ambient and max. temperatures
    tFlow = np.zeros(number_columns - 2)
    tAmbient = np.zeros(int((number_rows - 7) / 2))
    tMax = dimplex_LA12TU.cell_value(0, 1)

    firstRowCOP = number_rows - len(tAmbient)

    qNominal = np.empty((len(tAmbient), len(tFlow)))
    cop = np.empty((len(tAmbient), len(tFlow)))

    for i in range(number_columns - 2):
        tFlow[i] = dimplex_LA12TU.cell_value(3, 2 + i)

    for col in range(len(tFlow)):
        for row in range(len(tAmbient)):
            qNominal[row, col] = dimplex_LA12TU.cell_value(int(4 + row),
                                                           int(2 + col))
            cop[row, col] = dimplex_LA12TU.cell_value(int(firstRowCOP + row),
                                                      int(2 + col))

    pNominal = qNominal / cop

    # Create HP
    lower_activation_limit = 0.5

    #  Generate complex heat pump energy system object
    heatpump = hp.Heatpump(environment, tAmbient, tFlow, qNominal, pNominal, cop, tMax, lower_activation_limit)

    #  Generate building energy system (BES) object instance
    bes = build_es.BES(environment)

    #  Add heat pump object to BES
    bes.addDevice(heatpump)

    #  Generate heating curve object for building
    heatingCurve = hc.HeatingCurve(environment)

    #  Generate building object instance
    building = build.Building(environment)

    #  Add entities to building object
    entities = [apartment, bes, heatingCurve]
    building.addMultipleEntities(entities)

    print('Access heat pump nominals:')
    print(building.getHeatpumpNominals())
    print()

    print('Access flow temperatures:')
    print(building.flowTemperature)
    print()

    print('Get number of apartments:')
    print(building.get_number_of_apartments())

    print('Get net floor area of building in m^2:')
    print(building.get_net_floor_area_of_building())

    #  Get space heating power curve for whole year:
    array_sh_power = building.get_space_heating_power_curve()

    #  Get electrical power curve for whole year:
    array_el_power = building.get_electric_power_curve()

    #  Get domestic hot water power curve for whole year:
    array_dhw_power = building.get_dhw_power_curve()

    #  Generate time array (in days)
    array_time = np.arange(start=0, stop=int(nb_timesteps * timestep),
                           step=timestep) / (3600 * 24)

    if do_plot:
        fig = plt.figure()
        fig.add_subplot(311)
        plt.plot(array_time, array_sh_power)
        plt.xlabel('Time in days')
        plt.ylabel('Space heating\npower in Watt')

        fig.add_subplot(312)
        plt.plot(array_time, array_el_power)
        plt.xlabel('Time in days')
        plt.ylabel('Electric\npower in Watt')

        fig.add_subplot(313)
        plt.plot(array_time, array_dhw_power)
        plt.xlabel('Time in days')
        plt.ylabel('DHW power\nin Watt')

        plt.show()
        plt.close()


if __name__ == '__main__':
    #  Run program
    run_example(do_plot=True)
