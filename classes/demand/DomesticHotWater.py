#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 08 22:39:15 2015

@author: Thomas
"""


import classes.demand.Load
import numpy as np
import functions.changeResolution as cr
import functions.dhw_stochastical as dhw_sto

class DomesticHotWater(classes.demand.Load.Load):
    """
    Implementation of the domestic hot water (DHW) object
    """

    loaded_profile = False
    loaded_dhw_sto = False
    a42 = [] # Tap water consumption profiles given in Annex 42
    dhw_sto_profiles = {}

    def __init__(self, 
                 environment, 
                 tFlow, 
                 thermal=True,
                 method=0,
                 loadcurve=[],
                 dailyConsumption=0, supplyTemperature=0,
                 singleFamilyHouse=True, numberHousehold=0,
                 occupancy=[]):
        """
        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        tFlow : Float
            Flow temperature of domestic hot water in degree Celsius.
        thermal : Boolean, optional
            Is the DHW provided electrically (False) or via thermal energy 
            storage (True)
        method : Integer, optional
            - `0` : Provide load curve directly (for all timesteps!)
            - `1` : Load profile from Annex 42
            - `2` : Stochastical method
        loadcurve : Array-like, optional
            Load curve for all investigated time steps (in Watt).
            This parameter is required when using ``method=0``.
        dailyConsumption : Float, optional
            Average, total domestic hot water consumption in liters/day.
            This parameter is required when using ``method=1``.
        supplyTemperature : Float, optional
            Supply temperature in degree Celsius. This parameter is necessary
            to compute the heat load that results from each liter consumption.
            This parameter is required when using ``method=1``.
            
        Info
        ----
        The load profiles from Annex 42 can be found here: 
        http://www.ecbcs.org/annexes/annex42.htm
        """
        self.method = method
        if method == 0:
            super(DomesticHotWater,self).__init__(environment, loadcurve)
        elif method == 1:
            timeDis = environment.timer.timeDiscretization
            # If not already done, load the Annex 42 profile
            if not DomesticHotWater.loaded_profile:
                filename = "inputs/standard_load_profile/dhw_annex42.csv"
                DomesticHotWater.a42 = np.loadtxt(filename, 
                                                  skiprows=1, delimiter="\t")
                # Adjust time resolution. Annex 42 data is sampled at 900 sec.
                if timeDis != 900:
                    res = []
                    changeResol = cr.changeResolution
                    for i in range(3):
                        res.append(changeResol(DomesticHotWater.a42[:,i], 
                                               oldResolution=900,
                                               newResolution=timeDis,
                                               method="mean"))
                    DomesticHotWater.a42 = np.transpose(np.array(res))
                DomesticHotWater.loaded_profile = True
                
            # Compute tap water profile (based on average daily consumption)
            if dailyConsumption <= 150:
                tapProfile = self.a42[:,0] * dailyConsumption / 100
            elif dailyConsumption <= 250 and dailyConsumption > 150:
                tapProfile = self.a42[:,1] * dailyConsumption / 200
            elif dailyConsumption > 250:
                tapProfile = self.a42[:,2] * dailyConsumption / 300
            
            # Compute equivalent heat demand in Watt
            cWater = 4180 # J/kgK
            flowFactor = 1 / 3600 # l/h -> kg/s
            deltaTemperature = tFlow - supplyTemperature
            loadcurve = cWater * tapProfile * flowFactor * deltaTemperature
            super(DomesticHotWater,self).__init__(environment, loadcurve)
        elif method == 2:
            # Load profiles
            if not DomesticHotWater.loaded_dhw_sto:
                loc = "inputs/dhw_stochastical.xlsx"
                DomesticHotWater.dhw_sto_profiles = dhw_sto.load_profiles(loc)
                DomesticHotWater.loaded_dhw_sto = True
            
            # Compute dhw demand
            profiles = DomesticHotWater.dhw_sto_profiles
            initialDay = environment.timer.currentDay
            timeDis = environment.timer.timeDiscretization
            tempDiff = tFlow - supplyTemperature
            (water, heat) = dhw_sto.full_year_computation(occupancy, profiles, 
                                                          timeDis, initialDay, 
                                                          tempDiff)
                                                      
            self.water = water
            super(DomesticHotWater,self).__init__(environment, heat)
        
        self._kind = "domestichotwater"
        self.tFlow = tFlow
        self.thermal = thermal
    
    def getDemand(self, currentValues=True, returnTemperature=True):
        """
        Get the domestic hot water demand (and the required flow temperature).
        
        Parameters
        ----------
        currentValues : Boolean, optional
            Return only current values (True) or the entire load (False)
        returnTemperature : Boolean, optional
            Also return the required flow temperature (True)
        """
        if self.method in (0, 1, 2):
            load = self._getLoadcurve(currentValues)
                
        if returnTemperature:
            tFlow = np.zeros_like(load)
            tFlow[load > 0] = self.tFlow
            
            return (load, tFlow)
        else:
            return load
    