#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 21:24:23 2015

@author: Thomas
"""

import random
import math
import numpy as np

class Appliances:
    """ Class to hold all relevant variables:
        Appliances.data -> data stored in the csv input file
        Appliances.calib_cycles -> calibrated cycles (calibration_factor*base_cycles)

    row     row_float       meaning
    0       not imported    Orientation (Cold, Cooking, Consumer electronics)
    1       not imported    Device (TV, Oven, PC, Microwave)
    2       0               User owns such an appliance (1 for yes, 0 for no)
    3       1               Dwellings with such a device
    4       2               Cycles per year
    5       3               Mean cycle length
    6       4               Mean cycle power
    7       5               Standby power
    8       6               Restart delay
    9       7               Occupancy dependent (1 for yes, 0 for no) - device is only active if user is at home
    10      8               Activity use profile (Number code, see below ***)
    11      9               Activity probability
    12      10              Appliance mean power factor
    
    *** Codes for the activity profile:
    0 - watching TV
    1 - cooking
    2 - doing laundry
    3 - washing
    4 - ironing
    5 - cleaning the house (vacuuming)
    6 - ACTIVE OCC (not further described in original tool)
    7 - LEVEL (not further described in original tool)
    8 - CUSTOM (not further described in original tool)
    """
    
    def comp_calib_cycles(self, calibration_factor):
        calib_cycles = []
        for rows in self.data:
            calib_cycles.append(rows[2]*calibration_factor)
        return calib_cycles
        
    def comp_mean_energy_demand(self):
        mean_energy_demand = []
        for rows in self.data:
            mean_energy_demand.append(rows[3]*rows[4] / (60*1000))
        return mean_energy_demand
        
    def comp_time_running(self):
        time_running = []
        for rows in range(len(self.data)):
            time_running.append(self.data[rows][3]*self.calib_cycles[rows])
        return time_running

    def comp_time_not_running(self):
        time_not_running = []
        for rows in self.time_running:
            time_not_running.append(365*24*60-rows)
        return time_not_running
    
    def comp_proportion_starts_occupancy(self, mean_active_occupancy):
        proportion_starts_occupancy = []
        for rows in self.data:
            if(rows[7] == 0):
                temp = 1
            else:
                temp = mean_active_occupancy
            
            proportion_starts_occupancy.append(temp)
        return proportion_starts_occupancy 
    
    def comp_minutes_events(self):
        minutes_events = []
        for rows in range(len(self.data)):
            minutes_events.append(365*24*60*self.proportion_starts_occupancy[rows]-self.time_running[rows]-self.calib_cycles[rows]*self.data[rows][6])
        return minutes_events

    # Mean time between start etvents given occupancy is NOT computed!
    # This value sometimes suffers from division by zero. Instead only its
    # reciprocal, _lambda is computed (please notice the _ before lambda. This
    # is necessary, since lambda defines short functions in Python!)
        
    def comp_lambda(self):
        _lambda = []
        for rows in range(len(self.data)):
            _lambda.append(self.calib_cycles[rows]/self.minutes_events[rows])
        return _lambda
        
    def comp_calib_scalar(self):
        calib_scalar = []
        for rows in range(len(self.data)):
            calib_scalar.append(self._lambda[rows]/self.data[rows][9])
        return calib_scalar
        
    def comp_energy_used(self):
        energy_used = []
        for rows in range(len(self.data)):
            energy_used.append(self.calib_cycles[rows]*self.mean_energy_demand[rows])
        return energy_used    

    def comp_energy_standby(self):
        energy_standby = []
        for rows in range(len(self.data)):
            energy_standby.append(self.time_not_running[rows]*self.data[rows][5]/(60*1000))
        return energy_standby    
        
    def comp_energy_total(self):
        energy_total = []
        for rows in range(len(self.data)):
            energy_total.append(self.energy_standby[rows]+self.energy_used[rows])
        return energy_total    
        
    def comp_energy_total_ownership(self):
        energy_total_ownership = []
        for rows in range(len(self.data)):
            energy_total_ownership.append(self.energy_total[rows]*self.data[rows][1])
        return energy_total_ownership    

    def load_appliances(self, filename):
        """
        Load the installed appliances
        """
#        result = []
#        
#        with open(filename, 'rb') as input:
#            reader = csv.reader(input, delimiter=';')
#            reader.next() # Skip first line!
#            for row in reader:
#                row_float=[]
#                for col in row[2:]:
#                    row_float.append(float(col))
#
#                result.append(row_float)
#    
#        self.data = result
        self.data = np.loadtxt(filename, 
                               delimiter=";", 
                               skiprows=1, 
                               usecols=range(2,13))
    
    def randomize(self):
        """
        """
        for app in self.data:
            if random.random() <= app[1]:
                app[0] = 1
            else:
                app[0] = 0
                
    
    def __init__(self,
                 filename,
                 calibration_factor=1,
                 mean_active_occupancy=0.459,
                 randomize_appliances=False):
        """
        """
        self.load_appliances(filename)

        if randomize_appliances:
            self.randomize()
        
        self.calib_cycles = self.comp_calib_cycles(calibration_factor)
        self.mean_energy_demand = self.comp_mean_energy_demand()
        self.time_running = self.comp_time_running()
        self.time_not_running = self.comp_time_not_running()
        self.proportion_starts_occupancy = self.comp_proportion_starts_occupancy(mean_active_occupancy)
        self.minutes_events = self.comp_minutes_events()
        self._lambda = self.comp_lambda()
        self.calib_scalar = self.comp_calib_scalar()
        self.energy_used = self.comp_energy_used()
        self.energy_standby = self.comp_energy_standby()
        self.energy_total = self.comp_energy_total()
        self.energy_total_ownership = self.comp_energy_total_ownership()
        


def get_power_usage(iCycleTimeLeft, sApplianceType, iStandbyPower, iRatedPower):
    # Set the return power to the rated power
    result = iRatedPower    
    
    # Some appliances have a custom (variable) power profile depending on the time left
    if sApplianceType == 26 or sApplianceType == 27: #"WASHING_MACHINE", "WASHER_DRYER"
        # Calculate the washing cycle time        
        if sApplianceType == 26:
            iTotalCycleTime = 138
        else:
            iTotalCycleTime = 198
            
        # This is an example power profile for an example washing machine
        # This simplistic model is based upon data from personal communication with a major washing maching manufacturer
        temp = iTotalCycleTime - iCycleTimeLeft + 1
        
        if temp > 0 and temp <= 8: 
            result = 73 # Start-up and fill
        elif temp > 8 and temp <= 29:
            result = 2056 # Heating
        elif temp > 29 and temp <= 81:
            result = 73 # Wash and drain
        elif temp > 81 and temp <= 92:
            result = 73 # Spin
        elif temp > 92 and temp <= 94:
            result = 250 # Rinse
        elif temp > 94 and temp <= 105:
            result = 73 # Spin
        elif temp > 105 and temp <= 107:
            result = 250 # Rinse
        elif temp > 107 and temp <= 118:
            result = 73 # Spin
        elif temp > 118 and temp <= 120:
            result = 250 # Rinse
        elif temp > 120 and temp <= 131:
            result = 73 # Spin
        elif temp > 131 and temp <= 133:
            result = 250 # Rinse            
        elif temp > 133 and temp <= 138:
            result = 568 # Fast spin
        elif temp > 138 and temp <= 198:
            result = 2500 # Drying cycle
        else:
            result = iStandbyPower                  
    
    return result

def cycle_length(iMeanCycleLength, sApplianceType):
    # Set the value to that provided in the configuration
    result = iMeanCycleLength
    
    # Use the TV watching length data approximation, derived from the TUS data
    if (sApplianceType == 14) or (sApplianceType == 15) or (sApplianceType == 16):
        # The cycle length is approximated by the following function
        # The avergage viewing time is approximately 73 minutes
        result = round(70.0 * (- math.log(1 - random.random())) ** 1.1)
        
    elif (sApplianceType == 31) or (sApplianceType == 32):
        # Provide some variation on the cycle length of heating appliances
        result = random.gauss(float(iMeanCycleLength), iMeanCycleLength / 10)
        
    return result

def start_appliance(iRestartDelay, iCycleTimeLeft, sApplianceType, iStandbyPower, iRatedPower, iMeanCycleLength):
    #Determine how long this appliance is going to be on for
    iCycleTimeLeft = cycle_length(iMeanCycleLength, sApplianceType)
    
    # Determine if this appliance has a delay after the cycle before it can restart
    iRestartDelayTimeLeft = iRestartDelay
    
    # Set the power
    iPower = get_power_usage(iCycleTimeLeft, sApplianceType, iStandbyPower, iRatedPower)
    
    # Decrement the cycle time left
    iCycleTimeLeft = iCycleTimeLeft - 1
    
    return [iCycleTimeLeft, iPower, iRestartDelayTimeLeft]

def get_length_months():
          # JAN FEB MRZ APR MAI JUN JUL AUG SEP OKT NOV DEZ
    return [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]    

def date_add(number, date):
    """ 
    Problem: Usage of a VBA built-in function called DateAdd.
    
    According to the VBA manual, this function adds a _number_ of days to the given _date_
    The return value is (in the Richardson tool) definded as a "day"-type. Therefore, we return an integer.
    Parameter date a list with the following meaning: [day, month, year]
    """    
    length_months = get_length_months()

    #Compute the day-equivalent of the current date.
    #Example:   January second: 2
    #           February 5: 5+31 = 36
    current_day = date[0]
    for i in range(date[1]-1):
        current_day = current_day + length_months[i]
    
    # If the result is below 1 (January first), we have to add days
    # If the result is above 365, we have to subtract days
    # Elegant solution: Usage of the modulo operator!
    result = [(current_day + number - 1) % 365] + 1

    return result

def date_part(day):
    """
    Problem: Richardson tool uses a VBA built-in function called DatePart.
    
    According to the VBA manual, this function adds a _number_ of days to the given _date_
    The return value is (in the Richardson tool) definded as a "month"-type. Therefore, we return an integer.
        If the return month represents January, we return 1 (NOT 0 - as lists usuall begin with)
    Parameter day represents the integer value of the corresponding date (January first -> 1, December 31st -> 365)
    """
    length_months = get_length_months()
    
    temp_day = day
    result = 0
    while temp_day > 0:
        temp_day = temp_day - length_months[result]
        result += 1
        
    return result
    

def run_application_simulation(occupancy_distribution, app, activity_statistics, iMonth=1):
    """
    Direct portation from original Richardson file
    """
    
    # Define the relative monthly temperatures
    # Data derived from MetOffice temperature data for the Midlands in 2007 (http://www.metoffice.gov.uk/climate/uk/2007/) Crown Copyright
    oMonthlyRelativeTemperatureModifier = [1.63, 1.821, 1.595, 0.867, 0.763, 0.191, 0.156, 0.087, 0.399, 0.936, 1.561, 1.994]
    
    # Array for storing the results is initialized (in VBA, this is already done with the right dimensions)
    result = []
    
    # Remake of the Excel-Sheet that stores the appliances' data:
#    app = Appliances(path+'\\HouseSpecification\\', 'Appliances.csv')
    
#    # Not in the original Richardson Tool: Generate a new distribution of the installed appliances:
#    if redistribute == True: 
#        for i in range(33):     # For all appliances:
#            if random.random() < app.data[i][1]:
#                app.data[i][0] = 1
#            else:
#                app.data[i][0] = 0
    
    # For all appliances:
    for i in range(33):
        
        # Initialization
        iCycleTimeLeft = 0
        iRestartDelayTimeLeft = 0
        
        #skip sApplianceType. This is not exported in the csv file. The few times it is needed, we will "improvise" by using the iterator "i"
        iMeanCycleLength = app.data[i][3]
        iCyclesPerYear = app.calib_cycles[i]
        iStandbyPower = app.data[i][5]
        iRatedPower = app.data[i][4]
        dCalibration = app.calib_scalar[i]
        #dOwnership = app.data[i][1]  -- Part of the Richardson tool, but never used during the computation ...
        #iTargetAveragekWhYear = app.comp_energy_total[i]  -- Part of the Richardson tool, but never used during the computation ...
        sUseProfile = app.data[i][8]
        iRestartDelay = app.data[i][6]
        bHasAppliance = app.data[i][0]
        
        #Formatting the output --- not necessary
        
        # Check if this appliance is assigned to this dwelling
        if bHasAppliance == 0: # Device is NOT installed in the current building
            no_consumption = []
            for j in range(24*60): # 24 hours with 60 minutes each
                no_consumption.append(0)
            result.append(no_consumption)
        else: # Device is installed in the current building:
        
            # Randomly delay the start of appliances that have a restart delay (e.g. cold appliances with more regular intervals)
            iRestartDelayTimeLeft = random.random() * iRestartDelay * 2  # Weighting is 2 just to provide some diversity
            
            # Make the rated power variable over a normal distribution to provide some variation
            iRatedPower = random.gauss(iRatedPower, iRatedPower/10)
            
            consumption = []            
            
            # Loop through each minute of the day
            for j in range(24*60): # 24 hours with 60 minutes each
                
                # Set the default (standby) power demand at this time step
                iPower = iStandbyPower
            
                # Get the ten minute period count
                iTenMinuteCount = int(math.floor(j / 10.0))
            
                # Get the number of current active occupants for this minute
                # Convert from 10 minute to 1 minute resolution
                iActiveOccupants = occupancy_distribution[iTenMinuteCount]

                #Now generate a key to get the activity statistics
                # This key is generated in VBA, but not applied at this point.
                # Key uses:
                    #bWeekend
                    #iActiveOccupants
                    #sUseProfile
                
                # If this appliance is off having completed a cycle (ie. a restart delay)
                if (iCycleTimeLeft <= 0) and (iRestartDelayTimeLeft > 0):
                    # Decrement the cycle time left
                    iRestartDelayTimeLeft = iRestartDelayTimeLeft - 1
                    
                elif iCycleTimeLeft <= 0: # Else if this appliance is off
                    # There must be active occupants, or the profile must not depend on occupancy for a start event to occur
                   #If (iActiveOccupants > 0 And sUseProfile <> "CUSTOM") Or (sUseProfile = "LEVEL") Then
                    if (iActiveOccupants > 0 and sUseProfile != 8) or (sUseProfile == 7):
                        # Variable to store the event probability (default to 1)
                        dActivityProbability = 1
                        
                        #For appliances that depend on activity profiles and is not a custom profile ...
                        if sUseProfile < 6: # neither ActiveOCC nor Level nor Custom
                            # Get the probability for this activity profile for this time step
                            # Five activity slots (sUseProfile) for each occupant number
                            # Second index: 0: occupant number, 1: activity code (sUseProfile), 2: Time from 00_00 until 00_10, 3: Time from 00_10 until 00_20 ...
                            dActivityProbability = activity_statistics[int(5*iActiveOccupants + sUseProfile)][iTenMinuteCount+2]

                        # For electric space heaters ... (excluding night storage heaters)
                        elif i == 31: #(sApplianceType = "ELEC_SPACE_HEATING")
                            # If this appliance is an electric space heater, then the activity probability is a function of the month of the year
                            dActivityProbability = oMonthlyRelativeTemperatureModifier[iMonth-1]
                        
                        # Check the probability of a start event
                        if random.random() < (dCalibration * dActivityProbability):
                            # This is a start event
                            [iCycleTimeLeft, iPower, iRestartDelayTimeLeft] = start_appliance(iRestartDelay, iCycleTimeLeft, i, iStandbyPower, iRatedPower, iMeanCycleLength)
                    
                    # Custom appliance handler: storage heaters have a simple representation
                elif sUseProfile == 8: #Notice: This clause is overdefined in the original Richardson tool... I simplified it!
                    # The number of cycles (one per day) set out in the calibration sheet
                    # is used to determine whether the storage heater is used
                    
                    # This model does not account for the changes in the Economy 7 time
                    # It assumes that the time starts at 00:30 each day
                    if (iTenMinuteCount == 4): # ie. 00:30 - 00:40
                        # Assume January 14th is the coldest day of the year
                        oDate = [14, 1, 1997] #VBA: oDate = #1/14/1997#
                        
                        #Get the month and day when the storage heaters are turned on and off, using the number of cycles per year
                        oDateOff = date_add(round(iCyclesPerYear/2), oDate)
                        oDateOn = date_add(-round(iCyclesPerYear/2), oDate)
                        iMonthOff = date_part(oDateOff)
                        iMonthOn = date_part(oDateOn)
                            
                        #If this is a month in which the appliance is turned on of off
                        if (iMonth == iMonthOff) or (iMonth == iMonthOn):
                            # Pick a 50% chance since this month has only a month of year resolution
                            dProbability = 0.5 / 10  # (since there are 10 minutes in this period)
                        elif (iMonth > iMonthOff) and (iMonth < iMonthOn):
                            # The appliance is not used in summer
                            dProbability = 0
                        else:
                            # The appliance is used in winter
                            dProbability = 1
                            
                        #Determine if a start event occurs
                        if (random.random() <= dProbability):
                            # This is a start event
                            [iCycleTimeLeft, iPower, iRestartDelayTimeLeft] = start_appliance(iRestartDelay, iCycleTimeLeft, i, iStandbyPower, iRatedPower, iMeanCycleLength)
                            

                else: # The appliance is on - if the occupants become inactive, switch off the appliance
                    if (iActiveOccupants == 0) and (sUseProfile != 7) and (sUseProfile != 2) and (sUseProfile != 8):
                       #(iActiveOccupants = 0) and (sUseProfile <> "LEVEL") and (sUseProfile <> "ACT_LAUNDRY") and (sUseProfile <> "CUSTOM"):  
                    
                        # Do nothing. The activity will be completed upon the return of the active occupancy.
                        # Note that LEVEL means that the appliance use is not related to active occupancy.
                        # Note also that laundry appliances do not switch off upon a transition to inactive occupancy.
                        pass
                    else:    
                        # Set the power
                        iPower = get_power_usage(iCycleTimeLeft, i, iStandbyPower, iRatedPower)
                        
                        # Decrement the cycle time left
                        iCycleTimeLeft = iCycleTimeLeft - 1
                
                consumption.append(iPower)
            
            result.append(consumption)
    
    return result