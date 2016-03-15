#!/usr/bin/env python
# coding=utf-8
"""
Functions to help processing city district graphs
"""

import copy


def get_subcity(city, nodelist):
    """
    Returns (copied) subgraph of city object, only holding building nodes
    within nodelist building.
    Important: Returned subgraph is copy of (sub)graph!

    Raises assertion error, if nodes in nodelist are not
    building nodes. Does not include network or street nodes.

    Parameters
    ----------
    city : city object
        City object of pycity
    nodelist : list
        List of building node ids, which should be extracted

    Returns
    -------
    subcity : city object
        City object (only including chosen building nodes)
    """

    #  Check if all node ids in nodelist are within nodelist_building
    for node in nodelist:
        assert node in city.nodelist_building

    #  Initialize street_graph as deepcopy of self.city
    city_copy = copy.deepcopy(city)

    #  Get subgraph (only holding nodes within nodelist)
    subcity = city_copy.subgraph(nodelist)

    #  Readd environment pointer
    subcity.environment = city.environment

    return subcity
