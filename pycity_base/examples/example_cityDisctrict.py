#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import os
import xlrd
import numpy as np
import shapely.geometry.point as point

import pycity_base.classes.Timer
import pycity_base.classes.Weather
import pycity_base.classes.Prices
import pycity_base.classes.Environment

import pycity_base.classes.demand.Apartment as Apartment
import pycity_base.classes.demand.DomesticHotWater as DomesticHotWater
import pycity_base.classes.demand.ElectricalDemand as ElectricalDemand
import pycity_base.classes.demand.SpaceHeating as SpaceHeating
import pycity_base.classes.HeatingCurve as HeatingCurve
import pycity_base.classes.Building as Building
import pycity_base.classes.CityDistrict as CityDistrict
import pycity_base.classes.supply.PV as PV
import pycity_base.classes.supply.WindEnergyConverter as Wind


def run_test():

    #  Generate timer, weather and price objects
    timer = pycity_base.classes.Timer.Timer()
    weather = pycity_base.classes.Weather.Weather(timer)
    prices = pycity_base.classes.Prices.Prices()

    #  Generate environment
    environment = pycity_base.classes.Environment.Environment(timer, weather, prices)

    #  Generate city district object
    cityDistrict = CityDistrict.CityDistrict(environment)
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
        heat_demand = SpaceHeating.SpaceHeating(environment,
                                                method=1,  # Standard load profile
                                                livingArea=146,
                                                specificDemand=166)

        #  Generate electrical demand curve
        el_demand = ElectricalDemand.ElectricalDemand(environment,
                                                      method=1,  # Standard load profile
                                                      annualDemand=3000)

        #  Generate domestic hot water demand curve
        dhw_annex42 = DomesticHotWater.DomesticHotWater(environment,
                                                        tFlow=60,
                                                        thermal=True,
                                                        method=1,  # Annex 42
                                                        dailyConsumption=70,
                                                        supplyTemperature=25)

        #  Generate apartment and add demand durves
        apartment = Apartment.Apartment(environment)
        apartment.addEntity(heat_demand)
        apartment.addMultipleEntities([el_demand, dhw_annex42])

        #  Generate heating curve
        heatingCurve = HeatingCurve.HeatingCurve(environment)

        #  Generate building and add apartment and heating curve
        building = Building.Building(environment)
        entities = [apartment, heatingCurve]
        building.addMultipleEntities(entities)

        #  Add buildings to city district
        cityDistrict.addEntity(entity=building, position=dict_pos[i])

    #  Generate PV farms within city district within loop
    #  #-------------------------------------------------------------------
    for i in range(2):

        #  Generate PV field within city district
        pv = PV.PV(environment, 20, 0.15)

        #  Add PV fields to city district
        cityDistrict.addEntity(entity=pv, position=dict_pos[i+4])

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

    wec = Wind.WindEnergyConverter(environment=environment,
                                   velocity=mapWind,
                                   power=mapPower,
                                   hubHeight=hubHeight)

    cityDistrict.addEntity(entity=wec, position=point.Point(100, 100))

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
    print(cityDistrict.get_aggr_space_h_power_curve())
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
    run_test()
