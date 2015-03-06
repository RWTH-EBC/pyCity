# -*- coding: utf-8 -*-
"""
Created on Wed Aug 06 12:34:23 2014

@author: tsz

This file contains a few characteristic curves of real HP units
"""

import numpy as np

class HPCharacteristics(object):
    """
    This class currently holds the following heat pumps 
    -------------
    - `Manufacturer` -- Model -- Nominal heat output / COP
    - Dimplex -- LA 12 TU -- 9.60 / 3.70 
    """

    def __init__(self, qNominal):
        """
        Parameters
        ----------
        qNominal : Float
            Minimum required heat output at 2 °C ambient temperature and 
            35 °C flow temperature.
        """
        if qNominal > 9200:
            [tAmbient, tFlow, heat, power, tMax] = self._getDimplexLA12TU()
        else:
            [tAmbient, tFlow, heat, power, tMax] = self._getDimplexLA9TU()
        
        self.tAmbient = tAmbient
        self.tFlow = tFlow
        self.heat = heat
        self.power = power
        self.tMax = tMax
        
    def getCharacteristics(self):
        """
        Return the characteristics of the heat pump
        
        Returns
        -------
        tAmbient : Array_like (one dimensional)
            Array of ambient temperatures for which heat output and 
            electricity consumption are available
        tFlow : Array_like (one dimensional)
            Array of flow temperatures for which heat output and electricity 
            consumption are available
        heat : Array_like (two dimensional)
            - Nominal heat output as function of tFlow and tAmbient.
            - Shape: (len(tAmbient), len(tFlow))
        power : Array_like (two dimensional)
            - Nominal electricity consumption as function of tFlow and tAmbient.
            - Shape: (len(tAmbient), len(tFlow))
        tMax : Float
            Maximum temperature the device can provide.
        """
        return (self.tAmbient, self.tFlow, self.heat, self.power, self.tMax)
    
    # From here on, only characteristics of heat pumps are stored.
    # This could also for example be done in a database...
    def _getDimplexLA12TU(self):
        """ http://www.dimplex.de/pdf/de/produktattribute/produkt_1725609_extern_egd.pdf """
        tAmbient = np.array([-20, -15, -7, 2, 7, 10, 12, 20])
        tFlow = np.array([35, 45, 55])
        q = np.array([[4.89, 4.7,   4.5], 
                      [5.87, 5.7,   5.5], 
                      [7.6,  7.35,  7.17],
                      [9.6,  9.1,   8.8],
                      [11.4, 10.85, 9.8],
                      [11.7, 11.2,  10.6],
                      [12.2, 11.4,  10.9],
                      [13.6, 12.8,  12.39]])
                      
        p = np.array([[2.56, 3.18, 3.75],
                      [2.57, 3.22, 3.79],
                      [2.53, 3.2,  3.81],
                      [2.59, 3.2,  3.79],
                      [2.65, 3.17, 3.92],
                      [2.54, 3.17, 3.85],
                      [2.55, 3.2,  3.8],
                      [2.55, 3.15, 3.75]])

        tMax = 60        
        
        return [tAmbient, tFlow, q, p, tMax]
    
    def _getDimplexLA9TU(self):
        """ http://www.dimplex.de/pdf/de/produktattribute/produkt_1725608_extern_egd.pdf """
        tAmbient = np.array([-20, -15, -7, 2, 7, 10, 12, 20])
        tFlow = np.array([35, 45, 55])
        q = np.array([[2.96,   2.26,  2.03], 
                      [3.73,   3.15,  2.78], 
                      [5.50,   4.56,  3.98],
                      [7.50,   6.53,  5.88],
                      [9.20,   8.21,  7.10],
                      [10.20,  8.88,  7.81],
                      [11.45, 10.29,  9.11],
                      [12.70, 11.70, 10.40]])
                   
        cop = np.array([[1.86, 1.42, 1.28], 
                        [2.16, 1.79, 1.51], 
                        [2.80, 2.28, 1.87],
                        [3.70, 2.86, 2.45],
                        [4.20, 3.62, 2.70],
                        [4.50, 3.55, 2.95],
                        [4.77, 4.04, 3.31],
                        [5.29, 4.33, 3.48]])
                   
        p = q / cop
        
        tMax = 60
        
        return [tAmbient, tFlow, q, p, tMax]