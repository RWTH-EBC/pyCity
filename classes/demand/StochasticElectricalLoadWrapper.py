#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 14:09:28 2015

@author: tsz
"""

from __future__ import division

import numpy as np
import random

import functions.stochastic_electrical_load.occupancy_model as occupancy_model
import functions.stochastic_electrical_load.lighting_model as lighting_model
import functions.stochastic_electrical_load.appliance_model as appliance_model


class Electricity_profile(object):
    """
    """

    # Define class variables for transition_probability_matrixes and initial 
    # occupancy 
    tpm = {}
    
    occ_start_states = {}
    occ_start_states_loaded = False
    
    type_weekday = ["wd", "we"] # weekday, weekend
    
    # Load statistics for appliances (transition probability matrix)
    activity_statistics = {}
    activity_statistics_loaded = False
    
    
    def __init__(self, number_occupants, appliances, lightbulbs, 
                 initial_day=1):
        """
        This class loads all input data before 
        
        Parameters
        ----------
        number_occupants : integer
            How many active occupants live in this building?
        appliances : list
            List of appliance objects
        initial_day : integer, optional
            Initial day. 1-5 correspond to Monday-Friday, 6-7 to Saturday and 
            Sunday
        """

        # Adjust number_occupants to be between 1 and 5 (as inputs are only
        # available for these numbers)
        number_occupants = max(1, min(5, number_occupants))

        folder = "inputs/stochastic_electrical_load/constants/"
        if not Electricity_profile.occ_start_states_loaded:
            # Load start states matrixes and activity statistics
            Electricity_profile.occ_start_states_loaded = True
            Electricity_profile.activity_statistics_loaded = True
            
            for weekday in self.type_weekday:
                temp = (np.loadtxt(folder+"occ_start_states_" +weekday+".csv",
                                   delimiter=";")).tolist()
                Electricity_profile.occ_start_states[weekday] = temp
        
                temp = (np.loadtxt(folder+"ActiveAppliances_" +weekday+".csv",
                                   delimiter=";")).tolist()
                Electricity_profile.activity_statistics[weekday] = temp
        
        if not (number_occupants, "wd") in Electricity_profile.tpm.keys():
            # Load transition probability matrixes
            for weekday in self.type_weekday:
                fname = folder+"tpm"+str(number_occupants)+"_"+weekday+".csv"
                temp = (np.loadtxt(fname, delimiter=";")).tolist()
                Electricity_profile.tpm[number_occupants, weekday] = temp

        # Determine initial occupancy:
        # Determine if the current day is a weekend-day
        if initial_day <= 5:
            self.weekend = False
        else:
            self.weekend = True
        # Get starting states and starting probabilities
        start_states = Electricity_profile.occ_start_states
        start_probs = start_states[self.type_weekday[self.weekend]]
        get_state = self._get_start_state
        self.initial_occupancy = get_state(start_probs[:][number_occupants])

        
        # Create lighting configuration
        self.lighting_config = lighting_model.LightingModelConfiguration()
        
        # Save inputs
        self.number_occupants = number_occupants
        self.appliances = appliances
        self.lightbulbs = lightbulbs

        
    def _get_start_state(self, start_probabilities):
        """
        Determine the active occupancy start state.
        """
        # Pick a random number to determine the start state
        fRand = random.random()
        
        # Reset the cumulative probability count
        fCumulativeP = 0
    
        # Return value
        result = 0
    
        # Loop construction
        found = False # Boolean variable instead of using break
        i = 0    
        
        while not found:
            fCumulativeP += start_probabilities[i]
            if (fRand < fCumulativeP or i >= len(start_probabilities)-1):
                result = i
                found = True
            i += 1
            
        return result
    
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
    
    def demands(self, irradiation, weekend, day, only_occupancy=False):
        """
        """

        # Occupancy
        tpm = self.tpm[self.number_occupants, self.type_weekday[weekend]]
        occupancy = occupancy_model.all_states(tpm, self.initial_occupancy)
        self.initial_occupancy = occupancy[-1]
        
        if only_occupancy:
            return occupancy
        else:
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
            
            return (total_demand, occupancy)