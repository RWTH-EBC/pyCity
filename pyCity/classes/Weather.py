# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 17:11:19 2015

@author: tsz
"""

import numpy as np
import functions.changeResolution as changeResolution

class Weather(object):
    """
    Weather class keeps track of the weather data.
    In a real world setting, this would be the interface to a web-based
    weather forecast.
    """
        
    def __init__(self, timer, pathTRY="", pathTemperature="", pathDirectRadiation="", 
                 pathDiffuseRadiation="", pathWindspeed="", pathHumidity="", pathPressure="",
                 timeDiscretization=3600, delimiter="\t", useTRY=True):
        """
        Parameters
        ----------
        timer : Timer object 
            A pointer to the common timer object 
        pathTRY : String, optional if useTRY=False
            Path to a standard Test Reference Year file
            Example: "inputs\\weather\\TRY2011\\TRY2010_01_Jahr.dat"
        pathTemperature : String, optional if useTRY=True
            Path to the file that holds the ambient temperature values
        pathDirectRadiation : String, optional
            Path to the file that holds the values for direct solar radiation
        pathDiffuseRadiation : String, optional
            Path to the file that holds the values for diffuse solar radiation
        pathWindspeed : String, optional
            Path to the file that holds the values for wind speed
        pathHumidity : String, optional
            Path to the file that holds the values for relative humidity
        pathPressure : String, optional
            Path to the file that holds the values for diffuse solar radiation
        timeDiscretization : String, optional
            Time discretization of the input files in seconds
        delimiter : String, optional
            elimiter used in all files
            "\t" is tab-separated, "," is column separated...
        useTRY : Boolean, optional
            True: Read data from TRY file 
            False: Read data from other files. 
            Note, if useTRY=False: Only the ambient temperature is required!
        """

        self.timer = timer
        self._kind  = "weather"
        
        # Initialize current weather conditions
        self.currentTAmbient   = np.zeros(timer.timestepsHorizon)
        self.currentPAmbient   = np.zeros(timer.timestepsHorizon)
        self.currentPhiAmbient = np.zeros(timer.timestepsHorizon)
        self.currentVWind      = np.zeros(timer.timestepsHorizon)
        self.currentQDiffuse   = np.zeros(timer.timestepsHorizon)
        self.currentQDirect    = np.zeros(timer.timestepsHorizon)

        if useTRY:
            # Read TRY data
            TRYData = np.loadtxt(pathTRY, skiprows=38)

            # Save relevant weather data
            self.pAmbient   = TRYData[:, 9]
            self.phiAmbient = TRYData[:, 11]
            self.qDirect    = TRYData[:, 13]
            self.qDiffuse   = TRYData[:, 14]
            self.tAmbient   = TRYData[:, 8]
            self.vWind      = TRYData[:, 7]

        else:
            # If the data is not provided via TRY, load each file separately
            def readTXT(path, delimiter):
                if not path == "":
                    result = np.loadtxt(path, delimiter=delimiter)
                else:
                    result = np.zeros(timer.timestepsTotal)
                return result
            
            self.tAmbient   = readTXT(pathTemperature)
            self.qDirect    = readTXT(pathDirectRadiation)
            self.qDiffuse   = readTXT(pathDiffuseRadiation)
            self.vWind      = readTXT(pathWindspeed)
            self.phiAmbient = readTXT(pathHumidity)
            self.pAmbient   = readTXT(pathPressure)

                           
        if not timeDiscretization == self.timer.timeDiscretization:
            # If there is a difference between the standard time discretization
            # and the discretization of the input data, convert the inputs
            # to the desired time discretization
            self.tAmbient   = changeResolution.changeResolution(self.tAmbient,   timeDiscretization, self.timer.timeDiscretization)
            self.qDirect    = changeResolution.changeResolution(self.qDirect,    timeDiscretization, self.timer.timeDiscretization)
            self.qDiffuse   = changeResolution.changeResolution(self.qDiffuse,   timeDiscretization, self.timer.timeDiscretization)
            self.vWind      = changeResolution.changeResolution(self.vWind,      timeDiscretization, self.timer.timeDiscretization)
            self.phiAmbient = changeResolution.changeResolution(self.phiAmbient, timeDiscretization, self.timer.timeDiscretization)
            self.pAmbient   = changeResolution.changeResolution(self.pAmbient,   timeDiscretization, self.timer.timeDiscretization)
    
    def _getWeatherData(self, fromTimestep, toTimestep, getTAmbient, getQDirect, getQDiffuse, getVWind, getPhiAmbient, getPAmbient):
        """
        Get the weather data between two specified time steps
        
        Parameters
        ----------
        fromTimestep : Integer
            Starting time step
        toTimestep : Integer
            Ending time step
        getTAmbient : Boolean
            If True, return current ambient temperature
        getQDirect : Boolean
            If True, return current direct radiation
        getQDiffuse : Boolean
            If True, return current diffuse radiation
        getVWind : Boolean
            If True, return current wind velocity
        getPhiAmbient : Boolean
            If True, return relative humidity
        getPAmbient : Boolean
            If True, return ambient pressure    
        """
        # Initialize results tuple
        result = ()        
        
        # Append values to the 'result' if required
        def requireValue(request, current_values, total_values):
            if request:
                current_values = total_values[fromTimestep : toTimestep]
                return (current_values,)
            else:                    
                return ()
        
        # Check if value is required
        result += requireValue(getTAmbient,   self.currentTAmbient,   self.tAmbient)
        result += requireValue(getQDirect,    self.currentQDirect,    self.qDirect)
        result += requireValue(getQDiffuse,   self.currentQDiffuse,   self.qDiffuse)
        result += requireValue(getVWind,      self.currentVWind,      self.vWind)
        result += requireValue(getPhiAmbient, self.currentPhiAmbient, self.phiAmbient)
        result += requireValue(getPAmbient,   self.currentPAmbient,   self.pAmbient)
        
        # Return results
        return result
        
    def getWeatherForecast(self, getTAmbient=True, getQDirect=True, getQDiffuse=True, getVWind=True, getPhiAmbient=True, getPAmbient=True):
        """
        Get the current weather forecast
        
        Parameters
        ----------
        getTAmbient : Boolean, optional
            If True, return current ambient temperature
        getQDirect : Boolean, optional
            If True, return current direct radiation
        getQDiffuse : Boolean, optional
            If True, return current diffuse radiation
        getVWind : Boolean, optional
            If True, return current wind velocity
        getPhiAmbient : Boolean, optional
            If True, return relative humidity
        getPAmbient : Boolean, optional
            If True, return ambient pressure
            
        Return
        ------
        The result is returned as a tuple
        """
        # Get current and final position
        currentPosition = self.timer.currentTimestep
        finalPosition = currentPosition + self.timer.timestepsHorizon
        
        return self._getWeatherData(currentPosition, finalPosition, getTAmbient, getQDirect, getQDiffuse, getVWind, getPhiAmbient, getPAmbient)
        
    def getPreviousWeather(self, fromTimestep=0, numberTimesteps=0, useTimesteps=True, getTAmbient=True, getQDirect=True, getQDiffuse=True, getVWind=True, getPhiAmbient=True, getPAmbient=True):
        """
        Get previous weather data from 'fromTimestep' up to the current timestep
        
        Parameters
        ----------
        fromTimestep : Integer, optional
            Get weather data from THIS timestep until the current timestep
        numberTimesteps : Integer, optional
            Get weather data for the last numberTimesteps days
        useTimesteps : Boolean, optional
            True: use fromTimestep 
            False: use numberTimesteps
        getTAmbient : Boolean, optional
            If True, return current ambient temperature
        getQDirect : Boolean, optional
            If True, return current direct radiation
        getQDiffuse : Boolean, optional
            If True, return current diffuse radiation
        getVWind : Boolean, optional
            If True, return current wind velocity
        getPhiAmbient : Boolean, optional
            If True, return relative humidity
        getPAmbient : Boolean, optional
            If True, return ambient pressure
            
        Return
        ------
        The result is returned as a tuple
        """
        if not useTimesteps:
            fromTimestep = self.timer.currentTimestep - numberTimesteps
        return self._getWeatherData(fromTimestep, self.timer.currentTimestep, getTAmbient, getQDirect, getQDiffuse, getVWind, getPhiAmbient, getPAmbient)
        