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

    def addEntity(self, entity, position, name=None, is_supply_electricity=None, is_supply_heating=False,
                  is_supply_cooling=False, is_supply_gas=False, is_supply_other=False):
        """
        Method adds entity (e.g. building object) to city district object.

        Parameters
        ----------
        entity : object
            Possible entity object (building, windenergyconverter or pv)
        position : sympy.geometry.Point object
            New node's position
        name : str, optional
            Name of entity (default: None)
        is_supply_electricity : bool, optional
            Boolean to define, if entity is of kind electrical supply (default: None)
            True - Entity is electric supplier
            False - Entity is not an electric supplier
            When initialized as "None", method automatically decides if value is True or False,
            based on _kind of entity ("building" - False; "windenergyconverter" - True; "pv" - True)
        is_supply_heating : bool, optional
            Boolean to define, if entity is of kind heating supply (default: False)
        is_supply_cooling : bool, optional
            Boolean to define, if entity is of kind cooling supply (default: False)
        is_supply_gas : bool, optional
            Boolean to define, if entity is of kind gas supply (default: False)
        is_supply_other : bool, optional
            Boolean to define, if entity is of kind other supply (default: False)

        Example
        -------
        >>> myBuilding = Building(...)
        >>> myCityDistrict = CityDistrict(...)
        >>> myCityDistrict.addDevice(myBuilding)
        """

        if is_supply_electricity is None:  # Automatically decide via entity._kind
            if entity._kind == "building":
                is_supply_electricity = False

            elif entity._kind == "windenergyconverter":
                is_supply_electricity = True

            elif entity._kind == "pv":
                is_supply_electricity = True
            else:
                raise ValueError('Unknown kind of entity. Select known entity (building, windenergyconverter, pv) or '
                                 'clearly define parameter is_supply_electricity, when using own entity type.')

        #  Use add_building method of uesgraph (in ues graph, every demand and every supplier is linked to a building)
        #  PV or wec "buildings" are buildings with zero energy demand (only generation is taken into account)
        #  Add building node to graph (node_type='building')
        node_number = self.add_building(name=name, position=position, is_supply_electricity=is_supply_electricity,
                                        is_supply_heating=is_supply_heating, is_supply_cooling=is_supply_cooling,
                                        is_supply_gas=is_supply_gas, is_supply_other=is_supply_other)

        #  Add entity as attribute to node with returned node_number
        self.add_node(node_number, entity=entity)

    def addMultipleEntities(self, entities, positions):
        """
        Add multiple entities to the existing city district.
        
        Parameter
        ---------
        entities_tuple : List-like
            List (or tuple) of entities that are added to the city district
        positions : List-like
            List (or tuple) of positions (of entities) that are added to city district
            (list of sympy.geometry.Point objects)
            
        Example
        -------
        >>> import sympy.geometry.point as point
        >>> myPV  = PV(...)
        >>> myWEC = WindEnergyConverter(...)
        >>> myCityDistrict = CityDistrict(...)
        >>> position_1 = point.Point(0, 0)
        >>> position_2 = point.Point(0, 10)
        >>> myCityDistrict.addMultipleEntities([myPV, myWEC], [position_1, position_2])
        """
        assert len(entities) == len(positions), 'Number of entities must match to number of positions'

        for i in range(len(entities)):
            curr_entity = entities[i]
            curr_pos = positions[i]
            self.addEntity(entity=curr_entity, position=curr_pos)

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
        Get the (aggregated) forecast of all (stand alone) pv units.
        """

        #  Create empty list of pv entities
        pv_entities = []

        #  Loop over all nodes
        for n in self:
            #  If node holds attribute 'node_type'
            if 'node_type' in self.node[n]:
                #  If node_type is building
                if self.node[n]['node_type'] == 'building':
                    #  If entity is of type pv
                    if self.node[n]['entity']._kind == 'pv':
                        #  Add pv entity to list
                        pv_entities.append(self.node[n]['entity'])

        if len(pv_entities) == 0:
            return np.zeros(self.environment.timer.timestepsHorizon)
        else:
            return self._getRESPower(pv_entities)

    def getWindEnergyConverterPower(self):
        """
        Get the (aggregated) forecast of all wind energy converters.
        """

        #  Create empty list of pv entities
        wind_entities = []

        #  Loop over all nodes
        for n in self:
            #  If node holds attribute 'node_type'
            if 'node_type' in self.node[n]:
                #  If node_type is building
                if self.node[n]['node_type'] == 'building':
                    #  If entity is of type pv
                    if self.node[n]['entity']._kind == 'windenergyconverter':
                        #  Add pv entity to list
                        wind_entities.append(self.node[n]['entity'])

        if len(wind_entities) == 0:
            return np.zeros(self.environment.timer.timestepsHorizon)
        else:
            return self._getRESPower(wind_entities)

    def getDemands(self):
        """ 
        Get the aggregated electricity and heat demand forecast of all
        buildings.

        Returns tuple of electrical and thermal demand array

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
                    #  If entity is kind building
                    if self.node[n]['entity']._kind == 'building':
                        temp = self.node[n]['entity'].getDemands()
                        demandElectrical += temp[0]
                        demandThermal += temp[1]

        return (demandElectrical, demandThermal)

    def getFlowTemperatures(self):
        """ 
        Get the aggregated flow temperature forecast.
        """

        timesteps = self.environment.timer.timestepsHorizon
        flowTemperature = np.zeros(timesteps)

         #  Loop over all nodes
        for n in self:
            #  If node holds attribute 'node_type'
            if 'node_type' in self.node[n]:
                #  If node_type is building
                if self.node[n]['node_type'] == 'building':
                    #  If entity is kind building
                    if self.node[n]['entity']._kind == 'building':
                        flow_temp = self.node[n]['entity'].getFlowTemperature()
                        flowTemperature = np.maximum(flowTemperature, flow_temp)

        return flowTemperature
