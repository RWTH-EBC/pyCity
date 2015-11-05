#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 11 14:19:13 2015

@author: tsz
"""

from __future__ import division


def saveResult(timer, currentAttribute, totalAttribute, currentResult):
    """ 
    Save the current result in currentAttribute and append to totalAttribute 
    
    Parameters
    ----------
    timer : Timer instance
        Pointer to the common timer instance
    currentAttribute : Array-like
        Attribute for the results of the current optimization period
    totalAttribute : Array-like
        Attribute for the results of all optimization periods
    currentResult : Array-like
        Results of the current optimization period
        
    Returns
    -------
    Returns a tuple of updated currentAttribute and totalAttribute
    
    Example
    -------
    >>> # Save the results of a scheduling optimization
    >>> # Due to limited space, the variable names are shortened
    >>> # cS --> currentSchedule, tS --> totalSchedule
    >>> schedule = optimizer(...)
    >>> (self.cS, self.tS) = saveResult(timer, self.cS, self.tS, schedule)
    """
    # Get current and final position
    currentPosition = timer.currentTimestep
    finalPosition = currentPosition + timer.timestepsUsedHorizon
    
    # Only save the first values that are not overwritten later
    requiredResult = currentResult[0:timer.timestepsUsedHorizon]
    
    # Save the results
    currentAttribute = requiredResult
    totalAttribute[currentPosition : finalPosition] = requiredResult
    
    return (currentAttribute, totalAttribute)
    
    
def saveResultInit(timer, currentAttribute, totalAttribute, currentResult):
    """
    Save the current result in currentAttribute, append it to totalAttribute 
    and return the new initial value.
    
    Parameters
    ----------
    timer : Timer instance
        Pointer to the common timer instance
    currentAttribute : Array-like
        Attribute for the results of the current optimization period
    totalAttribute : Array-like
        Attribute for the results of all optimization periods
    currentResult : Array-like
        Results of the current optimization period
        
    Returns
    -------
    Returns a tuple of updated currentAttribute and totalAttribute as well as 
    a new initial value
    
    Example
    -------
    >>> # Save the resulting storage temperature
    >>> # Due to limited space, the variable names are shortened
    >>> # cT --> currentTSto, tT --> totalTSto, tI --> tInit
    >>> tSto = optimizer(...)
    >>> (self.cT, self.tT, self.tI) = saveResult(timer, self.cT, self.tT, tSto)
    """
    (currentAttribute, totalAttribute) = saveResult(timer, 
                                                    currentAttribute, 
                                                    totalAttribute, 
                                                    currentResult)
    init_value = currentResult[timer.timestepsUsedHorizon-1]
    
    return (currentAttribute, totalAttribute, init_value)
    
def getValues(currentValues, current, total):
    """ 
    Return either the current values (for this horizon) or all computed results

    Parameters
    ----------
    currentValues : Boolean
        True: return 'current', False: return 'total'
    current : Pointer
        Pointer to the current values
    total : Pointer
        Pointer to the total values
    """
    if currentValues:
        return current
    else:
        return total