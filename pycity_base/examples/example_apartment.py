#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to initialize apartment object and add heat, electrical and hot water
demand objects.
"""

from __future__ import division

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


def run_example(do_plot=False):
    timestep = 900  # in seconds

    nb_timesteps = int(365 * 24 * 3600 / timestep)

    #  Generate environment
    timer = time.Timer(time_discretization=timestep,
                       timesteps_total=nb_timesteps)
    weather = we.Weather(timer)
    prices = pr.Prices()
    environment = env.Environment(timer, weather, prices)

    #  Generate heat demand object
    heat_demand = sh.SpaceHeating(environment,
                                  method=1,  # Standard load profile
                                  living_area=146,
                                  specific_demand=166)

    #  Generate electrical demand object
    el_demand = ed.ElectricalDemand(environment,
                                    method=1,  # Standard load profile
                                    annual_demand=3000)

    #  Generate hot water demand object (based on Annex 42 profiles)
    dhw_annex42 = dhw.DomesticHotWater(environment,
                                       t_flow=60,
                                       thermal=True,
                                       method=1,  # Annex 42
                                       daily_consumption=70,
                                       supply_temperature=25)
    #  Annotation: The usage of the deterministic IEA Annex 42 hot water
    #  profile is fine for a single apartment. However, try to use stochastic
    #  dhw profiles (method = 2 --> Requires occupancy input profile) on
    #  city district scale. The usage of Annex 42 profiles on city district
    #  scale will produce illogical peak loads / peak loads at the same point
    #  in time!

    #  Initialize apartment object
    apartment = ap.Apartment(environment=environment,
                             net_floor_area=80,  # Net floor area in m^2
                             occupancy=None)  # Occupants object (optional)

    #  Add entities to apartment object
    entities = [heat_demand, el_demand, dhw_annex42]
    apartment.addMultipleEntities(entities)

    #  Get space heating power curve for whole year:
    array_sh_power = apartment.get_space_heating_power_curve(currentValues=False)

    #  Get electrical power curve for whole year:
    array_el_power = apartment.get_el_power_curve(currentValues=False)

    #  Get domestic hot water power curve for whole year:
    array_dhw_power = apartment.get_dhw_power_curve(currentValues=False)

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
