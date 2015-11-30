#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python code with city district class. Usage requires installation of uesgraphs Python package.
uesgraphs can be downloaded on Github: https://github.com/RWTH-EBC/uesgraphs
"""


from __future__ import division
import numpy as np

try:
    import uesgraphs.uesgraph as ues
except:
    ImportError('Package uesgraphs is not found. Please install uesgraphs first. https://github.com/RWTH-EBC/uesgraphs')


class CityDistrict(ues.UESGraph):
    """
    City district class. Inheritance from urban energy system graph (uesgraph).
    """

    def __init__(self, environment):
        """
        Constructor of city district object.

        Parameters
        ----------
        environment : object
            Environmental object of PyCity (common to all other objects)

        Atributes
        ---------
        _kind : str
            Type of object ("citydistrict")
        buildings : list
            List holding building objects
        wec : list
            List holding wind energy converters of city district
        pv : list
            List holding central PV farms of city district
        """
        #  Initialize super class
        super(CityDistrict, self).__init__()

        #  Add pointer to environment
        self.environment = environment

        #  Define object type
        self._kind = 'citydistrict'

    def addEntity(self, entity, position=None, name=None):
        """
        Method adds entity (e.g. building object) to city district object.

        Parameters
        ----------
        entity : object
            Possible entity object (building, windenergyconverter or pv)
        position : sympy.geometry.Point object, optional
            New node's position (default: None)
        name : str, optional
            Name of entity (default: None)

        Example
        -------
        >>> myBuilding = Building(...)
        >>> myCityDistrict = CityDistrict(...)
        >>> myCityDistrict.addDevice(myBuilding)
        """

        if entity._kind == "building":
            is_supply_electricity = False

        elif entity._kind == "windenergyconverter":
            is_supply_electricity = True

        elif entity._kind == "pv":
            is_supply_electricity = True

        #  TODO: Add further entities, e.g. power plants, gas supply, cooling supply feeder etc.

        #  Use add_building method of uesgraph (in ues graph, every demand and every supplier is linked to a building)
        #  PV or wec "buildings" are buildings with zero energy demand (only generation is taken into account)
        #  Add building node to graph (node_type='building')
        node_number = self.add_building(name=name, position=position, is_supply_electricity=is_supply_electricity)

        #  Add entity as attribute to node with returned node_number
        self.add_node(node_number, entity=entity)

    def addMultipleEntities(self, entities):
        """
        Add multiple entities to the existing city district
        
        Parameter
        ---------
        entities: List-like
            List (or tuple) of entities that are added to the city district
            
        Example
        -------
        >>> myPV  = PV(...)
        >>> myWEC = WindEnergyConverter(...)
        >>> myCityDistrict = CityDistrict(...)
        >>> myCityDistrict.addMultipleEntities([myPV, myWEC])
        """
        for entity in entities:
            self.addEntity(entity)

    def _getRESPower(self, generators):
        """
        Get the (aggregated) forecast of all renewable electricity generators.
        """
        power = np.zeros(self.environment.timer.timestepsHorizon)
        for generator in generators:
            power += generator.getPower()

        return power

    def getPVPower(self):
        """
        Get the (aggregated) forecast of all pv units.
        """
        #  Fixme: Of all pv units or only centralized pv farms?
        if len(self.pv) == 0:
            return np.zeros(self.environment.timer.timestepsHorizon)
        else:
            return self._getRESPower(self.pv)

    def getWindEnergyConverterPower(self):
        """
        Get the (aggregated) forecast of all wind energy converters.
        """
        if len(self.wec) == 0:
            return np.zeros(self.environment.timer.timestepsHorizon)
        else:
            return self._getRESPower(self.wec)

    def getDemands(self):
        """ 
        Get the aggregated electricity and heat demand forecast of all
        buildings.
        
        Order
        -----
        ElectricityDemand : Array_like
            Aggregated electrical demand
        HeatDemand : Array_like
            Aggregated heat demand
        """
        timesteps = self.environment.timer.timestepsHorizon
        demandElectrical = np.zeros(timesteps)
        demandThermal = np.zeros(timesteps)

        #  Loop over all nodes
        for n in self:
            #  If node holds attribute 'node_type'
            if 'node_type' in self.node[n]:
                #  If node_type is building
                if self.node[n]['node_type'] == 'building':
                    temp = self.node[n]['entity'].getDemands()
                    demandElectrical += temp[0]
                    demandThermal += temp[1]

        # # for building in self.buildings:
        #     temp = building.getDemands()
        #     demandElectrical += temp[0]
        #     demandThermal += temp[1]

        return (demandElectrical, demandThermal)

    def getFlowTemperatures(self):
        """ 
        Get the aggregated flow temperature forecast.
        """
        timesteps = self.environment.timer.timestepsHorizon
        flowTemperature = np.zeros(timesteps)

        for building in self.buildings:
            flowTemperature = np.maximum(flowTemperature,
                                         building.getFlowTemperature())

        return flowTemperature
