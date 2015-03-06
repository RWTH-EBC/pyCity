# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 09:12:35 2015

@author: T_ohne_admin
"""

import classes.BuildingLoad

class SpaceHeating(classes.BuildingLoad.BuildingLoad):
    """
    Implementation of the space heating object
    """
    
    def __init__(self, environment, pathLoadcurve="", delimiter="\t", loadcurve=[], 
                 timeDiscretization=900, dataOnFile=True):
        """
        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        pathLoadcurve : String, optional
            Path to a file that holds the space heating curve
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
        super(SpaceHeating, self).__init__(environment, pathLoadcurve, delimiter, loadcurve, timeDiscretization, dataOnFile)
        self._kind = "spaceheating"