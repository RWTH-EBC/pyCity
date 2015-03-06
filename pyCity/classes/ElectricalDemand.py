# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 09:12:18 2015

@author: T_ohne_admin
"""

import classes.BuildingLoad

class ElectricalDemand(classes.BuildingLoad.BuildingLoad):
    """
    Implementation of the electrical demand object
    """
    
    def __init__(self, environment, pathLoadcurve="", delimiter="\t", loadcurve=[], 
                 timeDiscretization=900, dataOnFile=True):
        """
        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        pathLoadcurve : String, optional
            Path to a file that holds the electricity demand curve
        delimiter : String, optional
            Delimiter used in the file defined with pathLoadcurve
        loadcurve : Array-like, optional
            Instead of via pathLoadcurve, the load curve can be defined 
            directly
        timeDiscretization : Integer, optional
            Temporal discretization of the data provided in pathLoadcurve or
            loadcurve
        dataOnFile : Boolean, optional
            If True: Use pathLoadcurve to get the load curve
            If False: Use loadcurve directly
        """
        super(ElectricalDemand, self).__init__(environment, pathLoadcurve, delimiter, loadcurve, timeDiscretization, dataOnFile)
        self._kind = "electricaldemand"