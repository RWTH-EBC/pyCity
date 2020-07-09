#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example script on how to generate a city district.
"""

from __future__ import division

import os
import xlrd
import numpy as np
import shapely.geometry.point as point

import pycity_base.classes.timer as time
import pycity_base.classes.weather as we
import pycity_base.classes.prices as pr
import pycity_base.classes.environment as env
import pycity_base.classes.demand.apartment as ap
import pycity_base.classes.demand.domestic_hot_water as dhw
import pycity_base.classes.demand.electrical_demand as ed
import pycity_base.classes.demand.space_heating as sh
import pycity_base.classes.heating_curve as hc
import pycity_base.classes.building as bd
import pycity_base.classes.city_district as cd
import pycity_base.classes.supply.photovoltaic as pv
import pycity_base.classes.supply.wind_energy_converter as wec


def run_example():
    timestep = 900  # in seconds

    nb_timesteps = int(365 * 24 * 3600 / timestep)

    #  Generate environment with timer, weather, and prices objects
    timer = time.Timer(time_discretization=timestep,
                       timesteps_total=nb_timesteps)
    weather = we.Weather(timer)
    prices = pr.Prices()
    environment = env.Environment(timer, weather, prices)

    #  Generate city district object
    cityDistrict = cd.CityDistrict(environment)
    #  Annotations: To prevent some methods of subclasses uesgraph / nx.Graph
    #  from failing (e.g. '.subgraph()) environment is optional input
    #  parameter.

    #  Empty dictionary for positions
    dict_pos = {}

    #  Generate shapely point positions
    dict_pos[0] = point.Point(0, 0)
    dict_pos[1] = point.Point(0, 10)
    dict_pos[2] = point.Point(10, 0)
    dict_pos[3] = point.Point(10, 10)
    dict_pos[4] = point.Point(20, 20)
    dict_pos[5] = point.Point(30, 30)

    #  Generate building objects within loop
    #  #-------------------------------------------------------------------
    for i in range(4):

        #  Generate heat demand curve for space heating
        heat_demand = sh.SpaceHeating(environment,
                                      method=1,  # Standard load profile
                                      living_area=146,
                                      specific_demand=166)

        #  Generate electrical demand curve
        el_demand = ed.ElectricalDemand(environment,
                                        method=1,  # Standard load profile
                                        annual_demand=3000)

        #  Generate domestic hot water demand curve
        dhw_annex42 = dhw.DomesticHotWater(environment,
                                           t_flow=60,
                                           thermal=True,
                                           method=1,  # Annex 42
                                           daily_consumption=70,
                                           supply_temperature=25)
        #  Annotation: The usage of the deterministic IEA Annex 42 hot water
        #  profile is fine for a single apartment. However, try to use
        #  stochastic dhw profiles (method = 2 --> Requires occupancy
        #  input profile) on city district scale. The usage of Annex 42
        #  profiles on city district scale will produce illogical peak loads /
        #  peak loads at the same point in time!
        #  Thus, this section is for example purpose, only (executes faster
        #  than generating multiple, stochastic profiles)

        #  Generate apartment and add demand durves
        apartment = ap.Apartment(environment)
        apartment.addEntity(heat_demand)
        apartment.addMultipleEntities([el_demand, dhw_annex42])

        #  Generate heating curve
        heatingcurve = hc.HeatingCurve(environment)

        #  Generate building and add apartment and heating curve
        building = bd.Building(environment)
        entities = [apartment, heatingcurve]
        building.addMultipleEntities(entities)

        #  Add buildings to city district
        cityDistrict.addEntity(entity=building, position=dict_pos[i])

    #  Generate PV farms within city district within loop
    #  #-------------------------------------------------------------------
    for i in range(2):

        #  Generate PV field within city district
        pv_unit = pv.PV(environment=environment, method=0, area=20, eta_noct=0.15)

        #  Add PV fields to city district
        cityDistrict.addEntity(entity=pv_unit, position=dict_pos[i+4])

    #  Add wind energy converter
    #  #-------------------------------------------------------------------
    # Create Wind Energy Converter (ENERCON E-126)
    src_path = os.path.dirname(os.path.dirname(__file__))
    wind_data_path = os.path.join(src_path, 'inputs',
                                  'wind_energy_converters.xlsx')
    wecDatasheets = xlrd.open_workbook(wind_data_path)
    ENERCON_E_126 = wecDatasheets.sheet_by_name("ENERCON_E_126")
    hubHeight = ENERCON_E_126.cell_value(0, 1)
    mapWind = []
    mapPower = []
    counter = 0
    while ENERCON_E_126._dimnrows > 3 + counter:
        mapWind.append(ENERCON_E_126.cell_value(3 + counter, 0))
        mapPower.append(ENERCON_E_126.cell_value(3 + counter, 1))
        counter += 1

    mapWind = np.array(mapWind)
    mapPower = np.array(mapPower) * 1000

    turbine = wec.WindEnergyConverter(environment=environment,
                                      velocity=mapWind,
                                      power=mapPower,
                                      hub_height=hubHeight)

    cityDistrict.addEntity(entity=turbine, position=point.Point(100, 100))

    #  Extract information of city object
    #  #-------------------------------------------------------------------

    print('Number of building entities:')
    print(cityDistrict.get_nb_of_building_entities())

    print('Node id list of building entities:')
    print(cityDistrict.get_list_build_entity_node_ids())

    print('Number of PV farms:')
    print(cityDistrict.get_nb_of_entities(entity_name='pv'))

    print('Node information:')
    print(cityDistrict.nodes(data=True))

    print('\n')

    print('Power curves of all building objects:')
    print(cityDistrict.get_power_curves())
    print()

    print('Flow temperatures:')
    print(cityDistrict.getFlowTemperatures())
    print()

    print('PV power:')
    print(cityDistrict.getPVPower())
    print()

    print('Return aggregated space heating power curve:')
    print(cityDistrict.get_aggr_space_heating_power_curve())
    print()

    print('Return aggregated space cooling power curve:')
    print(cityDistrict.get_aggr_space_cooling_power_curve())
    print()

    print('Return aggregated electrical power curve:')
    print(cityDistrict.get_aggr_el_power_curve())
    print()

    print('Return hot water power curve:')
    print(cityDistrict.get_aggr_dhw_power_curve())
    print()

    print('Get wind energy converter power:')
    print(cityDistrict.getWindEnergyConverterPower())
    print()

    print('Get list of nodes of type building:')
    print(cityDistrict.get_list_id_of_spec_node_type(node_type='building'))
    print()

    print('Get total number of occupants within city district:')
    print(cityDistrict.get_nb_occupants())


if __name__ == '__main__':
    #  Run program
    run_example()
