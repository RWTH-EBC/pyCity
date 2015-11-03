#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 11 16:01:38 2015

@author: tsz
"""

from __future__ import division

import numpy as np

class Controller(object):
    """
    The building controller is responsible for gathering the total thermal and
    electrical demand as well as for computing the required flow temperature.
    """
    
    def __init__(self, environment, heatingCurve):
        """
        Parameters
        ---------
        environment : environment object
            Common to all other objects. Includes time and weather instances
        heatingCurve : heatingCurve object
            Computes the required flow temperature according to the ambient 
            temperature
        """
        self.environment = environment
        self.heatingCurve = heatingCurve
        self.flowTemperature = np.zeros(self.environment.getTimestepsHorizon())
        self._kind = "controller"
        
    def getDemands(self, apartments):
        """
        Get the entire thermal and electrical demand of all apartments in this 
        building.
        
        Parameters
        ----------
        apartments : List 
            List of all building's apartments
        """
        
        # Initialization
        # Demands are zero
        demandElectrical = np.zeros(self.environment.getTimestepsHorizon())
        demandThermal    = np.zeros(self.environment.getTimestepsHorizon())
        
        # Add demands of each apartment
        for apartment in apartments:
            # Update demands
            apartment.updateDemands()
            
            # Get entire electrical, domestic hot water and space heating 
            # demand
            (tempEl, tempDhw, tempSh) = apartment.getDemands()
            dhwThermal = apartment.getDomesticHotWaterThermal()
            
            if dhwThermal:
                demandThermal    += tempSh + tempDhw
                demandElectrical += tempEl
            else:
                demandThermal    += tempSh
                demandElectrical += tempEl + tempDhw


        return (demandElectrical, demandThermal)
        
    def getFlowTemperature(self, apartments):
        """
        Get the required flow temperature of this building.
        
        Parameters
        ----------
        apartments : List 
            List of all building's apartments
        """
        
        # Get ambient temperature
        relevantPreviousDays = 1 # Number of previous days' weather forecast 
                                 # relevant to the heating curve
        numberTimesteps = (relevantPreviousDays * 24 / 
                           self.environment.getTimeDiscretization() * 3600)
        (tAmbientPrevious,) = self.environment.weather.getPreviousWeather(numberTimesteps=numberTimesteps, useTimesteps=True, getTAmbient=True)
        (tAmbientForecast,) = self.environment.weather.getWeatherForecast(getTAmbient=True)
        tAmbient = np.concatenate((tAmbientPrevious, tAmbientForecast))
        
        # Get flow temperature according to heating curve
        rawTFlow = self.heatingCurve.computeRequiredFlowTemperature(tAmbient, smoothingPeriod=relevantPreviousDays)
        timestepsHorizon = self.environment.getTimestepsHorizon()
        firstIndex = len(rawTFlow) - timestepsHorizon
        lastIndex  = firstIndex + timestepsHorizon
        tFlow = rawTFlow[firstIndex : lastIndex]
        
        # Check if this flow temperature has to be increased at certain time 
        # steps due to domestic hot water
        for apartment in apartments:
            tFlowDHW = apartment.getDomesticHotWaterTemperature()
            tFlow = np.maximum(tFlow, tFlowDHW)
        
        self.flowTemperature = tFlow
        return tFlow
        