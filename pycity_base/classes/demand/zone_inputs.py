#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 09:27:39 2015

@author: tsz
"""

from __future__ import division

import numpy as np


class ZoneInputs(object):
    """
    """

    def __init__(self, environment, 
                 zone_parameters=None,
                 t_m_init=20,
                 ventilation=0,
                 occupancy=0,
                 appliances=0, 
                 lighting=0):
        """
        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        zone_parameters : ZoneParameters object
            Holds all relevant parameters of the thermal zone (geometry,
            U-values)
        t_m_init : Float, optional
            Initial temperature of the internal heat capacity.
            Requires ``method=2``.
        ventilation : Array-like, optional
            Ventilation rate in 1/h.
            Requires ``method=2``.
        occupancy : Array-like, optional
            Full year occupancy profile.
            Requires ``method=2``.
        appliances : Array-like, optional
            Internal gains from electrical appliances in Watt.
            Requires ``method=2``.
        lighting : Array-like, optional
            Internal gains from lighting in Watt.
            Requires ``method=2``.
        """
        self._kind = "zoneinputs"

        self.environment = environment
        self.zone_parameters = zone_parameters
        self.t_m_init = t_m_init

        # Compute internal and solar gains. Get ambient (supply) temperature.
        self.Phi_int = self.getInternalGains(occupancy=occupancy,
                                             appliances=appliances,
                                             lighting=lighting)
        self.T_e = environment.weather.t_ambient
        self.T_sup = environment.weather.t_ambient
        
        # UNDER CONSTRUCTION
        self.Phi_sol, self.solar_opaque, self.solar_window = self.getSolarGains()

    @property
    def kind(self):
        return self._kind

    def getInternalGains(self, occupancy=0, appliances=0, lighting=0):
        """
        Computation of Phi_int.

        Based on DIN EN ISO 13790, equation 36, section 10.2.
        Confirm pages 60, ff.

        Parameters
        ----------
        occupancy : array-like
            Number of active people at each time step (no unit).
            According to DIN EN ISO 8996, table A.2 (page 21), this number is
            multiplied by 115 Watt/person.
        appliances : array-like
            Aggregated electricity consumption of all electrical appliances in
            this zone in Watt.
        lighting : array-like
            Aggregated electricity consumption of all installed lights in Watt.
        """
        # Compute gains from people
        # Average power per person: DIN EN ISO 8996, table A.2 (page 21)
        averagePowerPerson = 115  # Watt/person
        gainsPeople = occupancy * averagePowerPerson

        # Assumption: The entire electricity consumption are heat gains
        return (gainsPeople + appliances + lighting)

    def getSolarGains(self):
        """
        Set the solar gains for the upcoming scheduling period.
        """
        # Get beam and diffuse radiation on a horizontal surface
        beamRad = self.environment.weather.q_direct
        diffuseRad = self.environment.weather.q_diffuse

        # Get ground reflectance
        groundReflectance = self.zone_parameters.albedo


        # Initialize solar gains
        solarGains = np.zeros_like(beamRad)
        solarOpaque = []
        solarWindows = []
        
        # Update solar geometry
        self.environment.weather.computeGeometry(True)

        # Iterate over all surface areas
        for i in range(len(self.zone_parameters.F_r)):
            # Compute heat flux through each opaque and window-like surface
            # DIN EN ISO 13790:2008, equation 43, section 11.3.2, page 67
            # Note: F_sh_ob, I_sol and F_r are the same for opaque and 
            # window-like components, therefore the total, effective area and 
            # radiative heat exchange with the sky are summed up.
            A_opaque_sol  = self.zone_parameters.A_opaque_sol[i]
            A_windows_sol = self.zone_parameters.A_windows_sol[i]
            A_windows     = self.zone_parameters.A_windows[i]
            A_total = A_opaque_sol + A_windows_sol
            Psi_r_windows = self.zone_parameters.Psi_r_windows[i]
            Psi_r_total = self.zone_parameters.Psi_r_opaque[i] + Psi_r_windows
        
            radFunc = self.environment.weather.getTotalRadiationTiltedSurface
            radTilt = radFunc(beamRadiation=beamRad,
                              diffuseRadiation=diffuseRad,
                              beta=self.zone_parameters.beta[i],
                              gamma=self.zone_parameters.gamma[i],
                              albedo=groundReflectance)[0]
            solarOpaque.append(radTilt)

            if A_windows > 0:
                solarWindows.append((A_windows_sol * radTilt - Psi_r_windows * self.zone_parameters.F_r[i]) / A_windows)
            elif A_windows == 0:
                solarWindows.append(0)
            else:
                msg = 'A_windows cannot be negative!'
                raise AssertionError(msg)

            solarGains += (A_total * radTilt 
                         - Psi_r_total * self.zone_parameters.F_r[i])

        # Return results
        return solarGains, solarOpaque, solarWindows
