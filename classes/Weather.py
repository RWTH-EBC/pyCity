#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 17:11:19 2015

@author: tsz
"""


import os
import numpy as np
import functions.changeResolution as changeResolution
import classes.Sun

class Weather(classes.Sun.Sun):
    """
    Weather class keeps track of the weather data.
    In a real world setting, this would be the interface to a web-based
    weather forecast.
    """
        
    def __init__(self, timer, 
                 pathTRY='inputs/weather/TRY2010_05_Jahr.dat',
                 pathTemperature="", pathDirectRadiation="", 
                 pathDiffuseRadiation="", pathWindspeed="", pathHumidity="", 
                 pathPressure="", pathCloudiness="",
                 timeDiscretization=3600, delimiter="\t", useTRY=True,
                 location=(50.76, 6.07), heightVelocityMeasurement=10):
        """
        Parameters
        ----------
        timer : Timer object 
            A pointer to the common timer object 
        pathTRY : String, optional if useTRY=False
            Path to a standard Test Reference Year file
            Example: "inputs/weather/TRY2010_05_Jahr.dat"
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
            Path to the file that holds the values for ambient pressure
        pathCloudiness : String, optional
            Path to the file that holds the values for the cloudiness
        timeDiscretization : String, optional
            Time discretization of the input files in seconds
        delimiter : String, optional
            elimiter used in all files
            "\t" is tab-separated, "," is column separated...
        useTRY : Boolean, optional
            True: Read data from TRY file 
            False: Read data from other files. 
            Note, if useTRY=False: Only the ambient temperature is required!
        location : Tuple, optional
            (longitude, latitude) of the simulated system's position. Standard
            values (50.76, 6.07) represent Aachen, Germany.
        heightVelocityMeasurement : Float, optional
            At which height is the wind velocity measured? (10 meters for
            German test reference years).
        """

        super(Weather, self).__init__(timer, location)
        self._kind  = "weather"
        
        self.heightVelocityMeasurement = heightVelocityMeasurement
        
        # Initialize current weather conditions
        self.currentTAmbient   = np.zeros(timer.timestepsHorizon)
        self.currentPAmbient   = np.zeros(timer.timestepsHorizon)
        self.currentPhiAmbient = np.zeros(timer.timestepsHorizon)
        self.currentVWind      = np.zeros(timer.timestepsHorizon)
        self.currentQDiffuse   = np.zeros(timer.timestepsHorizon)
        self.currentQDirect    = np.zeros(timer.timestepsHorizon)
        self.currentCloudiness = np.zeros(timer.timestepsHorizon)

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
            self.cloudiness = TRYData[:, 5]
            
            # Read TRY number
            with open(pathTRY, "rb") as data:
                first_line = data.readline()
            self.try_number = first_line[3] + first_line[4]

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
            self.cloudiness = readTXT(pathCloudiness)
            self.try_number = "00"

                           
        if not timeDiscretization == self.timer.timeDiscretization:
            # If there is a difference between the standard time discretization
            # and the discretization of the input data, convert the inputs
            # to the desired time discretization
            changeRes = changeResolution.changeResolution
            self.tAmbient = changeRes(self.tAmbient, timeDiscretization, 
                                      self.timer.timeDiscretization)
            self.qDirect = changeRes(self.qDirect, timeDiscretization, 
                                     self.timer.timeDiscretization)
            self.qDiffuse = changeRes(self.qDiffuse, timeDiscretization, 
                                      self.timer.timeDiscretization)
            self.vWind = changeRes(self.vWind, timeDiscretization, 
                                   self.timer.timeDiscretization)
            self.phiAmbient = changeRes(self.phiAmbient, timeDiscretization, 
                                        self.timer.timeDiscretization)
            self.pAmbient = changeRes(self.pAmbient, timeDiscretization, 
                                      self.timer.timeDiscretization)
            self.cloudiness = changeRes(self.cloudiness, timeDiscretization, 
                                      self.timer.timeDiscretization)
    
    def getRadiationTiltedSurface(self, beta, gamma, albedo=0.3, update=False):
        """
        beta : float
            Slope, the angle (in degree) between the plane of the surface in 
            question and the horizontal. 0 <= beta <= 180. If beta > 90, the 
            surface faces downwards.
        gamma : float
            Surface azimuth angle. The deviation of the projection on a 
            horizontal plane of the normal to the surface from the local 
            meridian, with zero due south, east negative, and west positive.
            -180 <= gamma <= 180
        albedo : float, optional
            Average value on earth: 0.3
            Ground reflectance. 0 <= albedo <= 1
        update : Boolean, optional
            If True, air mass, extraterrestrial radiation, delta, omega and 
            thetaZ are updated before computing the total radiation on the
            tilted surface.
        """
        # Get radiation
        radiation = self.getWeatherForecast(getQDirect=True, getQDiffuse=True)
        (beam, diffuse) = radiation
        
        # Return total radiation on a given tilted surface
        return self.getTotalRadiationTiltedSurface(beamRadiation=beam,
                                                   diffuseRadiation=diffuse,
                                                   beta=beta, 
                                                   gamma=gamma, 
                                                   albedo=albedo, 
                                                   update=update)
    
    def _getWeatherData(self, 
                        fromTimestep, 
                        toTimestep, 
                        getTAmbient, 
                        getQDirect, 
                        getQDiffuse, 
                        getVWind, 
                        getPhiAmbient, 
                        getPAmbient,
                        getCloudiness):
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
        getCloudiness : Boolean
            If Ture, return cloudiness
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
        result += requireValue(getTAmbient,
                               self.currentTAmbient,   
                               self.tAmbient)
        result += requireValue(getQDirect,    
                               self.currentQDirect,    
                               self.qDirect)
        result += requireValue(getQDiffuse,   
                               self.currentQDiffuse,   
                               self.qDiffuse)
        result += requireValue(getVWind,      
                               self.currentVWind,      
                               self.vWind)
        result += requireValue(getPhiAmbient, 
                               self.currentPhiAmbient, 
                               self.phiAmbient)
        result += requireValue(getPAmbient,   
                               self.currentPAmbient,   
                               self.pAmbient)
        
        # Return results
        return result
        
    def getWeatherForecast(self, 
                           getTAmbient=False, 
                           getQDirect=False, 
                           getQDiffuse=False, 
                           getVWind=False, 
                           getPhiAmbient=False,
                           getPAmbient=False,
                           getCloudiness=False):
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
        getCloudiness : Boolean
            If Ture, return cloudiness
            
        Return
        ------
        The result is returned as a tuple
        """
        # Get current and final position
        currentPosition = self.timer.currentTimestep
        finalPosition = currentPosition + self.timer.timestepsHorizon
        
        return self._getWeatherData(currentPosition, 
                                    finalPosition, 
                                    getTAmbient, 
                                    getQDirect, 
                                    getQDiffuse, 
                                    getVWind, 
                                    getPhiAmbient, 
                                    getPAmbient,
                                    getCloudiness)
        
    def getPreviousWeather(self, 
                           fromTimestep=0, 
                           numberTimesteps=0, 
                           useTimesteps=True, 
                           getTAmbient=False, 
                           getQDirect=False, 
                           getQDiffuse=False, 
                           getVWind=False, 
                           getPhiAmbient=False, 
                           getPAmbient=False,
                           getCloudiness=False):
        """
        Get previous weather data from ``fromTimestep`` up to the current 
        timestep
        
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
        getCloudiness : Boolean
            If Ture, return cloudiness
            
        Return
        ------
        The result is returned as a tuple
        """
        if not useTimesteps:
            fromTimestep = max(0, self.timer.currentTimestep - numberTimesteps)
        return self._getWeatherData(fromTimestep, 
                                    self.timer.currentTimestep, 
                                    getTAmbient, 
                                    getQDirect, 
                                    getQDiffuse, 
                                    getVWind, 
                                    getPhiAmbient, 
                                    getPAmbient,
                                    getCloudiness)
        