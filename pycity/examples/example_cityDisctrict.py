#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import division
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


def run_test():
    #  Generate timer, weather and price objects
    timer = pycity.classes.Timer.Timer()
    weather = pycity.classes.Weather.Weather(timer)
    prices = pycity.classes.Prices.Prices()

    #  Generate environment
    environment = pycity.classes.Environment.Environment(timer, weather, prices)

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

    #  Generate PV field within city district
    pv = PV.PV(environment, 20, 0.15)

    #  Generate city district object
    cityDistrict = CityDistrict.CityDistrict(environment)
    #  Annotations: To prevent some methods of subclasses uesgraph / nx.Graph
    #  from failing (e.g. '.subgraph()) environment is optional input
    #  parameter.

    #  Generate sympy point positions
    position_1 = point.Point(0, 0)
    position_2 = point.Point(0, 10)
    position_3 = point.Point(10, 0)
    position_4 = point.Point(10, 10)
    position_5 = point.Point(20, 20)
    position_6 = point.Point(30, 30)

    #  Add buildings to city district
    cityDistrict.addEntity(entity=building, position=position_1)
    cityDistrict.addEntity(entity=building, position=position_2)
    cityDistrict.addEntity(entity=building, position=position_3)
    cityDistrict.addEntity(entity=building, position=position_4)

    #  Add PV fields to city district
    cityDistrict.addEntity(entity=pv, position=position_5)
    cityDistrict.addEntity(entity=pv, position=position_6)

    print('Number of building entities:')
    print(cityDistrict.get_nb_of_building_entities())

    print('Node id list of building entities:')
    print(cityDistrict.get_list_build_entity_node_ids())

    print('Number of PV farms:')
    print(cityDistrict.get_nb_of_entities(entity_name='pv'))

    print('Node information:')
    print(cityDistrict.nodes(data=True))

    print('\n')

    print('Energy demands of building objects:')
    print(cityDistrict.getDemands())

    print('Flow temperatures:')
    print(cityDistrict.getFlowTemperatures())

    print('PV power:')
    print(cityDistrict.getPVPower())

if __name__ == '__main__':
    #  Run program
    run_test()
