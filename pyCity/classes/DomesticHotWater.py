# -*- coding: utf-8 -*-
"""
Created on Sun Feb 08 22:39:15 2015

@author: T_ohne_admin
"""

import BuildingLoad
import numpy as np

class DomesticHotWater(BuildingLoad.BuildingLoad):
    """
    Implementation of the domestic hot water (DHW) object
    """

    def __init__(self, environment, tFlowMin, thermal=True, pathLoadcurve="", 
                 delimiter="\t", loadcurve=[], timeDiscretization=900, dataOnFile=True):
        """
        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        tFlowMin : Float
            Required flow temperature if domestic hot water is required
        thermal : Boolean, optional
            Is the DHW provided electrically (False) or via thermal energy 
            storage (True)
        pathLoadcurve : String, optional
            Path to a file that holds the domestic hot water demand curve
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
        
        if dataOnFile:
            super(DomesticHotWater,self).__init__(environment, pathLoadcurve=pathLoadcurve, delimiter=delimiter, timeDiscretization=timeDiscretization, dataOnFile=dataOnFile)
        else:
            super(DomesticHotWater,self).__init__(environment, pathLoadcurve="", loadcurve=loadcurve, timeDiscretization=timeDiscretization, dataOnFile=dataOnFile)
        self._kind = "domestichotwater"
        self.tFlowMin = tFlowMin
        self.thermal = thermal
        self.currentTFlow = np.zeros(environment.getTimestepsHorizon())
        
    def getTemperature(self):
        """ Return the required flow temperature """
        # Update demand
        self.updateCurrentLoad()
        
        # Every time, the demand is positive, tFlowMin is required
        self.currentTFlow = np.zeros(self.environment.getTimestepsHorizon())
        self.currentTFlow[self.currentLoad > 0] = self.tFlowMin
        
        return self.currentTFlow
        
    def getThermalOrElectrical(self):
        """ 
        Return whether DHW is provided via the thermal energy storage unit 
        (True) or electrically (False) 
        """
        return self.thermal
    

