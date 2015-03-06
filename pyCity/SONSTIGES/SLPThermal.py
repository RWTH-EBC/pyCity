# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 15:13:42 2015

@author: tsz
"""

import numpy as np
import functions.changeResolution

class SLPThermal(object):
    """
    Object that holds the thermal standard load profile and is able to return 
    a scaled version.
    """
   
    def __init__(self, environment, pathSFH="", pathMFH="", timeDiscretization=3600, dataJoule=True, useStandardSLP=True):
        """
        Constructor of the thermal standard load profile
        
        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        pathSFH : String, optional
            Path to a specific SLP profile of single family houses.
            This parameter is optional, as there is already a path hard-coded.
        pathMFH : String, optional
            Path to a specific SLP profile of multi family houses.
            This parameter is optional, as there is already a path hard-coded.
        timeDiscretization : Integer, optional
            Time discretization of the given data
        dataJoule : Boolean, optional
            True: Data is provided in Joule
            False: Data is provided in Watt
        useStandardSLP : Boolean, optional
            True: use the hard-coded standard load profile
            False: use an alternatively provided thermal standard load profile
        """
        # If the standard SLP path is used, overwrite the given pathSLP
        if useStandardSLP:
            # Reset timeDiscretization and dataJoule
            timeDiscretization = 3600
            dataJoule = True
            # Use standard paths
            pathSFH = "inputs\\slp_thermal_sfh.csv"
            pathMFH = "inputs\\slp_thermal_mfh.csv"
            
        # Load the standard load profile
        # The data is tab-separated
        # The first line is a header (skiprows=1)
        demandSFH = np.loadtxt(pathSFH, delimiter="\t", skiprows=1)
        demandMFH = np.loadtxt(pathMFH, delimiter="\t", skiprows=1)
        
        # In case the time discretization does not comply with the 
        # environment's time discretization, adjust the profile
        commonTimeDiscretization = environment.getTimeDiscretization()
        if not timeDiscretization == commonTimeDiscretization:
            # Adjust demands
            if dataJoule:
                demandSFH = functions.changeResolution.changeResolution(demandSFH, timeDiscretization, commonTimeDiscretization, "sum")
                demandMFH = functions.changeResolution.changeResolution(demandMFH, timeDiscretization, commonTimeDiscretization, "sum")
                demandSFH = demandSFH / commonTimeDiscretization
                demandMFH = demandMFH / commonTimeDiscretization
            else:
                demandSFH = functions.changeResolution.changeResolution(demandSFH, timeDiscretization, commonTimeDiscretization, "mean")
                demandMFH = functions.changeResolution.changeResolution(demandMFH, timeDiscretization, commonTimeDiscretization, "mean")
            
        self.demandSFH = demandSFH  # in Watt
        self.demandMFH = demandMFH  # in Watt
        self.environment = environment
        
    def getDemandCurve(self, scalingFactor, singleFamilyHouse=True, currentDemand=True):
        """
        Return the (scaled) standard load curve.
        
        Parameter
        ---------
        scalingFactor: Float
            Factor for scaling the standard load profile curve
        singleFamilyHouse : Boolean, optional
            True:  Return the single family curve
            False: Return the multi family curve
        currentDemand : Boolean, optional
            True: Return the current demand
            False: Return the entire demand curve
        """
        if singleFamilyHouse:
            if currentDemand:
                result = self._getCurrentCurve(self.demandSFH)
            else:
                result = self.demandSFH
        else:
            if currentDemand:
                result = self._getCurrentCurve(self.demandMFH)
            else:
                result = self.demandMFH
                
        return result * scalingFactor
        
    def _getCurrentCurve(self, curve):
        """
        Get the current SLP curve
        """
        currentTimestep = self.environment.getCurrentTimestep()
        finalTimestep = currentTimestep + self.environment.getTimestepsHorizon()
        return curve[currentTimestep : finalTimestep]
