# -*- coding: utf-8 -*-
"""
Created on Tue Mar 03 14:38:14 2015

@author: tsz

All data sheets are taken from:
http://www.enercon.de/p/downloads/ENERCON_Produkt_de_Maerz_2014_web.pdf
"""

from __future__ import division

import numpy as np

class WindEnergyConverter(object):
    """
    """
    
    def __init__(self, environment, velocity=[], power=[], useStoredDevice=True, nominalPower=7580):
        """
        Create a wind energy converter.
        
        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        velocity : Array_like, optional
            Vector of wind velocities for which power data is available. This
            parameter is obsolete if ``useStoredDevice==True``.
        power : Array_like, optional
            Vector of power data. This parameter is obsolete if 
            ``useStoredDevice==True``.
        useStoredDevice : Boolean, optional
            - ``True``: Use a predefined wind energy converter (Enercon)
            - ``False``: Use the given velocity/power data
        nominalPower : Float, optional
            If ``useStoredDevice==True``, the stored data for a device close 
            to the given nominalPower is taken.
            ``0 <= nominalPower <= 7580``
        """
        
        self.environment = environment        
        
        if useStoredDevice:
            if nominalPower == 7580:
                (velocity, power) = self._enercon126()

        self.velocity = velocity
        self.power    = power
    
    def _enercon126(self):
        """
        Return wind velocity (in m/s) and power (in W) of the Enercon E 126 
        wind energy converter. Nominal power: 7580 kW
        
        Source:
        http://www.enercon.de/p/downloads/ENERCON_Produkt_de_Maerz_2014_web.pdf
        Page 16.
        """
        # Wind velocity in m/s
        velocity = np.arange(start=1, stop=26, step=1)
        
        # Only enter the power data until nominal load is reached
        powerRaw = np.array([0, 0, 55, 175, 410, 760, 1250, 1900, 2700, 3750, 4850, 5750, 6500, 7000, 7350, 7500, 7580])
        
        # The remaining entries are assumed to be the nominal load
        power = np.ones_like(velocity) * np.max(powerRaw)
        power[0:len(powerRaw)] = powerRaw

        # Return results (multiply power by 1000 to convert to W instead of kW)
        return (velocity, 1000 * power)
        
    def getPower(self):
        """
        Get the expected power output of the wind energy converter for the 
        current optimization period.
        
        Returns
        -------
        currentPower : Array_like
            Output power in Watt.
        """
        (currentWind,) = self.environment.getWeatherForecast(getTAmbient=False, getQDirect=False, getQDiffuse=False, getVWind=True, getPhiAmbient=False, getPAmbient=False)
        self.currentPower = np.interp(currentWind, self.velocity, self.power)
        
        return self.currentPower
