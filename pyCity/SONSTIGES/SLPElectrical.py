# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 15:12:45 2015

@author: tsz
"""

import numpy as np
import functions.changeResolution

class SLPElectrical(object):
    """
    Object that holds the electrical standard load profile and is able to
    return a scaled version.
    """
   
    def __init__(self, environment, path="", timeDiscretization=900, dataJoule=True, useStandardSLP=True):
        """
        Constructor of the electrical standard load profile
        
        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        path : String, optional
            Path to a specific SLP profile.
            This parameter is optional, as there is already a path hard-coded.
        timeDiscretization : Integer, optional
            Time discretization of the given data
        dataJoule : Boolean, optional
            True: Data is provided in Joule
            False: Data is provided in Watt
        useStandardSLP : Boolean, optional
            True: use the hard-coded standard load profile
            False: use an alternatively provided standard load profile
        """
        # If the standard SLP path is used, overwrite the given pathSLP
        if useStandardSLP:
            # Reset timeDiscretization and dataJoule
            timeDiscretization = 900
            dataJoule = True
            # Use standard paths
            path = "inputs\\slp_electrical.csv"
            
        # Load the standard load profile
        # The data is tab-separated
        # The first line is a header (skiprows=1)
        demand = np.loadtxt(path, delimiter="\t", skiprows=1)
        
        # In case the time discretization does not comply with the 
        # environment's time discretization, adjust the profile
        commonTimeDiscretization = environment.getTimeDiscretization()
        if not timeDiscretization == commonTimeDiscretization:
            # Adjust demands
            if dataJoule:
                demand = functions.changeResolution.changeResolution(demand, timeDiscretization, commonTimeDiscretization, "sum")
                demand = demand / commonTimeDiscretization
            else:
                demand = functions.changeResolution.changeResolution(demand, timeDiscretization, commonTimeDiscretization, "mean")
                
        self.demand = demand
        self.environment = environment
        
    def getDemandCurve(self, scalingFactor, currentDemand=True):
        """
        Return the (scaled) standard load curve.
        
        Parameter
        ---------
        scalingFactor: Float
            Factor for scaling the standard load profile curve
        currentDemand : Boolean, optional
            True: Return the current demand
            False: Return the entire demand curve
        """
        if currentDemand:
            result = self._getCurrentCurve(self.demand)
        else:
            result = self.demand
                
        return result * scalingFactor
        
    def _getCurrentCurve(self, curve):
        """
        Get the current SLP curve
        """
        currentTimestep = self.environment.getCurrentTimestep()
        finalTimestep = currentTimestep + self.environment.getTimestepsHorizon()
        return curve[currentTimestep : finalTimestep]
