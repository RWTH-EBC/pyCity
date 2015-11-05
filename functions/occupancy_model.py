#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 16:50:36 2015

@author: tsz
"""

from __future__ import division
import random


def all_states(tpm, initial_state):
    """ 
        Determine the active occupancy transitions for each ten minute period 
        of the day
        
        This is a direct portation of Step 3 in the Excel-Tool 
        (module Occupancy_Model)
    """

    # Start with an empty result list
    result = []
    current_state = initial_state

    i = 1
    
    while i <= 144:
        
        # Get a new random number
        fRand = random.random()
        # Reset cumulative probability count
        fCumulativeP = 0
        
        # Determine the row for this state
        iRow = 7 * (i-1) + current_state
        
        # Loop construction
        j = 0
        found = False
        
       # while (not found and j <= 7):
        while (not found and j <= 6):
            fCumulativeP = fCumulativeP + tpm[iRow][j+2]
            if (fRand < fCumulativeP or i == len(tpm[iRow])-1):
                current_state = j
                found = True
            j += 1
        
        # Store next state
        result.append(current_state)
        
        i += 1
    return result    
