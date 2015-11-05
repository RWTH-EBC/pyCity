#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 09:27:39 2015

@author: tsz

"""

import numpy as np
from __future__ import division


class ZoneInputs(object):
    """
    """

    def __init__(self, environment, zoneParameters, T_m_init):
        """
        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        zoneParameters : ZoneParameters object
            Holds all relevant parameters of the thermal zone (geometry,
            U-values)
        """
        self.environment = environment
        self.zoneParameters = zoneParameters
        self.T_m_init = T_m_init

        # Initialize internal and solar gains as well as supply temperatures
        timestepsHorizon = environment.timer.timestepsHorizon
        self.Phi_int = np.zeros(timestepsHorizon)
        self.Phi_sol = np.zeros(timestepsHorizon)
        self.T_e = np.zeros(timestepsHorizon)
        self.T_sup = np.zeros(timestepsHorizon)

    def getTInit(self):
        """ """
        return self.T_m_init
    
    def setTInit(self, T_m_init):
        """ """
        self.T_m_init = T_m_init

    def update(self, occupancy, appliances, lighting):
        """
        Compute internal and solar gains as well as the ambient and supply
        temperature.
        """
        self.getInternalGains(occupancy=occupancy,
                              appliances=appliances,
                              lighting=lighting)
        self.getSolarGains()
        self.getAmbientTemperatures()

    def getInternalGains(self, occupancy, appliances, lighting):
        """
        Computation of Phi_int.

        Based on DIN EN ISO 13790, equation 36, section 10.2.
        Confirm pages 60, ff.

        Parameters
        ----------
        occupancy : array_like
            Number of active people at each time step (no unit).
            According to DIN EN ISO 8996, table A.2 (page 21), this number is
            multiplied by 115 Watt/person.
        appliances : array_like
            Aggregated electricity consumption of all electrical appliances in
            this zone in Watt.
        lighting : array_like
            Aggregated electricity consumption of all installed lights in Watt.
        """
        # Compute gains from people
        # Average power per person: DIN EN ISO 8996, table A.2 (page 21)
        averagePowerPerson = 115  # Watt/person
        gainsPeople = occupancy * averagePowerPerson

        # Assumption: The entire electricity consumption are heat gains
        self.Phi_int = gainsPeople + appliances + lighting

    def getSolarGains(self, groundReflectance=0.3):
        """
        Set the solar gains for the upcoming scheduling period.

        Parameter
        ---------
        groundReflectance : float, optional
            Average reflectivity of the ground (sometimes refered to as
            albedo). Typical values are between 0.2 and 0.3.
        """
        # Get beam and diffuse radiation on a horizontal surface
        radiation = self.environment.getWeatherForecast(getQDirect=True,
                                                        getQDiffuse=True)
        (beamRadiation, diffuseRadiation) = radiation

        # Set form factors for radiation between component and sky (DIN EN
        # ISO 13790:2008, section 11.4.6, page 73)
        # Based on the index convention
        # ([South, West, North, East, Floor, Roof/Ceiling]), the azimuth
        # (gamma), slope (beta) angles and form factor for losses to the sky
        # (F_r) are:
        #         S,   W,   N,   E,   F, R
        gamma = [ 0,  90, 180, 270,   0, 0]
        beta  = [90,  90,  90,  90,   0, 0]
        F_r   = [0.5,  0.5, 0.5, 0.5, 0, 1]
        # No direct interaction between sun and floor, therefore the
        # corresponding F_r entry is zero.

        # Initialize solar gains
        solarGains = np.zeros_like(beamRadiation)

        # Iterate over all surface areas
        for i in range(len(gamma)):
            # Update only in the first iteration
            if i == 0:
                update = True
            else:
                update = False
            # Compute solar irradiation on tilted surfaces
            function = self.environment.getTotalRadiationTiltedSurface
            radTiltedSurface = function(beta=beta[i],
                                        gamma=gamma[i],
                                        albedo=groundReflectance,
                                        update=update)
            totalRadiationTiltedSurface = radTiltedSurface[0]

            # Compute heat flux through each opaque and window-like surface
            # DIN EN ISO 13790:2008, equation 43, section 11.3.2, page 67
            # Note: F_sh_ob, I_sol and F_r are the same for opaque and
            # window-like components, therefore the total, effective area and
            # radiative heat exchange with the sky are summed up.
            A_total = (self.zoneParameters.A_opaque_sol[i]
                       + self.zoneParameters.A_windows_sol[i])
            Psi_r_total = (self.zoneParameters.Psi_r_opaque[i]
                           + self.zoneParameters.Psi_r_windows[i])
            solarGains += (A_total * totalRadiationTiltedSurface
                           - Psi_r_total * F_r[i])

        # Return results
        self.Phi_sol = solarGains

    def getAmbientTemperatures(self):
        """
        """
        (tAmbient,) = self.environment.getWeatherForecast(getTAmbient=True)

        self.T_e = tAmbient
        self.T_sup = tAmbient  # Assume that both temperatures are equal
