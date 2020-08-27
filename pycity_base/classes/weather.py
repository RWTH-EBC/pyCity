#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 17:11:19 2015

@author: tsz
"""

from __future__ import division

import os
import numpy as np
import pycity_base.classes.sun
from pycity_base.functions import change_resolution as chres


class Weather(pycity_base.classes.sun.Sun):
    """
    Weather class keeps track of the weather data.
    In a real world setting, this would be the interface to a web-based
    weather forecast.
    """

    def __init__(self, timer,
                 path_TRY=None, path_TMY3=None, new_try=False,
                 path_temperature="", path_direct_radiation="",
                 path_diffuse_radiation="", path_wind_speed="", path_humidity="",
                 path_pressure="", path_cloudiness="",
                 time_discretization=3600, delimiter="\t",
                 use_TRY=True, use_TMY3=False,
                 location=(50.76, 6.07), height_velocity_measurement=10,
                 altitude=152.0, time_zone=1):
        """
        Parameters
        ----------
        timer : Timer object 
            A pointer to the common timer object 
        path_TRY : String, optional if use_TRY=False.
            Path to a standard Test Reference Year file
            Default value is None. If default value is set, TRY2010_05_Jahr.dat is used.
            Example: "inputs/weather/TRY2010_05_Jahr.dat"
        path_TMY3 : String, optional if use_TMY3=False.
            Path to a standard Test Reference Year file
            Default value is None. If default value is set, data for New York 
            City, JFK airport
            Example: "inputs/weather/tmy3_744860_new_york_jfk_airport.csv"
        new_try : bool, optional
            Defines, if TRY dataset have been generated after 2017 (default: False)
            If False, assumes that TRY dataset has been generated before 2017.
            If True, assumes that TRY dataset has been generated after 2017 and
            belongs to the new TRY classes. This is important for extracting
            the correct values from the TRY dataset!
        path_temperature : String, optional if use_TRY=True or use_TMY3=True
            Path to the file that holds the ambient temperature values
        path_direct_radiation : String, optional
            Path to the file that holds the values for direct solar radiation
        path_diffuse_radiation : String, optional
            Path to the file that holds the values for diffuse solar radiation
        path_wind_speed : String, optional
            Path to the file that holds the values for wind speed
        path_humidity : String, optional
            Path to the file that holds the values for relative humidity
        path_pressure : String, optional
            Path to the file that holds the values for ambient pressure
        path_cloudiness : String, optional
            Path to the file that holds the values for the cloudiness
        time_discretization : String, optional
            Time discretization of the input files in seconds
        delimiter : String, optional
            elimiter used in all files
            "\t" is tab-separated, "," is column separated...
        use_TRY : Boolean, optional
            True: Read data from TRY file
            False: Read data from other files.
        use_TMY3 : Boolean, optional
            True: Read data from TMY3 file 
            False: Read data from other files. 
        location : Tuple, optional
            (latitude, longitude) of the simulated system's position. Standard
            values (50.76, 6.07) represent Aachen, Germany.
        height_velocity_measurement : Float, optional
            At which height is the wind velocity measured? (10 meters for
            German test reference years).
        altitude : float, optional
            The locations altitude in meters.
        time_zone : integer, optional
            Shift between the location's time and GMT in hours. CET is 1.
            Daylight savings time is neglected.
        """

        super(Weather, self).__init__(timer, location, time_zone, altitude)
        self._kind = "weather"
        self.weather_dataset_name = ""
        self.try_number = "00"

        self.height_velocity_measurement = height_velocity_measurement

        # Initialize current weather conditions
        self.current_t_ambient = np.zeros(timer.timesteps_horizon)
        self.current_p_ambient = np.zeros(timer.timesteps_horizon)
        self.current_phi_ambient = np.zeros(timer.timesteps_horizon)
        self.current_v_wind = np.zeros(timer.timesteps_horizon)
        self.current_q_diffuse = np.zeros(timer.timesteps_horizon)
        self.current_q_direct = np.zeros(timer.timesteps_horizon)
        self.current_cloudiness = np.zeros(timer.timesteps_horizon)
        self.current_rad_sky = np.zeros(timer.timesteps_horizon)
        self.current_rad_earth = np.zeros(timer.timesteps_horizon)

        #  Calculate number of rows, which should be loaded into weather class
        nb_rows = int(8760 * 3600 / time_discretization)

        if use_TRY:

            if new_try is False:
                # Generate TRY path (if path is None) and use TRY2010_05_Jahr.dat
                if path_TRY is None:
                    src_path = os.path.dirname(os.path.dirname(__file__))
                    path_TRY = os.path.join(src_path,
                                            'inputs',
                                            'weather',
                                            'TRY2010_05_Jahr.dat')

                # Read TRY data
                TRYData = np.genfromtxt(path_TRY, skip_header=38, encoding="utf-8")

                # Save relevant weather data (only extract row 0 to 8760)
                self.p_ambient = TRYData[0:nb_rows, 9]
                self.phi_ambient = TRYData[0:nb_rows, 11]
                self.q_direct = TRYData[0:nb_rows, 13]
                self.q_diffuse = TRYData[0:nb_rows, 14]
                self.t_ambient = TRYData[0:nb_rows, 8]
                self.v_wind = TRYData[0:nb_rows, 7]
                self.cloudiness = TRYData[0:nb_rows, 5]
                self.rad_sky = TRYData[0:nb_rows, 16]
                self.rad_earth = TRYData[0:nb_rows, 17]

                # Read TRY number
                with open(path_TRY, "rb") as data:
                    first_line = data.readline()
                self.try_number = first_line[3] + first_line[4]

            else:
                #  New TRY dataset (after 2017)
                if path_TRY is None:
                    msg = 'path_TRY cannot be None.'
                    raise AssertionError(msg)

                # Read TRY data
                TRYData = np.genfromtxt(path_TRY, skip_header=34, encoding="utf-8")

                # Save relevant weather data (only extract row 0 to 8760)
                self.p_ambient = TRYData[0:nb_rows, 6]
                self.phi_ambient = TRYData[0:nb_rows, 11]
                self.q_direct = TRYData[0:nb_rows, 12]
                self.q_diffuse = TRYData[0:nb_rows, 13]
                self.t_ambient = TRYData[0:nb_rows, 5]
                self.v_wind = TRYData[0:nb_rows, 8]
                self.cloudiness = TRYData[0:nb_rows,9]
                self.rad_sky = TRYData[0:nb_rows, 14]
                self.rad_earth = TRYData[0:nb_rows, 15]

                # Read TRY number
                with open(path_TRY, "rb") as data:
                    first_line = data.readline()
                self.try_number = first_line[3] + first_line[4]

            self.weather_dataset_name = ((str(path_TRY).replace('\\', '/')).split("/")[-1]).split(".")[0]

        elif use_TMY3:
            # Generate TMY3 path (if path is None) and use 
            # tmy3_744860_new_york_jfk_airport.csv
            if path_TMY3 is None:
                src_path = os.path.dirname(os.path.dirname(__file__))
                path_TMY3 = os.path.join(src_path,
                                         'inputs',
                                         'weather',
                                         'tmy3_744860_new_york_jfk_airport.csv')

            weather_data = np.genfromtxt(path_TMY3, skip_header=2, delimiter=",",
                                         usecols=(4, 7, 10, 25, 31, 37, 40, 46),
                                         encoding="utf-8")

            self.p_ambient = weather_data[0:nb_rows, 6]
            self.phi_ambient = weather_data[0:nb_rows, 5]
            self.t_ambient = weather_data[0:nb_rows, 4]
            self.v_wind = weather_data[0:nb_rows, 7]
            self.cloudiness = weather_data[0:nb_rows, 3]

            globalHorIrrad = weather_data[0:nb_rows, 0]
            directNormalIrrad = weather_data[0:nb_rows, 1]

            self.computeGeometry(allTimeSteps=True)
            changeRes = chres.changeResolution

            old_res = (3600 * 24 * 365)/len(self.theta_z)

            thetaZ = changeRes(self.theta_z,
                               oldResolution=old_res,
                               newResolution=time_discretization)

            self.q_direct = directNormalIrrad * np.cos(np.radians(thetaZ))
            self.q_diffuse = np.maximum(0, globalHorIrrad - self.q_direct)

            self.weather_dataset_name = ((str(path_TMY3).replace('\\', '/')).split("/")[-1]).split(".")[0]

        else:  # pragma: no cover
            # If the data is not provided via TRY, load each file separately
            def readTXT(path, delimiter):
                if not path == "":
                    result = np.loadtxt(path, delimiter=delimiter)
                else:
                    result = np.zeros(timer.timesteps_total)
                return result

            self.t_ambient = readTXT(path_temperature, delimiter)
            self.q_direct = readTXT(path_direct_radiation, delimiter)
            self.q_diffuse = readTXT(path_diffuse_radiation, delimiter)
            self.v_wind = readTXT(path_wind_speed, delimiter)
            self.phi_ambient = readTXT(path_humidity, delimiter)
            self.p_ambient = readTXT(path_pressure, delimiter)
            self.cloudiness = readTXT(path_cloudiness, delimiter)

        if not time_discretization == self.timer.time_discretization:
            # If there is a difference between the standard time discretization
            # and the discretization of the input data, convert the inputs
            # to the desired time discretization
            changeRes = chres.changeResolution
            self.t_ambient = changeRes(self.t_ambient, time_discretization,
                                       self.timer.time_discretization)
            self.q_direct = changeRes(self.q_direct, time_discretization,
                                      self.timer.time_discretization)
            self.q_diffuse = changeRes(self.q_diffuse, time_discretization,
                                       self.timer.time_discretization)
            self.v_wind = changeRes(self.v_wind, time_discretization,
                                    self.timer.time_discretization)
            self.phi_ambient = changeRes(self.phi_ambient, time_discretization,
                                         self.timer.time_discretization)
            self.p_ambient = changeRes(self.p_ambient, time_discretization,
                                       self.timer.time_discretization)
            self.cloudiness = changeRes(self.cloudiness, time_discretization,
                                        self.timer.time_discretization)
            if use_TRY:
                self.rad_sky = changeRes(self.rad_sky,
                                         time_discretization,
                                         self.timer.time_discretization)
                self.rad_earth = changeRes(self.rad_earth,
                                           time_discretization,
                                           self.timer.time_discretization)

    @property
    def kind(self):
        return self._kind

    def getRadiationTiltedSurface(self, beta, gamma, albedo=0.3, update=False,
                                  currentValues=True):
        """
        Calculates radiation on tilted surface

        Parameters
        ----------
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
            theta_z are updated before computing the total radiation on the
            tilted surface.
        currentValues : bool, optional
            If True, returns values of current horizon (default: True).
            If False, returns annual values.
        """
        # Get radiation
        radiation = self.getWeatherForecast(getQDirect=True, getQDiffuse=True,
                                            currentValues=currentValues)
        (beam, diffuse) = radiation

        # Return total radiation on a given tilted surface
        return self.getTotalRadiationTiltedSurface(beamRadiation=beam,
                                                   diffuseRadiation=diffuse,
                                                   beta=beta,
                                                   gamma=gamma,
                                                   albedo=albedo,
                                                   update=update,
                                                   currentValues=currentValues)

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
        def requireValue(request, currentValues, totalValues):
            if request:
                currentValues = totalValues[fromTimestep: toTimestep]
                return (currentValues,)
            else:
                return ()

        # Check if value is required
        result += requireValue(getTAmbient,
                               self.current_t_ambient,
                               self.t_ambient)
        result += requireValue(getQDirect,
                               self.current_q_direct,
                               self.q_direct)
        result += requireValue(getQDiffuse,
                               self.current_q_diffuse,
                               self.q_diffuse)
        result += requireValue(getVWind,
                               self.current_v_wind,
                               self.v_wind)
        result += requireValue(getPhiAmbient,
                               self.current_phi_ambient,
                               self.phi_ambient)
        result += requireValue(getPAmbient,
                               self.current_p_ambient,
                               self.p_ambient)

        # Return results
        return result

    def getWeatherForecast(self,
                           getTAmbient=False,
                           getQDirect=False,
                           getQDiffuse=False,
                           getVWind=False,
                           getPhiAmbient=False,
                           getPAmbient=False,
                           getCloudiness=False,
                           currentValues=True):
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
            If True, return cloudiness
        currentValues : bool, optional
            If True, returns values of current horizon (default: True).
            If False, returns annual values.
            
        Returns
        -------
        The result is returned as a tuple
        """
        # Get current and final position
        if currentValues:
            currentPosition = self.timer.current_timestep
            finalPosition = currentPosition + self.timer.timesteps_horizon
        else:
            currentPosition = 0
            finalPosition = self.timer.timesteps_total

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
            
        Returns
        -------
        The result is returned as a tuple
        """
        if not useTimesteps:
            fromTimestep = max(0, self.timer.current_timestep - numberTimesteps)
        return self._getWeatherData(fromTimestep,
                                    self.timer.current_timestep,
                                    getTAmbient,
                                    getQDirect,
                                    getQDiffuse,
                                    getVWind,
                                    getPhiAmbient,
                                    getPAmbient,
                                    getCloudiness)
