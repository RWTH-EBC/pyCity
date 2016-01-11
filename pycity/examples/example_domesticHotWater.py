#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 22:07:04 2015

@author: Thomas
"""

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

import pycity.classes.demand.DomesticHotWater as DomesticHotWater

import pycity.classes.Timer
import pycity.classes.Weather
import pycity.classes.Environment
import pycity.classes.Prices


def run_test():
    timeDiscretization = 3600
    total_nb_timesteps = 365 * 24 * 60 * 60 / timeDiscretization
    timer = pycity.classes.Timer.Timer(timeDiscretization=timeDiscretization,
                                       timestepsTotal=total_nb_timesteps)
    weather = pycity.classes.Weather.Weather(timer, useTRY=True)
    prices = pycity.classes.Prices.Prices()

    environment = pycity.classes.Environment.Environment(timer, weather,
                                                         prices)

    dhw_annex42 = DomesticHotWater.DomesticHotWater(environment,
                                                    tFlow=60,
                                                    thermal=True,
                                                    method=1,  # Annex 42
                                                    dailyConsumption=100,
                                                    supplyTemperature=25)

    results = dhw_annex42.getDemand(currentValues=False)

    print('Results for Annex42 profile:')
    print()
    print("Thermal demand: " + str(results[0]))
    print("Required flow temperature: " + str(results[1]))
    print()
    
    #  Convert into energy values in kWh
    dhw_energy_curve = results[0] * timeDiscretization / (3600*1000)
    annual_energy_demand = np.sum(dhw_energy_curve)

    print('Annual dhw energy demand in kWh: ', annual_energy_demand)

    print('#----------------------------------------------------------------')
    #  #---------------------------------------------------------------------
    #  Compute active occupants for one year
    #  Max. occupancy is 5 people simultaneously
    occupancy = np.random.geometric(p=0.8, size=6 * 24 * 365) - 1
    occupancy = np.minimum(5, occupancy)

    dhw_stochastical = DomesticHotWater.DomesticHotWater(environment,
                                                         tFlow=60,
                                                         thermal=True,
                                                         method=2,
                                                         supplyTemperature=20,
                                                         occupancy=occupancy)

    dhw_power_curve = dhw_stochastical.getDemand(currentValues=False,
                                                 returnTemperature=False)
    #  Convert into energy values in kWh
    dhw_energy_curve = dhw_power_curve * timeDiscretization / (3600*1000)
    annual_energy_demand = np.sum(dhw_energy_curve)
    #  DHW volume flow curve in liters/hour
    volume_flow_curve = dhw_stochastical.water
    #  Recalc into water volume in liters
    water_volume_per_timestep = volume_flow_curve / 3600 * timeDiscretization
    # Average daily dhw consumption in liters
    av_daily_dhw_volume = np.sum(water_volume_per_timestep) / 365

    print('Results for stochastic DHW profile:\n')
    print('Max number of occupants:', max(occupancy))
    print('Annual dhw energy demand in kWh: ', annual_energy_demand)
    print('Average daily domestic hot water volume in liters:',
          av_daily_dhw_volume)

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
    run_test()
