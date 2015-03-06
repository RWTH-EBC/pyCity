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
    
    def __init__(self, revenueChp=5.41, costsElectricity=30, revenueElectricity=10, costsGas=6.6):
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
        
        self.revChp = revenueChp / (kWh_to_J * Cents_in_Euro)
        self.cEl    = costsElectricity / (kWh_to_J * Cents_in_Euro)
        self.revEl  = revenueElectricity / (kWh_to_J * Cents_in_Euro)
        self.cGas   = costsGas / (kWh_to_J * Cents_in_Euro)
        
    def getRevenueChp(self):
        """ 
        Return governmental subsidies for generated electrictiy from CHP (in
        €/J)
        """
        return self.revChp
        
    def getCostsElectricity(self):
        """ Return costs for electricity imports (in €/J) """
        return self.cEl
        
    def getRevenueElectricity(self):
        """ Return feed-in remuneration for electricity (in €/J) """
        return self.revChp
        
    def getCostsGas(self):
        """ Return costs for gas (in €/J) """
        return self.cGas

    def getAllData(self):
        """
        Return all market information.
        
        Order: Electricity costs, gas costs, CHP revenue, feed-in remuneration
        """
        return (self.getCostsElectricity(), self.getCostsGas(), self.getRevenueChp(), self.getRevenueElectricity())
    
    def setRevenueChp(self, revenueChp, perKWh=True):
        """ 
        Set a new value for governmental subsidies for CHP units 
        
        Parameters
        ----------
        revenueChp : float
            revenue for generated electricity from CHP
        perKWh : boolean, optional
            True if the given value is in €-ct / kWh
            False if the given value is in € / J
        """
        if perKWh:
            kWh_to_J = 3600 * 1000
            Cents_in_Euro = 100
            
            self.revChp = revenueChp / (kWh_to_J * Cents_in_Euro)
        else:
            self.revChp = revenueChp
            
    def setCostsElectricity(self, costsElectricity, perKWh=True):
        """ 
        Set a new value for electricity costs
        
        Parameters
        ----------
        costsElectricity : float
            costs for electricity imports
        perKWh : boolean, optional
            True if the given value is in €-ct / kWh
            False if the given value is in € / J
        """
        if perKWh:
            kWh_to_J = 3600 * 1000
            Cents_in_Euro = 100
            
            self.cEl = costsElectricity / (kWh_to_J * Cents_in_Euro)
        else:
            self.cEl = costsElectricity
            
    def setRevenueElectricity(self, revenueElectricity, perKWh=True):
        """ 
        Set a new value for feed-in remuneration
        
        Parameters
        ----------
        revenueElectricity : float
            feed-in remuneration
        perKWh : boolean, optional
            True if the given value is in €-ct / kWh
            False if the given value is in € / J
        """
        if perKWh:
            kWh_to_J = 3600 * 1000
            Cents_in_Euro = 100
            
            self.revEl = revenueElectricity / (kWh_to_J * Cents_in_Euro)
        else:
            self.revEl = revenueElectricity
            
    def setCostsGas(self, costsGas, perKWh=True):
        """ 
        Set a new value for gas costs
        
        Parameters
        ----------
        costsGas : float
            costs for gas consumption
        perKWh : boolean, optional
            True if the given value is in €-ct / kWh
            False if the given value is in € / J
        """
        if perKWh:
            kWh_to_J = 3600 * 1000
            Cents_in_Euro = 100
            
            self.cGas = costsGas / (kWh_to_J * Cents_in_Euro)
        else:
            self.cGas = costsGas
