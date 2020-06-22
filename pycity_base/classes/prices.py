#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 09 16:19:18 2015

@author: tsz
"""

from __future__ import division


class Prices(object):
    """
    Class that keeps track of the current market conditions (prices and 
    remuneration)
    """
    
    def __init__(self, 
                 revenue_chp=5.41,
                 costs_electricity=30,
                 revenue_electricity=10,
                 costs_gas=6.6):
        """
        Prices and revenue for different goods (all input values in €-ct/kWh)        
        
        Parameters
        ----------
        revenue_chp : float
            revenue for generated electricity from CHP
        costs_electricity : float
            costs for electricity imports
        revenue_electricity : float
            feed-in remuneration
        costs_gas : float
            costs for gas consumption
        """
        self._kind = "prices"        
                
        kWh_to_J = 3600 * 1000
        cents_in_euro = 100
        
        self.rev_chp = revenue_chp / (kWh_to_J * cents_in_euro)
        self.costs_electricity = costs_electricity / (kWh_to_J * cents_in_euro)
        self.revenue_electricity = revenue_electricity / (kWh_to_J * cents_in_euro)
        self.costs_gas = costs_gas / (kWh_to_J * cents_in_euro)

    @property
    def kind(self):
        return self._kind
        
    def getAllData(self):
        """
        Return all market information.
        
        Order: Electricity costs, gas costs, CHP revenue, feed-in remuneration
        """
        return (self.costs_electricity, self.costs_gas, self.rev_chp, self.revenue_electricity)
    
    def setAllData(self, costs_electricity=None, costs_gas=None, rev_chp=None, revenue_electricity=None):
        """
        Update multiple market data.
        """
        if costs_electricity != None:
            self.costs_electricity = costs_electricity
        if costs_gas != None:
            self.costs_gas = costs_gas
        if rev_chp != None:
            self.rev_chp = rev_chp
        if revenue_electricity != None:
            self.revenue_electricity = revenue_electricity
