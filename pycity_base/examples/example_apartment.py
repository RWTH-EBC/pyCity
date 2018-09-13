#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to initialize apartment object and add heat, electrical and hot water
demand objects
"""

from __future__ import division

import numpy as np
import matplotlib.pyplot as plt

import pycity_base.classes.Timer as Time
import pycity_base.classes.Weather as Weath
import pycity_base.classes.Prices as Price
import pycity_base.classes.Environment as Env
import pycity_base.classes.demand.Apartment as Apartment
import pycity_base.classes.demand.DomesticHotWater as DomesticHotWater
import pycity_base.classes.demand.ElectricalDemand as ElectricalDemand
import pycity_base.classes.demand.SpaceHeating as SpaceHeating


def run_test(do_plot=False):
    timestep = 900  # in seconds

    nb_timesteps = int(365 * 24 * 3600 / timestep)

    #  Generate environment
    timer = Time.Timer(timeDiscretization=timestep,
                       timestepsTotal=nb_timesteps)
    weather = Weath.Weather(timer)
    prices = Price.Prices()
    environment = Env.Environment(timer, weather, prices)

    #  Generate heat demand object
    heat_demand = SpaceHeating.SpaceHeating(environment,
                                            method=1,  # Standard load profile
                                            livingArea=146,
                                            specificDemand=166)

    #  Generate electrical demand object
    el_demand = ElectricalDemand.ElectricalDemand(environment,
                                                  method=1,
                                                  # Standard load profile
                                                  annualDemand=3000)

    #  Generate hot water demand object (based on Annex 42 profiles)
    dhw_annex42 = DomesticHotWater.DomesticHotWater(environment,
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
    apartment = Apartment.Apartment(environment=environment,
                                    net_floor_area=80,  #  Net floor area in m2
                                    occupancy=None)
                                    #  Occuants object (optional)

    #  Add entities to apartment object
    entities = [heat_demand, el_demand, dhw_annex42]
    apartment.addMultipleEntities(entities)

    #  Get space heating power curve for whole year:
    array_sh_power = apartment.get_space_heat_power_curve(current_values=False)

    #  Get electrical power curve for whole year:
    array_el_power = apartment.get_el_power_curve(current_values=False)

    #  Get domestic hot water power curve for whole year:
    array_dhw_power = apartment.get_dhw_power_curve(current_values=False)

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
    run_test(do_plot=True)