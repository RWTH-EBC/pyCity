#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 14:09:28 2015

@author: tsz
"""

import os
import numpy as np
import functions.stochastic_electrical_load.lighting_model as lighting_model
import functions.stochastic_electrical_load.appliance_model as appliance_model
from __future__ import division


class Electricity_profile(object):
    """
    """

    type_weekday = ["wd", "we"] # weekday, weekend
    
    # Load statistics for appliances (transition probability matrix)
    activity_statistics = {}
    activity_statistics_loaded = False
    
    
    def __init__(self, appliances, lightbulbs):
        """
        This class loads all input data before 
        
        Parameters
        ----------
        appliances : list
            List of appliance objects
        """
        src_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        folder = os.path.join(src_path, 'inputs', 'stochastic_electrical_load', 'constants')
        if not Electricity_profile.activity_statistics_loaded:
            # Load activity statistics
            Electricity_profile.activity_statistics_loaded = True
            
            for weekday in self.type_weekday:
                filename = "ActiveAppliances_" +weekday+".csv"
                file_path = os.path.join(folder, filename)
                temp = (np.loadtxt(file_path, delimiter=";")).tolist()
                Electricity_profile.activity_statistics[weekday] = temp
        
        # Create lighting configuration
        self.lighting_config = lighting_model.LightingModelConfiguration()
        
        # Save inputs
        self.appliances = appliances
        self.lightbulbs = lightbulbs


    def _get_month(self, day, leap_year=False):
        """
        """
        if leap_year:
            days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        else:
            days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
        days_summed = np.cumsum(days)
        
        for i in range(len(days)):
            if days_summed[i] >= day:
                break
        return int(i + 1)
    
    def demands(self, irradiation, weekend, day, occupancy):
        """
        Parameters
        ----------
        irradiation : Array-like
            Solar irradiation on a horizontal plane for one day (1 minute res.)
        weekend : Boolean
            - True: Weekend
            - False: Monday - Friday
        day : Integer
            Day of the (computation) year.
        occupancy : Array-like
            Occupancy for one day (10 minute resolution)
        """
        month = self._get_month(day)
        
        # Lighting
        fun = lighting_model.run_lighting_simulation
        demand_lighting = fun(occupancy, self.lightbulbs, irradiation,
                              self.lighting_config)
        
        # Appliances
        fun = appliance_model.run_application_simulation
        type_weekday = self.type_weekday[weekend]
        activity_statistics = self.activity_statistics[type_weekday]
        demand_appliances = fun(occupancy, self.appliances, 
                                activity_statistics, month)
                                
        total_demand_lighting = np.sum(demand_lighting, axis=0)
        total_demand_appliances = np.sum(demand_appliances, axis=0)
        
        total_demand = total_demand_appliances + total_demand_lighting
        
        return (total_demand, total_demand_lighting, total_demand_appliances)