# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 09:34:36 2015

@author: tsz
"""

import classes.Load
import numpy as np

class BuildingLoad(classes.Load.Load):
    """
    Implementation of a building load (electrical, domestic hot water and 
    space heating demand).
    """
    
    def __init__(self, environment, pathLoadcurve="", delimiter="\t", loadcurve=[], 
                 timeDiscretization=900, dataOnFile=True):
        """
        Parameters
        ----------
        environment : environment object
            Common to all other objects. Includes time and weather instances
        pathLoadcurve : string, optional
            Path to a file in which the load curve is stored
        delimiter : string, optional
            Delimiter used in the file specified in pathLoadcurve
        loadcurve : array-like, optional
            Instead of providing a path to a load curve, the load curve can 
            also be passed directly
        timeDiscretization : integer, optional
            Temporal discretization used in the given load curve (both, file 
            or direct)
        dataOnFile : Boolean, optional
            Use the provided path or use the provided load curve
        """
        
        if dataOnFile:
            super(BuildingLoad, self).__init__(environment, pathLoadcurve=pathLoadcurve, delimiter=delimiter, timeDiscretization=timeDiscretization, dataOnFile=dataOnFile)
        else:
            super(BuildingLoad, self).__init__(environment, pathLoadcurve="", loadcurve=loadcurve, timeDiscretization=timeDiscretization, dataOnFile=dataOnFile)
           
        self.currentLoad = np.zeros(environment.timer.timestepsHorizon)    
        self._kind = "buildingload"

    def getCurrentLoad(self):
        """ Return the currentLoad for the upcoming forecasting period """
        # Update current load
        self.updateCurrentLoad()
        
        # Return currentLoad
        return self.currentLoad
        
    def updateCurrentLoad(self):
        """ 
        Update (not return!) the currentLoad attribute for the entire forecast 
        horizon.
        """
        self.currentLoad = self.getFutureLoad()
        
        
        