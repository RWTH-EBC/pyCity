# -*- coding: utf-8 -*-
"""
Created on Sat Feb 07 07:09:12 2015

@author: T_ohne_admin
"""

import numpy as np
import functions.changeResolution

class Load(object):
    """
    This class holds a load curve and is able to return it.
    """
    
    def __init__(self, environment, pathLoadcurve="", delimiter="\t", loadcurve=[], 
                 timeDiscretization=900, dataOnFile=True):
        """
        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        pathLoadcurve: String, optional
            Path to the file that holds the device's load curve 
        delimiter: String, optional
            used delimiter in file pathLoadcurve, e.g. "\t", ";", ","
        loadcurve: Array like, optional
            manual load curve
        timeDiscretization: integer, optional
            sampling rate of the load curve in seconds
        dataOnFile: Boolean, optional
            True: use path_loadcure, False: use loadcurve
        """
        self._kind = "load"
        self.environment = environment
        
        if dataOnFile:
            loadcurve = np.loadtxt(pathLoadcurve, delimiter=delimiter)
            if len(loadcurve.shape) == 2:
                # The input file has more than one column --> interpret the 
                # values from the second column as load curve
                loadcurve = loadcurve[:,1]

        if not timeDiscretization == environment.getTimeDiscretization():
            # If there is a difference between the standard time discretization
            # and the discretization of the input data, convert the inputs
            # to the desired time discretization
            loadcurve = functions.changeResolution.changeResolution(loadcurve, timeDiscretization, environment.getTimeDiscretization())

        self.loadcurve = np.array(loadcurve)
        
    def getFutureLoad(self):
        """
        This function only makes sense for electrical and thermal demands.
        In case of electrical appliances, loadcurve should be used directly!
        """
        currentPosition = self.environment.getCurrentTimestep()
        finalPosition = currentPosition + self.environment.getTimestepsHorizon()
        return self.loadcurve[currentPosition : finalPosition]
        
    def getLoadcurve(self):
        """ Return the load curve (array-like) """
        return self.loadcurve