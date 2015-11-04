#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 09:12:18 2015

@author: Thomas
"""
from __future__ import division

import classes.demand.Load
import numpy as np
import functions.slp_electrical as slp_el
import functions.changeResolution as cr
import functions.stochastic_electrical_load.appliance_model as app_model
import functions.stochastic_electrical_load.lighting_model as light_model
import classes.demand.StochasticElectricalLoadWrapper as wrapper

class ElectricalDemand(classes.demand.Load.Load):
    """
    Implementation of the electrical demand object
    """
    
    loaded_slp = False
    slp = []

    def __init__(self, 
                 environment, 
                 method=0,
                 loadcurve=[], 
                 annualDemand=0, profileType="H0",
                 singleFamilyHouse=True, numberHousehold=0,
                 randomizeAppliances=True, lightConfiguration=0, occupancy=[]):
        """
        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        method : Integer, optional
            - `0` : Provide load curve directly (for all timesteps!)
            - `1` : Standard load profile (for households)
            - `2` : Stochastic electrical load model
        loadcurve : Array-like, optional
            Load curve for all investigated time steps
        annualDemand : Float (required for SLP)
            Annual electrical demand in kWh.
        profileType : String (required for SLP)
            - H0 : Household
            - L0 : Farms
            - L1 : Farms with breeding / cattle
            - L2 : Farms without cattle
            - G0 : Business (general)
            - G1 : Business (workingdays 8:00 AM - 6:00 PM)
            - G2 : Business with high loads in the evening
            - G3 : Business (24 hours)
            - G4 : Shops / Barbers
            - G5 : Bakery
            - G6 : Weekend operation
        numberHousehold : Boolean, optional (used in method 2)
            Number of people living in the household.
        randomizeAppliances : Boolean (only required in method 2)
            - True : Distribute installed appliances randomly
            - False : Use the standard distribution
        lightConfiguration : Integer (only optional in method 2)
            There are 100 light bulb configurations predefined for the 
            Stochastic model. Select one by entering an integer in [0, ..., 99]
        occupancy : Array-like (optional, but recommended in method 2)
            Occupancy given at 10-minute intervals for a full year
            
        Info
        ----
        The standard load profile can be downloaded here:
        http://www.ewe-netz.de/strom/1988.php
        """
        if method == 0:
            super(ElectricalDemand, self).__init__(environment, loadcurve)
        elif method == 1:
            if not ElectricalDemand.loaded_slp:
                filename = "inputs/standard_load_profile/slp_electrical.xlsx"
                ElectricalDemand.slp = slp_el.load(filename)
                ElectricalDemand.loaded_slp = True
            
            loadcurve = slp_el.get_demand(annualDemand, 
                                          ElectricalDemand.slp[profileType],
                                          environment.timer.timeDiscretization)
            
            super(ElectricalDemand, self).__init__(environment, loadcurve)
        elif method == 2:
            # Initialize appliances and lights
            pathApps = 'inputs/stochastic_electrical_load/Appliances.csv'
            self.appliances = app_model.Appliances(pathApps, 
                                                   randomizeAppliances)
            pathLights = 'inputs/stochastic_electrical_load/LightBulbs.csv'
            self.lights = light_model.load_lighting_profile(pathLights, 
                                                            lightConfiguration)
            
            # Create wrapper object
            timeDis = environment.timer.timeDiscretization
            timestepsDay = int(86400/timeDis)
            day = environment.timer.currentWeekday
            self.wrapper = wrapper.Electricity_profile(self.appliances, 
                                                       self.lights)
            
            # Make full year simulation
            demand = []
            beam = environment.weather.qDirect
            diffuse = environment.weather.qDiffuse
            irradiance = beam + diffuse
            required_timestamp = np.arange(1440)
            given_timestamp = timeDis * np.arange(timestepsDay)
            
            # Loop over all days
            for i in range(int(len(irradiance) * timeDis / 86400)):
                if (i + day) % 7 in (0,6):
                    weekend = True
                else:
                    weekend = False
                
                irrad_day = irradiance[timestepsDay*i : timestepsDay*(i+1)]
                current_irradiation = np.interp(required_timestamp, 
                                                given_timestamp, irrad_day)
                
                current_occupancy = occupancy[144*i : 144*(i+1)]
                                
                demand.append(self.wrapper.demands(current_irradiation, 
                                                   weekend, 
                                                   i, 
                                                   current_occupancy)[0])

            res = np.array(demand)
            res = np.reshape(res, res.size)
            
            loadcurve = cr.changeResolution(res, 60, timeDis)
            
            super(ElectricalDemand,self).__init__(environment, loadcurve)
        
        self._kind = "electricaldemand"
        self.method = method
        
    def getDemand(self, currentValues=True):
        """
        """
        if self.method in (0, 1, 2):
            return self._getLoadcurve(currentValues)
        else:
            pass
