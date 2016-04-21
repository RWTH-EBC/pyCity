#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python code with city district class. Usage requires installation of uesgraphs
Python package.
uesgraphs can be downloaded on Github: https://github.com/RWTH-EBC/uesgraphs
"""

from __future__ import division
import numpy as np

try:
    import uesgraphs.uesgraph as ues
except:
    ImportError('Package uesgraphs is not found. Please install uesgraphs' +
                'first. https://github.com/RWTH-EBC/uesgraphs')


class CityDistrict(ues.UESGraph):
    """
    City district class. Inheritance from urban energy system graph (uesgraph).

    See: https://github.com/RWTH-EBC/uesgraphs for further information
    """

    def __init__(self, environment=None):
        """
        Constructor of city district object.

        Parameters
        ----------
        environment : object
            Environment object of pycity

        Attributes
        ----------
        _kind : str
            Type of object ('citydistrict')
        environemnt : object
            Environment object of pycity (default: None)

        Annotations
        -----------
        To prevent different methods of subclass nx.Graph from failing
        the environment object is used as optional input for __init__
        (not as fix input). E.g. when generating subgraph via .subgraph()
        method, user has to add environment after initialization.
        """

        #  Initialize super class
        super(CityDistrict, self).__init__()

        #  Add pointer to environment
        self.environment = environment

        #  List of possible entity names (might be extended by user
        #  when using own entity._kind)
        self.entity_name_list = ['building', 'pv', 'windenergyconverter']

        #  Define object type
        self._kind = 'citydistrict'

    def addEntity(self, entity, position, name=None,
                  is_supply_electricity=None, is_supply_heating=False,
                  is_supply_cooling=False, is_supply_gas=False,
                  is_supply_other=False):
        """
        Method adds entity (e.g. building object) to city district object.

        Parameters
        ----------
        entity : object
            Standard entity object (building, windenergyconverter or pv)
        position : sympy.geometry.Point object
            New node's position
        name : str, optional
            Name of entity (default: None)
        is_supply_electricity : bool, optional
            Boolean to define, if entity is of kind electrical supply
            (default: None)
            True - Entity is electric supplier
            False - Entity is not an electric supplier
            When initialized as "None", method automatically decides if value
            is True or False, based on _kind of entity
            ("building" - False; "windenergyconverter" - True; "pv" - True)
        is_supply_heating : bool, optional
            Boolean to define, if entity is of kind heating supply
            (default: False)
        is_supply_cooling : bool, optional
            Boolean to define, if entity is of kind cooling supply
            (default: False)
        is_supply_gas : bool, optional
            Boolean to define, if entity is of kind gas supply
            (default: False)
        is_supply_other : bool, optional
            Boolean to define, if entity is of kind other supply
            (default: False)

        Returns
        -------
        node_number : int
            Node number

        Example
        -------
        >>> myBuilding = Building(...)
        >>> myCityDistrict = CityDistrict(...)
        >>> myCityDistrict.addDevice(myBuilding)
        """

        if self.environment is None:
            #  Extract environment from entity
            self.environment = entity.environment

        # Automatically decide via entity._kind
        if is_supply_electricity is None:
            if entity._kind == "building":
                is_supply_electricity = False

            elif entity._kind == "windenergyconverter":
                is_supply_electricity = True

            elif entity._kind == "pv":
                is_supply_electricity = True
            else:
                raise ValueError('Unknown kind of entity. Select known ' +
                                 'entity (building, windenergyconverter, pv)' +
                                 ' or clearly define parameter ' +
                                 'is_supply_electricity, when using own ' +
                                 'entity type.')

        # If entity._kind is new, extend entities list
        if entity._kind not in self.entity_name_list:
            self.entity_name_list.append(entity._kind)

        # Use add_building method of uesgraph (in ues graph, every demand
        #  and every supplier is linked to a building). PV or wec "buildings"
        #  are buildings with zero energy demand (only generation is taken
        #  into account). Add building node to graph (node_type='building')
        node_number = self.add_building(name=name, position=position,
                                        is_supply_electricity=
                                        is_supply_electricity,
                                        is_supply_heating=is_supply_heating,
                                        is_supply_cooling=is_supply_cooling,
                                        is_supply_gas=is_supply_gas,
                                        is_supply_other=is_supply_other)

        #  Add entity as attribute to node with returned node_number
        self.add_node(node_number, entity=entity)

        return node_number

    def addMultipleEntities(self, entities, positions):
        """
        Add multiple entities to the existing city district.
        
        Parameter
        ---------
        entities_tuple : List-like
            List (or tuple) of entities that are added to the city district
        positions : List-like
            List (or tuple) of positions (of entities) that are added to city
            district
            (list of sympy.geometry.Point objects)
            
        Example
        -------
        >>> import sympy.geometry.point as point
        >>> myPV  = PV(...)
        >>> myWEC = WindEnergyConverter(...)
        >>> myCityDistrict = CityDistrict(...)
        >>> pos_1 = point.Point(0, 0)
        >>> pos_2 = point.Point(0, 10)
        >>> myCityDistrict.addMultipleEntities([myPV, myWEC], [pos_1, pos_2])
        """
        assert len(entities) == len(positions), ('Number of entities must ' +
                                                 'match to number of positions')

        for i in range(len(entities)):
            curr_entity = entities[i]
            curr_pos = positions[i]
            self.addEntity(entity=curr_entity, position=curr_pos)

    def _getRESPower(self, generators, current_values=True):
        """
        Get the (aggregated) forecast of all renewable electricity generators.

        Parameters
        ----------
        current_values : bool, optional
            Defines, if only current horizon or all timesteps should be used.
            (default: True)
            False - Use complete number of timesteps
            True - Use horizon

        Returns
        -------
        power : np.array
            Power curve
        """
        if current_values:
            timesteps = self.environment.timer.timestepsHorizon
        else:
            timesteps = self.environment.timer.timestepsTotal

        power = np.zeros(timesteps)
        for generator in generators:
            power += generator.getPower(currentValues=current_values)

        return power

    def getPVPower(self, current_values=True):
        """
        Get the (aggregated) forecast of all (stand alone) pv units / pv farms.

        Parameters
        ----------
        current_values : bool, optional
            Defines, if only current horizon or all timesteps should be used.
            (default: True)
            False - Use complete number of timesteps
            True - Use horizon

        Returns
        -------
        pv_res_power : np.array
            Array with pv power values of all pv farms
        """

        if current_values:
            timesteps = self.environment.timer.timestepsHorizon
        else:
            timesteps = self.environment.timer.timestepsTotal

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
            return np.zeros(timesteps)
        else:
            return self._getRESPower(pv_entities, current_values=
                                     current_values)

    def getWindEnergyConverterPower(self, current_values=True):
        """
        Get the (aggregated) forecast of all wind energy converters.

        Parameters
        ----------
        current_values : bool, optional
            Defines, if only current horizon or all timesteps should be used.
            (default: True)
            False - Use complete number of timesteps
            True - Use horizon

        Returns
        -------
        wind_res_power : np.array
            Array with wind power values of all wind farms
        """

        if current_values:
            timesteps = self.environment.timer.timestepsHorizon
        else:
            timesteps = self.environment.timer.timestepsTotal

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
            return np.zeros(timesteps)
        else:
            return self._getRESPower(wind_entities, current_values=
                                     current_values)

    def get_power_curves(self, current_values=True):
        """ 
        Get the aggregated electricity and heat power forecast of all
        buildings.

        Returns tuple of electrical and thermal power array

        Parameters
        ----------
        current_values : bool, optional
            Defines, if only current horizon or all timesteps should be used.
            (default: True)
            False - Use complete number of timesteps
            True - Use horizon

        Order
        -----
        ElectricityDemand : Array_like
            Aggregated electrical demand
        HeatDemand : Array_like
            Aggregated heat demand
        """
        if current_values:
            timesteps = self.environment.timer.timestepsHorizon
        else:
            timesteps = self.environment.timer.timestepsTotal
        power_el = np.zeros(timesteps)
        power_th = np.zeros(timesteps)

        #  Loop over all nodes
        for n in self:
            #  If node holds attribute 'node_type'
            if 'node_type' in self.node[n]:
                #  If node_type is building
                if self.node[n]['node_type'] == 'building':
                    #  If entity is kind building
                    if self.node[n]['entity']._kind == 'building':
                        temp = self.node[n]['entity'].get_power_curves(
                            current_values=current_values)
                        power_el += temp[0]
                        power_th += temp[1]

        return (power_el, power_th)

    def get_aggr_space_h_power_curve(self, current_values=False):
        """
        Returns aggregated space heating power curve for all buildings
        within city district.

        Parameters
        ----------
        current_values : bool, optional
            Defines, if only current horizon or all timesteps should be used.
            (default: False)
            False - Use complete number of timesteps
            True - Use horizon

        Returns
        -------
        agg_th_p_curve : np.array
            Space heating thermal power curve in W per timestep
        """

        if current_values:  # Use horizon
            size = self.environment.timer.timestepsHorizon
        else:  # Use all timesteps
            size = self.environment.timer.timestepsTotal
        agg_th_p_curve = np.zeros(size)

        #  Loop over all nodes
        for n in self:
            #  If node holds attribute 'node_type'
            if 'node_type' in self.node[n]:
                #  If node_type is building
                if self.node[n]['node_type'] == 'building':
                    #  If entity is kind building
                    if self.node[n]['entity']._kind == 'building':
                        th_power_curve = self.node[n]['entity']. \
                            get_space_heating_power_curve(
                            current_values=current_values)[0:size]
                        agg_th_p_curve += th_power_curve

        return agg_th_p_curve

    def get_aggr_el_power_curve(self, current_values=False):
        """
        Returns aggregated electrical power curve for all buildings
        within city district.

        Parameters
        ----------
        current_values : bool, optional
            Defines, if only current horizon or all timesteps should be used.
            (default: False)
            False - Use complete number of timesteps
            True - Use horizon

        Returns
        -------
        agg_el_p_curve : np.array
            Electrical power curve in W per timestep
        """

        if current_values:  # Use horizon
            size = self.environment.timer.timestepsHorizon
        else:  # Use all timesteps
            size = self.environment.timer.timestepsTotal
        agg_el_p_curve = np.zeros(size)

        #  Loop over all nodes
        for n in self:
            #  If node holds attribute 'node_type'
            if 'node_type' in self.node[n]:
                #  If node_type is building
                if self.node[n]['node_type'] == 'building':
                    #  If entity is kind building
                    if self.node[n]['entity']._kind == 'building':
                        el_power_curve = self.node[n]['entity']. \
                            get_electric_power_curve(
                            current_values=current_values)[0:size]
                        agg_el_p_curve += el_power_curve

        return agg_el_p_curve

    def get_aggr_dhw_power_curve(self, current_values=False):
        """
        Returns aggregated domestic hot water (dhw) power curve for all
        buildings within city district.

        Parameters
        ----------
        current_values : bool, optional
            Defines, if only current horizon or all timesteps should be used.
            (default: False)
            False - Use complete number of timesteps
            True - Use horizon

        Returns
        -------
        agg_dhw_p_curve : np.array
            DHW power curve in W per timestep
        """

        if current_values:  # Use horizon
            size = self.environment.timer.timestepsHorizon
        else:  # Use all timesteps
            size = self.environment.timer.timestepsTotal
        agg_dhw_p_curve = np.zeros(size)

        #  Loop over all nodes
        for n in self:
            #  If node holds attribute 'node_type'
            if 'node_type' in self.node[n]:
                #  If node_type is building
                if self.node[n]['node_type'] == 'building':
                    #  If entity is kind building
                    if self.node[n]['entity']._kind == 'building':
                        dhw_power_curve = self.node[n]['entity']. \
                            get_dhw_power_curve(
                            current_values=current_values)[0:size]
                        agg_dhw_p_curve += dhw_power_curve

        return agg_dhw_p_curve

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
                        flowTemperature = np.maximum(flowTemperature,
                                                     flow_temp)

        return flowTemperature

    def get_nb_of_entities(self, entity_name):
        """
        Returns number of nodes of specific entity (e.g. "building", "pv",
        "windenergyconverter")

        Parameters
        ----------
        entity_name: str
            Standard entity names (building, windenergyconverter or pv)

        Returns
        -------
        nb_of_entities : int
            Number of nodes holding specific entity
        """
        assert entity_name in self.entity_name_list

        nb_of_entities = 0

        for n in self:
            #  If node holds attribute 'node_type'
            if 'node_type' in self.node[n]:
                #  If node_type is building
                if self.node[n]['node_type'] == 'building':
                    if 'entity' in self.node[n]:
                        #  If entity is of kind entity_name
                        if self.node[n]['entity']._kind == entity_name:
                            nb_of_entities += 1
        return nb_of_entities

    def get_node_numbers_of_entities(self, entity_name):
        """
        Returns list with node numbers, which hold specific kind of entity
        (e.g. "building", "pv", "windenergyconverter")

        Parameters
        ----------
        entity_name: str
            Standard entity names (building, windenergyconverter or pv)

        Returns
        -------
        node_nb_list : list (of ints)
            List holding node numbers
        """
        assert entity_name in self.entity_name_list

        node_nb_list = []

        for n in self:
            #  If node holds attribute 'node_type'
            if 'node_type' in self.node[n]:
                #  If node_type is building
                if self.node[n]['node_type'] == 'building':
                    if 'entity' in self.node[n]:
                        #  If entity is of kind entity_name
                        if self.node[n]['entity']._kind == entity_name:
                            node_nb_list.append(n)
        return node_nb_list

    def get_nb_of_building_entities(self):
        """
        Returns number of nodes holding entities of kind "building"
        (without PV- and windfarms).

        Returns
        -------
        nb_buildings : int
            Number of buildings
        """
        nb_buildings = self.get_nb_of_entities(entity_name='building')
        return nb_buildings

    def get_list_build_entity_node_ids(self):
        """
        Returns list with node ids holding building entities.
        (without PV- and windfarms)

        Returns
        -------
        build_node_id_list : list (of ints)
            List holding building entity node ids
        """
        build_node_id_list = self.get_node_numbers_of_entities(entity_name=
                                                               'building')
        return build_node_id_list
