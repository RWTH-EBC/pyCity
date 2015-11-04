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
                 revenueChp=5.41, 
                 costsElectricity=30, 
                 revenueElectricity=10, 
                 costsGas=6.6):
        """
        Prices and revenue for different goods (all input values in €-ct/kWh)        
        
        Parameters
        ----------
        revenueChp : float
            revenue for generated electricity from CHP
        costsElectricity : float
            costs for electricity imports
        revenueElectricity : float
            feed-in remuneration
        costsGas : float
            costs for gas consumption
        """
        self._kind = "prices"        
                
        kWh_to_J = 3600 * 1000
        Cents_in_Euro = 100
        
        self.revChp   = revenueChp / (kWh_to_J * Cents_in_Euro)
        self.costsEl  = costsElectricity / (kWh_to_J * Cents_in_Euro)
        self.revEl    = revenueElectricity / (kWh_to_J * Cents_in_Euro)
        self.costsGas = costsGas / (kWh_to_J * Cents_in_Euro)
        
    def getAllData(self):
        """
        Return all market information.
        
        Order: Electricity costs, gas costs, CHP revenue, feed-in remuneration
        """
        
        return (self.costsEl, self.costsGas, self.revChp, self.revEl)
    
    def setAllData(self, costsEl=None, costsGas=None, revChp=None, revEl=None):
        """
        Update multiple market data.
        """
        
        if costsEl != None:
            self.costsEl = costsEl
        if costsGas != None:
            self.costsGas = costsGas
        if revChp != None:
            self.revChp = revChp
        if revEl != None:
            self.revEl= revEl
