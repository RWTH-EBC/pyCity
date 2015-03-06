# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 12:57:00 2015

@author: T_ohne_admin
"""

import classes.ElectricalAppliance

class Washingmachine(classes.ElectricalAppliance.ElectricalAppliance):
    """
    Implementation of the washing machine.
    """
    
    def __init__(self, environment, capacity, gains, socMayrun,
                 socInit=0, timeGains=900, thermalConnection=False, 
                 pathElectric="", delEl="\t", loadEl=[], timeEl=900, dataOnFileEl=True, 
                 pathThermal="", delTh="\t", loadTh=[], timeTh=900, dataOnFileTh=True):
        """
        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        capacity : float
            maximum capacity of the washing machine (e.g. max. clothes)
        gains : array-like
            load curve describing how the capacity of the device is used over 
            time (e.g. 2 clothes in time step 0, 5 in time step 1)
        socMayrun : float
            when is the device allowed to run? Standard operation is to set 
            socMayrun=capacity
        socInit : float, optional
            initial state of charge
        timeGains : integer, optional
            time discretization of gains
        thermalConnection : boolean, optional
            is the device connected to the building's TES?
        pathElectric : string, optional
            (electrical) loadcurve of the appliance (stored in file)
        delEl : string, optional
            delimiter used in pathElectric
        loadEl : array-like, optional
            (electrical) loadcurve of the appliance (given directly)
        dataOnFileEl : boolean, optional
            use pathElectric and delEl or use loadEl directly
        pathThermal : string, optional
            (thermal) loadcurve of the appliance (stored in file)
        delTh : string, optional
            delimiter used in pathThermal
        loadTh : array-like, optional
            (electrical) loadcurve of the appliance (given directly)
        dataOnFileTh : boolean, optional
            use pathThermal and delTh or use loadTh directly
        
        The last four are only useful if thermalConnection is True
        """
        
        super(Washingmachine, self).__init__(environment, capacity, gains, socMayrun, socInit, timeGains, thermalConnection, pathElectric, delEl, loadEl, timeEl, dataOnFileEl, pathThermal, delTh, loadTh, timeTh, dataOnFileTh)
        self._kind = "washingmachine"