#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 16:47:12 2015

@author: tsz
"""

from __future__ import division

import numpy as np
import math


class Sun(object):
    """
    Implementation of the Sun class.
    """
    
    def __init__(self, 
                 timer, 
                 location=(50.76, 6.07), 
                 time_zone=1,
                 altitude=0, 
                 TRY=True):
        """
        location : tuple, optional
            (latitude, longitude) of the simulated system's position. Standard
            values (50.76, 6.07) represent Aachen, Germany.
        time_zone : integer, optional
            Shift between the location's time and GMT in hours. CET is 1.
            Daylight savings time is neglected.
        altitude : float, optional
            The locations altitude in meters.
        TRY : Boolean, optional
            Is the input data from a test reference year? If yes, the time 
            equation has an offset of 0.5 hours, else 0.
        """
        self._kind = "sun"

        self.timer = timer
        self.altitude = altitude
        self.time_zone = time_zone
        
        # Split location into latitude (phi) and longitude (lambda).
        (self.latitude, self.longitude) = location
        
        self.TRY = TRY

    @property
    def kind(self):
        return self._kind
    
    def setLocation(self, location=(50.76, 6.07), time_zone=1, altitude=0):
        """ 
        Update location (latitude and longitude), time zone and altitude. 
        
        Parameters
        ----------
        location : tuple, optional
            (latitude, longitude) of the simulated system's position. Standard
            values (50.76, 6.07) represent Aachen, Germany.
        time_zone : integer, optional
            Shift between the location's time and GMT in hours. CET is 1.
            Daylight savings time is neglected.
        altitude : float, optional
            The locations altitude in meters.   
        """
        (self.latitude, self.longitude) = location
        self.altitude = altitude
        self.time_zone = time_zone
    
    def update(self, currentValues=True):
        """ 
        Update attributes (for example because a new optimization period just
        started).
        
        ``update`` updates the following parameters:
        - Air mass
        - Extraterrestrial radiation
        - Delta
        - Omega
        - ThetaZ

        Parameters
        ----------
        currentValues : bool, optional
            If True, returns values of current horizon (default: True).
            If False, returns annual values.
        """
        self.computeGeometry(allTimeSteps=not currentValues)
    
    def computeGeometry(self, allTimeSteps=False):
        """
        This function computes hour angle, declination, zenith angle of the 
        sun for the forecasting horizon.
        
        The implemented equations can be found in:
        Duffie, Beckman - Solar Engineering of Thermal Processes, 2013 (4th 
        ed.)
        
        Parameters
        ----------
        allTimeSteps : boolean, optional
            - True: Compute the results for all time steps
            - False: Compute the results only for the upcoming horizon
        
        Notes
        -----
        Updates the following attributes

        * omega : array-like
          Hour angle. The angular displacement of the sun east or west of
          the local meridian due to rotation of the earth on its axis at
          15 degrees per hour; morning negative, afternoon positive

        * delta : array-like
          Declination. The angular position of the sun at solar noon (i.e.,
          when the sun is on the local meridian) with respect to the plane
          of the equator, north positive; −23.45 <= delta <= 23.45

        * theta_z : array-like
          Zenith angle. The angle between the vertical and the line to the
          sun, that is, the angle of incidence of beam radiation on a
          horizontal surface; 0 <= theta_z <= 90

        """
        # Get timer-relevant data
        time_discretization = self.timer.time_discretization
        initialTime = self.timer.current_timestep * time_discretization
        
        if allTimeSteps:
            timesteps = self.timer.timesteps_total
        else:
            timesteps = self.timer.timesteps_horizon
        
        # Define pi
        pi = math.pi
        
        # Notice:
        # All inputs and outputs are given/expected in degrees. For the 
        # computation, radians are required. Angles are converted from 
        # degrees to radians via np.radians(angle). The resulting radian 
        # value is noted with an R-suffix. Converting radian values to 
        # degrees is done via np.rad2deg(angleR).
        # This conversion might be done by multiplying/dividing with 180°/pi
    
        # Create time array
        time = ((np.linspace(0, timesteps-1, num=timesteps)) 
                * time_discretization + initialTime)
    
        # Determine the day's number and standard time (neglect daylight 
        # savings time)
        numberDay = time / (3600 * 24)
        standardTime = time / 3600 - np.floor(numberDay) * 24
        
        # Equation 1.4.2, page 9
        B = 360 / 365.26 * numberDay
        BR = np.radians(B)
        # Compute abbreviations for E and extraterrestrial irradiation (Gon)
        cosB  = np.cos(BR)
        sinB  = np.sin(BR)
        cos2B = np.cos(2 * BR)
        sin2B = np.sin(2 * BR)
        cos3B = np.cos(3 * BR)
        sin3B = np.sin(3 * BR)
        
        # Convert local time into solar time
        # Equation 1.5.3, page 11
        E = 229.2 / 60 * (0.000075 + 
                          0.001868 * cosB -
                          0.032077 * sinB - 
                          0.014615 * cos2B - 
                          0.040890 * sin2B)
        
        # Compute standard meridian
        # Footnote 5 of chapter 1. Can be found on page 11.
        lambdaStandard = self.time_zone * 15
        
        # Compute solar time
        # Equation 1.5.2, page 11 (conversion to hours instead of minutes)
        if self.TRY:
            offset = 0.5
        else:
            offset = 0
            
        solarTime = (standardTime
                     + 4 * (self.longitude - lambdaStandard) / 60
                     + E
                     - offset)
        
        # Hour angle
        # The angular displacement of the sun east or west of the local 
        # meridian due to rotation of the earth on its axis at 15 degrees 
        # per hour; morning negative, afternoon positive
        # Confirm page 13
        omega = 360 / 24 * (solarTime - 12)
        # Ensure: -180 <= omega <= 180
        omega[omega < -180] = omega[omega < -180] + 360
        omega[omega > 180] = omega[omega > 180] - 360
        omegaR = np.radians(omega)
        
        # Declination
        # The angular position of the sun at solar noon (i.e., when the sun 
        # is on the local meridian) with respect to the plane of the equator, 
        # north positive; −23.45 <= delta <= 23.45
        # Equation 1.6.1b, page 14
        delta = 180 / pi * (0.006918 - 0.399912 * cosB + 0.070257 * sinB
                                     - 0.006758 * cos2B + 0.000907 * sin2B 
                                     - 0.002697 * cos3B + 0.001480 * sin3B)
        deltaR = np.radians(delta)
        
        # Zenith angle
        # The angle between the vertical and the line to the sun, that is, the 
        # angle of incidence of beam radiation on a horizontal surface; 
        # 0 <= thetaZ <= 90. If thetaZ > 90, the sun is below the horizon.
        # Equation 1.6.5 on page 15
    
        # Introduce abbreviations to improve readability
        latitudeR = math.radians(self.latitude)
        cosPhi = math.cos(latitudeR)
        sinPhi = math.sin(latitudeR)
        cosDelta = np.cos(deltaR)
        sinDelta = np.sin(deltaR)
        cosOmega = np.cos(omegaR)
        cosThetaZ = np.maximum(0, cosPhi * cosDelta * cosOmega
                               + sinDelta * sinPhi)
        thetaZR = np.arccos(cosThetaZ)
        thetaZ = np.rad2deg(thetaZR)
        
        # Compute airmass
        # Footnote 3 on page 10
        self.airmass = (math.exp(-0.0001184 * self.altitude) /
                        (cosThetaZ + 0.5057 * np.power(96.08 - thetaZ, -1.634)))
        
        # Compute extraterrestrial irradiance (Gon)
        # Extraterrestrial radiation incident on the plane normal to the 
        # radiation on the nth day of the year.
        # Solar constant. Page 6 
        Gsc = 1367  # W/m^2
        # Equation 1.4.1b on page 9
        self.Gon = Gsc * (1.000110
                          + 0.034221 * cosB
                          + 0.001280 * sinB
                          + 0.000719 * cos2B
                          + 0.000077 * sin2B)
        
        # Save results
        self.theta_z = thetaZ
        self.delta = delta
        self.omega = omega

    def getIncidenceAngle(self, beta, gamma):
        """
        Compute the incidence angle on a tilted surface.
        
        All inputs/outputs are supposed to be in degrees!
        
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
        """
        # Compute incidence angle of beam radiation
        # Transform to radian
        betaR  = math.radians(beta)
        phiR   = math.radians(self.latitude)
        gammaR = math.radians(gamma)
        deltaR = np.radians(self.delta)
        omegaR = np.radians(self.omega)
        
        # Introduce required abbreviations
        sinBeta  = math.sin(betaR)
        cosBeta  = math.cos(betaR)
        sinDelta = np.sin(deltaR)
        cosDelta = np.cos(deltaR)
        sinPhi   = math.sin(phiR)
        cosPhi   = math.cos(phiR)
        sinGamma = math.sin(gammaR)
        cosGamma = math.cos(gammaR)
        sinOmega = np.sin(omegaR)
        cosOmega = np.cos(omegaR)
        
        # Equation 1.6.2, page 14
        cosTheta = np.maximum(sinDelta * sinPhi * cosBeta
                              - sinDelta * cosPhi * sinBeta * cosGamma
                              + cosDelta * cosPhi * cosBeta * cosOmega
                              + cosDelta * sinPhi * sinBeta * cosGamma * cosOmega
                              + cosDelta * sinBeta * sinGamma * sinOmega, 0)
        thetaR = np.arccos(cosTheta)
        theta = np.rad2deg(thetaR)
    
        # Return incidence angle
        return theta
        
    def getTotalRadiationTiltedSurface(self, beamRadiation, diffuseRadiation, 
                                       beta, gamma, albedo=0.3, update=False, currentValues=True):
        """
        Compute the total radiation on a tilted surface.

        Parameters
        ----------
        beamRadiation : array-like
            The solar radiation received from the sun without having been
            scattered by the atmosphere (also often named direct radiation)
        diffuseRadiation : array-like
            The solar radiation received from the sun after its direction has
            been changed by scattering by the atmosphere.
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
        update : bool, optional
            Perform an update of the common angles before computing the total
            radiation on the tilted surface
        currentValues : bool, optional
            If True, returns values of current horizon (default: True).
            If False, returns annual values.
        """
        # Update common angles
        if update:
            self.update(currentValues=currentValues)
        
        # Get incidence angle
        theta = self.getIncidenceAngle(beta, gamma)
        
        # Return total radiation on a tilted surface
        return self._getRadiationTiltedSurface(theta, 
                                               beamRadiation, 
                                               diffuseRadiation, 
                                               beta, 
                                               albedo)

    def _getRadiationTiltedSurface(self, theta, beamRadiation, 
                                   diffuseRadiation, beta, albedo=0.3):
        """
        Compute the total radiation on a tilted surface.
    
        Parameters
        ----------
        theta : array-like
            Incidence angle.
        beamRadiation : array-like
            The solar radiation received from the sun without having been
            scattered by the atmosphere (also often named direct radiation)
        diffuseRadiation : array-like
            The solar radiation received from the sun after its direction has 
            been changed by scattering by the atmosphere.
        beta : float
            Slope, the angle (in degree) between the plane of the surface in 
            question and the horizontal. 0 <= beta <= 180. If beta > 90, the 
            surface faces downwards.
        albedo : float, optional
            Average value on earth: 0.3
            Ground reflectance. 0 <= albedo <= 1
        """
        # Model coefficients 
        # Table 6, in Perez et al - 1990 - Modeling daylight availability and 
        # irradiance components from direct and global irradiance. 
        # Solar Energy, Vol. 44, No. 5, pp. 271-289
        # Values with increased accuracy can be found in the EnergyPlus 
        # engineering reference (Table 22, Fij Factors as a Function of Sky 
        # Clearness Range, page 147)
        
        fCoefficients = np.array(
            [[-0.0083117,  0.5877285, -0.0620636, 
              -0.0596012,  0.0721249, -0.0220216],
             [0.1299457,  0.6825954, -0.1513752,
              -0.0189325,  0.065965,  -0.0288748],
             [0.3296958,  0.4868735, -0.2210958,
              0.055414,  -0.0639588, -0.0260542],
             [0.5682053,  0.1874525, -0.295129,
              0.1088631, -0.1519229, -0.0139754],
             [0.873028,  -0.3920403, -0.3616149,
              0.2255647, -0.4620442,  0.0012448],
             [1.1326077, -1.2367284, -0.4118494,
              0.2877813, -0.8230357,  0.0558651],
             [1.0601591, -1.5999137, -0.3589221,
              0.2642124, -1.127234,   0.1310694],
             [0.677747,  -0.3272588, -0.2504286,
              0.1561313, -1.3765031,  0.2506212]
             ])
    
        # Compute a and b (page 281, below equation 9)
        thetaR = np.radians(theta)
        thetaZR = np.radians(self.theta_z)
        cosThetaZ = np.cos(thetaZR)
        cosTheta = np.cos(thetaR)
        a = np.maximum(0, cosTheta)
        b = np.maximum(0.087, cosThetaZ)
        
        # Compute epsilon (the sky's clearness)
        # Introduce variables and compute third power of thetaZR
        kappa = 1.041
        thetaZRTo3 = np.power(thetaZR, 3)
        
        # Compute normal incidence direct irradiance
        I = beamRadiation / b
        # Prevent division by zero
        temp = np.zeros_like(theta) # All inputs should have this length!
        temp[diffuseRadiation > 0] = (1.0 * I[diffuseRadiation > 0] / 
                                      diffuseRadiation[diffuseRadiation > 0])
        # equation 1 on p. 273 in Perez et al - 1990
        epsilon = (1 + temp + kappa * thetaZRTo3) / (1 + kappa * thetaZRTo3)
        
        # Determine clear sky category
        # table 1 on page 273 in Perez et al - 1990
        # Note: As this value is used to get data from fCoefficients, the 
        # implemented categories range from 0 to 7 instead from 1 to 8
        epsilonCategory = np.zeros_like(epsilon, dtype=int)
        epsilonCategory[(epsilon >= 1.065) & (epsilon < 1.23)] = 1
        epsilonCategory[(epsilon >= 1.230) & (epsilon < 1.50)] = 2
        epsilonCategory[(epsilon >= 1.500) & (epsilon < 1.95)] = 3
        epsilonCategory[(epsilon >= 1.950) & (epsilon < 2.80)] = 4
        epsilonCategory[(epsilon >= 2.800) & (epsilon < 4.50)] = 5
        epsilonCategory[(epsilon >= 4.500) & (epsilon < 6.20)] = 6
        epsilonCategory[epsilon >= 6.200] = 7
        
        # Compute Delta (the sky's brightness)
        # equation 2 on page 273 in Perez et al - 1990
        Delta = diffuseRadiation * self.airmass / self.Gon
        
        # Compute F1 (circumsolar brightening coefficient) and F2 (horizon 
        # brightening coefficient)
        # Below table 6 on page 282 in Perez et al - 1990
        # According to Duffie and Beckman (4th edition, page 94, 
        # equation 2.16.12), 
        # F1 is supposed to be greater or equal to 0
        F1 = np.maximum(fCoefficients[epsilonCategory, 0] +
                        fCoefficients[epsilonCategory, 1] * Delta +
                        fCoefficients[epsilonCategory, 2] * thetaZR,
                        0)
    
        F2 = (fCoefficients[epsilonCategory, 3] +
              fCoefficients[epsilonCategory, 4] * Delta +
              fCoefficients[epsilonCategory, 5] * thetaZR)
        
        # Compute diffuse radiation on tilted surface
        # Equation 9 on page 281 in Perez et al - 1990
        betaR = math.radians(beta)
        cosBeta = math.cos(betaR)
        sinBeta = math.sin(betaR)
        diffRadTiltSurface = diffuseRadiation * ((1 - F1) * (1 + cosBeta) / 2 
                                                 + F1 * a / b + F2 * sinBeta)
        
        # Compute the influence of beam radiation and reflected radiation
        # Equation 2.15.1 in Duffie and Beckman (4th edition, page 89)    
        # Compute direct radiation on tilted surface
        # Equation 1.8.1 in Duffie and Beckman (4th edition, page 24)
        # We divide by b instead of cosThetaZ to prevent division by 0
        # Direct radiation on a tilted surface is always positive, therefore 
        # use ``a`` insted of cosTheta
        directRadTiltSurface = beamRadiation * a / b
    
        # Compute reflected total radiation
        # Equation 2.15.1 in Duffie and Beckman (4th edition, page 89)
        # Notice: We changed the proposed nomenclature. rhoG is written as 
        # albedo.
        # Total solar radiation is computed as sum of beam and diffuse 
        # radiation. See page 10 in Duffie and Beckman (4th edition)
        totalSolarRad = beamRadiation + diffuseRadiation
        reflectedRadTiltSurface = totalSolarRad * albedo * (1 - cosBeta) / 2
        
        totalRadTiltSurface = (diffRadTiltSurface + 
                               directRadTiltSurface + 
                               reflectedRadTiltSurface)
    
        # Return total radiation on a tilted surface
        return (totalRadTiltSurface, 
                diffRadTiltSurface, 
                directRadTiltSurface, 
                reflectedRadTiltSurface)
