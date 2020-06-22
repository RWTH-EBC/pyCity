#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example of the domestic hot water (DHW) class.
"""

from __future__ import division

import numpy as np
import matplotlib.pyplot as plt

import pycity_base.classes.demand.domestic_hot_water as dhw

import pycity_base.classes.timer
import pycity_base.classes.weather
import pycity_base.classes.environment
import pycity_base.classes.prices
import pycity_base.classes.demand.occupancy


def run_example(do_plot=False):
    time_discretization = 3600
    total_nb_timesteps = 365 * 24 * 60 * 60 / time_discretization
    timer = pycity_base.classes.timer.Timer(time_discretization=time_discretization,
                                            timesteps_total=total_nb_timesteps)
    weather = pycity_base.classes.weather.Weather(timer, use_TRY=True)
    prices = pycity_base.classes.prices.Prices()

    environment = pycity_base.classes.environment.Environment(timer, weather,
                                                              prices)

    dhw_annex42 = dhw.DomesticHotWater(environment,
                                       t_flow=60,
                                       thermal=True,
                                       method=1,  # Annex 42
                                       daily_consumption=100,
                                       supply_temperature=25)

    results = dhw_annex42.get_power(currentValues=False)

    print('Results for Annex42 profile:')
    print()
    print("Thermal demand: " + str(results[0]))
    print("Required flow temperature: " + str(results[1]))
    print()
    
    #  Convert into energy values in kWh
    dhw_energy_curve = results[0] * time_discretization / (3600*1000)
    annual_energy_demand = np.sum(dhw_energy_curve)

    print('Annual dhw energy demand in kWh: ', annual_energy_demand)

    print('#----------------------------------------------------------------')
    #  #---------------------------------------------------------------------
    #  Compute active occupants for one year
    #  Max. occupancy is 5 people simultaneously
#    occupancy = np.random.geometric(p=0.8, size=6 * 24 * 365) - 1
#    occupancy = np.minimum(5, occupancy)
    occup_obj = pycity_base.classes.demand.occupancy.Occupancy(environment,
                                                               number_occupants=3)
    occupancy = occup_obj.occupancy

    dhw_stochastical = dhw.DomesticHotWater(environment,
                                            t_flow=60,
                                            thermal=True,
                                            method=2,
                                            supply_temperature=20,
                                            occupancy=occupancy)

    dhw_power_curve = dhw_stochastical.get_power(currentValues=False,
                                                 returnTemperature=False)
    #  Convert into energy values in kWh
    dhw_energy_curve = dhw_power_curve * time_discretization / (3600*1000)
    annual_energy_demand = np.sum(dhw_energy_curve)
    #  DHW volume flow curve in liters/hour
    volume_flow_curve = dhw_stochastical.water
    #  Recalc into water volume in liters
    water_volume_per_timestep = volume_flow_curve / 3600 * time_discretization
    # Average daily dhw consumption in liters
    av_daily_dhw_volume = np.sum(water_volume_per_timestep) / 365

    print('Results for stochastic DHW profile:\n')
    print('Max number of occupants:', max(occupancy))
    print('Annual dhw energy demand in kWh: ', annual_energy_demand)
    print('Average daily domestic hot water volume in liters:',
          av_daily_dhw_volume)

    if do_plot:
        ax1 = plt.subplot(2, 1, 1)
        plt.step(np.arange(8760) + 1, dhw_stochastical.loadcurve, linewidth=2)
        plt.ylabel("Heat demand in Watt")
        plt.xlim((0, 8760))

        plt.subplot(2, 1, 2, sharex=ax1)
        plt.step((np.arange(len(occupancy)) * 10 + 10) / 60, occupancy,
                 linewidth=2)
        plt.ylabel("Active occupants")
        offset = 0.2
        plt.ylim((-offset, max(occupancy) + offset))
        plt.yticks(list(range(int(max(occupancy) + 1))))

        plt.show()


if __name__ == '__main__':
    #  Run program
    run_example(do_plot=True)
