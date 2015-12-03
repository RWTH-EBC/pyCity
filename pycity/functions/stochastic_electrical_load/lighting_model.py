#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 21:24:29 2015

@author: Thomas
"""

from __future__ import division
import random
import math
import csv


# The Excel Sheet has a fairly complicated configuration file (which I suppose most people have ignored so far)
# This class provides the standard inputs. If required, other values can be entered.
class LightingModelConfiguration():
  
    def relative_bulb_use_weighting(self):
        """ This represents the concept that some bulbs are used more frequently than others in a house.

            The return value is [-ln(random_variable)]
        """
        return -math.log(random.random())

   
    def __init__(self, 
                 external_irradiance_threshold = [60, 10],
                 calibration_scalar=0.00815368639667705, 
                 effective_occupancy=[0, 1, 1.52814569536424, 1.69370860927152, 1.98344370860927, 2.09437086092715], 
                 lighting_event_lower_value=[1, 2, 3, 5, 9, 17, 28, 50, 92],
                 lighting_event_upper_value=[1, 2, 4, 8, 16, 27, 49, 91, 259]):
        
        # House external global irradiance threshold
        self.ext_irr_threshold_mean = external_irradiance_threshold[0]
        self.ext_irr_threshold_std_dev = external_irradiance_threshold[1]

        # This calibration scaler is used to calibrate the model to so that it provides a particular average output over a large number of runs.
        self.calib_scalar = calibration_scalar

        #Effective occupancy represents the sharing of light use.
        self.eff_occupancy = effective_occupancy

        #This model defines how long a bulb will stay on for, if a switch-on event occurs.
        self.light_event_lower_value = lighting_event_lower_value
        self.light_event_upper_value = lighting_event_upper_value
        

def load_lighting_profile(filename, index=0):
    """
    Load the installed light bulbs
    The tool already provided a sheet with 100 sample bulb configurations.
    """
    read_in = []
    
    try:
        with open(filename, 'rt', encoding='utf8') as input:
            reader = csv.reader(input, delimiter=';')
            for row in reader:
                row_float=[]
    
                # Not all houses have the same amount of light bulbs -> to prevent errors, 
                # since "" is not translatable into a float, we have to filter the values:
                i = 0
                while (i < len(row) and row[i] != ""):
                    row_float.append(float(row[i]))
                    i += 1
                read_in.append(row_float)
    except:
        with open(filename, 'r') as input:
            reader = csv.reader(input, delimiter=';')
            for row in reader:
                row_float=[]
    
                # Not all houses have the same amount of light bulbs -> to prevent errors, 
                # since "" is not translatable into a float, we have to filter the values:
                i = 0
                while (i < len(row) and row[i] != ""):
                    row_float.append(float(row[i]))
                    i += 1
                read_in.append(row_float)
   
    return read_in[index] # this is the desired house configuration.
    

def run_lighting_simulation(vOccupancyArray, vBulbArray, vIrradianceArray, light_mod_config):
    # Instantiate LightingModelConfiguration (with standard values)
#    light_mod_config = LightingModelConfiguration()
    
    # Determine the irradiance threshold of this house
    iIrradianceThreshold = random.gauss(light_mod_config.ext_irr_threshold_mean,
                                        light_mod_config.ext_irr_threshold_std_dev)
    
    # "Clear the target area"
    result = []
    
    # Get the bulb data
#    vBulbArray = load_lighting.load_lighting_profile(path + '\\HouseSpecification\\', 'LightBulbs.csv', 0)
    iNumBulbs = len(vBulbArray)    
    
    # Load the irradiance array    
#    vIrradianceArray = load_lighting.load_irradiance(path + '\\ConstantInputs\\','SolarIrradiance.csv', iMonth)
    
    # Get the calibration scalar
    fCalibrationScalar = light_mod_config.calib_scalar
    
    # For each bulb
    for i in range(iNumBulbs):
        # Reset counter for current light bulb
        consumption = []        
        
        # Get the bulb rating
        iRating = vBulbArray[i]
        
        # Assign a random bulb use weighting to this bulb
        # Note that the calibration scalar is multiplied here to save processing time later
        fCalibratedRelativeUseWeighting = fCalibrationScalar * light_mod_config.relative_bulb_use_weighting()

        iTime = 0 #Counter variable
        # Calculate the bulb usage at each minute of the day (24*60 minutes)
        while iTime < 24*60: 
            # Is this bulb switched on to start with?
            # This concept is not implemented in this example.
            # The simplified assumption is that all bulbs are off to start with.
            
            # Get the irradiance for this minute
            iIrradiance = vIrradianceArray[iTime]

            # Get the number of current active occupants for this minute
            # Convert from 10 minute to 1 minute resolution
            iActiveOccupants = vOccupancyArray[int(iTime / 10.0)]
            
            # Determine if the bulb switch-on condition is passed
            # ie. Insuffient irradiance and at least one active occupant
            # There is a 5% chance of switch on event if the irradiance is above the threshold
            bLowIrradiance = ((iIrradiance < iIrradianceThreshold) or (random.random() < 0.05))            
            
            # Get the effective occupancy for this number of active occupants to allow for sharing
            fEffectiveOccupancy = light_mod_config.eff_occupancy[iActiveOccupants]
            
            # Check the probability of a switch on at this time
            if (bLowIrradiance and (random.random() < (fEffectiveOccupancy * fCalibratedRelativeUseWeighting))):
                
                # This is a switch on event
                
                # Determine how long this bulb is on for
                r1 = random.random()
                cml = 0
                
                j = 1
                while j <= 9:
                    
                    #  Get the cumulative probability of this duration
                    cml = j / 9 # Equally distributed probabilities
                    
                    # Check to see if this is the type of light
                    if r1 < cml:
                        # Get the durations
                        iLowerDuration = light_mod_config.light_event_lower_value[j-1]
                        iUpperDuration = light_mod_config.light_event_upper_value[j-1]
                        
                        # Get another random number
                        r2 = random.random()
                        
                        # Guess a duration in this range
                        iLightDuration = (r2 * (iUpperDuration - iLowerDuration)) + iLowerDuration
                                                  
                        # Exit the loop
                        break;
                    
                    j += 1
                    
                j = 1
                while j <= iLightDuration:
                    # Range check
                    if iTime > 24*60-1:
                        break
                    
                    # Get the number of current active occupants for this minute
                    iActiveOccupants = vOccupancyArray[int(iTime / 10.0)]
                    
                    # If there are no active occupants, turn off the light
                    if iActiveOccupants == 0:
                        break
                    
                    # Store the demand
                    consumption.append(iRating)
                        
                    # Increment the time
                    iTime += 1
                
            else:
                # The bulb remains off
                consumption.append(0)
                
                # Increase counter
                iTime += 1                    
            
        
        result.append(consumption)
        
    return result
