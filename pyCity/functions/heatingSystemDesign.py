# -*- coding: utf-8 -*-
"""
Created on Mon Feb 09 08:38:15 2015

@author: tsz
"""

from __future__ import division

import numpy as np
import math

def bivalentChpBoiler(timer, spaceHeating, domesticHotWater, fullLoadHours=5000, chpRounding=500, boilerRounding=1000):
    """
    Design a bivalent CHP-Boiler system based on the CHP unit's full load hours.
    
    Parameters
    ----------
    timer : Timer object 
        A pointer to the common timer object 
    spaceHeating : SpaceHeating object 
        Space heating demand of the building
    domesticHotWater : DomesticHotWater object 
        Domestic hot water demand of the building
    fullLoadHours : Integer, optional
        CHP unit's design full load hours per year
    chpRounding : Integer, optional
        Round up the CHP unit's heat output. Example:
        If ``chpRounding=500`` and the design output is 5300 W, the final 
        result would be 5500 W.
    boilerRounding : Integer, optional
        Analogue to chpRounding
    
    Returns
    -------
    q_nominal_chp : Float
        Nominal CHP heat output in Watt
    q_nominal_boiler : Float
        Nominal boiler heat output in Watt
    """
    # Determine the load duration curve (space heating + domestic hot water)
    if domesticHotWater.getThermalOrElectrical():
        totalThermalDemand = spaceHeating.getLoadcurve() + domesticHotWater.getLoadcurve()
    else:
        totalThermalDemand = spaceHeating.getLoadcurve()
    
    # Compute the index that corresponds to fullLoadHours
    timeDiscretization = timer.getTimeDiscretization()
    relevantTimestep = int(fullLoadHours * 3600 / timeDiscretization)
    
    # Sort the duration curve
    sortedThermalDemand = np.flipud(np.sort(totalThermalDemand))
    
    # Get the value at fullLoadHours and round appropriately
    rawChpPower = sortedThermalDemand[relevantTimestep]
    chpPower = math.ceil(rawChpPower / chpRounding) * chpRounding
    
    # Compute the boiler's nominal heat output and round too
    rawBoilerPower = sortedThermalDemand[0] - chpPower
    boilerPower = math.ceil(rawBoilerPower / boilerRounding) * boilerRounding
    
    # Return both values
    return (chpPower, boilerPower)
    
def monovalentBoiler(spaceHeating, domesticHotWater, boilerRounding=1000):
    """
    Design a monovalent boiler system based on the annual load duration curve.

    Parameters
    ----------
    spaceHeating : SpaceHeating object 
        Space heating demand of the building
    domesticHotWater : DomesticHotWater object 
        Domestic hot water demand of the building
    fullLoadHours : Integer, optional
        CHP unit's design full load hours per year
    boilerRounding : Integer, optional
        Round up the boiler's heat output. Example:
        If ``boilerRounding=1000`` and the design output is 5300 W, the final 
        result would be 6000 W.
    
    Returns
    -------
    q_nominal : Float
        Nominal boiler heat output in Watt    
    """
    # Determine the load duration curve (space heating + domestic hot water)
    if domesticHotWater.getThermalOrElectrical():
        totalThermalDemand = spaceHeating.getLoadcurve() + domesticHotWater.getLoadcurve()
    else:
        totalThermalDemand = spaceHeating.getLoadcurve()
    
    # Compute the boiler's nominal heat output and round appropriately
    rawBoilerPower = np.max(totalThermalDemand)
    boilerPower = math.ceil(rawBoilerPower / boilerRounding) * boilerRounding
    
    # Return the boiler's nominal heat output
    return boilerPower
    