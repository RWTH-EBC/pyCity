#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example script on how to generate a city district with space heating,
user, stochastic electric, and hot water profiles plus energy systems.
"""

from __future__ import division

import shapely.geometry.point as point
import matplotlib.pyplot as plt

import uesgraphs.visuals as uesvis

import pycity_base.classes.timer as time
import pycity_base.classes.weather as weath
import pycity_base.classes.prices as price
import pycity_base.classes.environment as env
import pycity_base.classes.demand.apartment as apart
import pycity_base.classes.demand.occupancy as occ
import pycity_base.classes.demand.domestic_hot_water as dhw
import pycity_base.classes.demand.electrical_demand as eldem
import pycity_base.classes.demand.space_heating as spaceheat
import pycity_base.classes.building as build
import pycity_base.classes.city_district as citydist
import pycity_base.classes.supply.building_energy_system as besys
import pycity_base.classes.supply.boiler as boil
import pycity_base.classes.supply.photovoltaic as pvsys


def run_example():
    #  Define the time discretization for the timer object
    timestep = 3600  # in seconds

    #  Define the total number of timesteps (in this case for one year)
    nb_timesteps = int(365 * 24 * 3600 / timestep)

    #  Generate environment with timer, weather, and prices objects
    #  ######################################################################
    timer = time.Timer(time_discretization=timestep,
                       timesteps_total=nb_timesteps)
    weather = weath.Weather(timer=timer)
    prices = price.Prices()

    environment = env.Environment(timer=timer, weather=weather, prices=prices)

    #  Generate city district object
    #  ######################################################################
    city_district = citydist.CityDistrict(environment=environment)
    #  Annotations: To prevent some methods of subclasses uesgraph / nx.Graph
    #  from failing (e.g. '.subgraph()) environment is set as optional input
    #  parameter. However, it is necessary to use an environment object as
    #  input parameter to initialize a working cityDistrict object!

    #  Empty dictionary for building positions
    dict_pos = {}

    #  Generate shapely point positions
    dict_pos[0] = point.Point(0, 0)  # (x, y)
    dict_pos[1] = point.Point(20, 0)

    #  Use for loop to generate two identical building objects for city
    #  district
    #  ######################################################################
    for i in range(2):
        living_area = 200  # in m^2
        spec_sh_dem = 160  # Specific space heating demand in kWh/m^2
        number_occupants = 3  # Total number of occupants

        #  Generate space heating demand object (holding loadcurve attribute
        #  with space heating power)
        heat_demand = spaceheat.SpaceHeating(
            environment=environment,
            method=1,  # Standard load profile
            living_area=living_area,  # in m^2
            specific_demand=spec_sh_dem)  # in kWh/m^2

        #  Generate occupancy object with stochastic user profile
        occupancy = occ.Occupancy(environment=environment,
                                  number_occupants=number_occupants)

        #  Generate electrical demand object
        el_dem_stochastic = eldem.ElectricalDemand(
            environment=environment,
            method=2,  # stochastic Richardson profile (richardsonpy)
            total_nb_occupants=number_occupants,  # Number of occupants
            randomize_appliances=True,  # Random choice of installed appliances
            light_configuration=10,  # Light bulb configuration nb.
            occupancy=occupancy.occupancy,  # Occupancy profile (600 s resol.)
            prev_heat_dev=True,  # Prevent space heating and hot water devices
            annual_demand=None,  # Annual el. demand in kWh could be used for
            do_normalization=False)  # rescaling (if do_normalization is True)
        #  Annotation: The calculation of stochastic electric load profiles
        #  is time consuming. If you prefer a faster method, you can either
        #  hand over an own array-like load curve (method=0) or generate a
        #  standardized load profile (SLP) (method=1)

        #  Generate domestic hot water demand object
        dhw_obj = dhw.DomesticHotWater(
            environment=environment,
            t_flow=60,  # DHW output temperature in degree Celsius
            method=2,  # Stochastic dhw profile
            supply_temperature=25,  # DHW inlet flow temperature in degree C.
            occupancy=occupancy.occupancy)  # Occupancy profile (600 s resol.)

        #  Generate apartment and add demand durves
        apartment = apart.Apartment(environment)
        apartment.addMultipleEntities([heat_demand,
                                       el_dem_stochastic,
                                       dhw_obj])

        #  Generate building and add apartment
        building = build.Building(environment)
        building.addEntity(apartment)

        #  Add buildings to city district
        city_district.addEntity(entity=building,
                                position=dict_pos[i])

    #  Access information on city district object instance
    #  ######################################################################
    print('Get number of building entities:')
    print(city_district.get_nb_of_building_entities())
    print()

    print('Get list with node ids of building entities:')
    print(city_district.get_list_build_entity_node_ids())
    print()

    print('Get city district overall space heating power load curve:')
    print(city_district.get_aggr_space_heating_power_curve())
    print()

    print('Get city district overall space cooling power load curve:')
    print(city_district.get_aggr_space_cooling_power_curve())
    print()

    #  We can use the Visuals class of uesgraphs to plot the city district

    #  Generate uesgraphs visuals object instance
    uesvisuals = uesvis.Visuals(uesgraph=city_district)

    fig = plt.figure()
    ax = fig.gca()
    ax = uesvisuals.create_plot_simple(ax=ax)
    plt.show()
    plt.close()

    #  Access buildings
    #  ######################################################################
    #  As city_district is a networkx graph object, we can access the building
    #  entities with the corresponding building node,
    #  Pointer to building object with id 1001:
    building_1001 = city_district.nodes[1001]['entity']

    print('Get building 1001 electric load curve:')
    print(building_1001.get_electric_power_curve())
    print()

    #  Add energy systems to buildings
    #  ######################################################################
    #  We can also add building energy systems (BES) to each building object

    #  Generate boiler object
    boiler = boil.Boiler(environment=environment,
                         q_nominal=10000,  # Boiler thermal power in Watt
                         eta=0.85)  # Boiler efficiency

    #  Generate PV module object
    pv = pvsys.PV(environment=environment,
                  method=0,
                  area=30,  # Area in m^2
                  eta_noct=0.15)  # Electrical efficiency at NOCT conditions

    # Instantiate BES (container object for all energy systems)
    bes = besys.BES(environment)

    #  Add energy systems to bes
    bes.addMultipleDevices([boiler, pv])

    #  Add bes to building 1001
    building_1001.addEntity(entity=bes)

    print('Does building 1001 has a building energy system (BES)?')
    print(building_1001.has_bes)

    #  Access boiler nominal thermal power
    print('Nominal thermal power of boiler in kW:')
    print(building_1001.bes.boilers[0].q_nominal / 1000)


if __name__ == '__main__':
    #  Run program
    run_example()
