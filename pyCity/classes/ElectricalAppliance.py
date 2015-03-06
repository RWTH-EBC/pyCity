# -*- coding: utf-8 -*-
"""
Created on Sun Feb 08 17:48:19 2015

@author: T_ohne_admin
"""

import Load
import numpy as np
import functions.changeResolution
import functions.handleData

class ElectricalAppliance(object):
    """
    Implementation of a general class for electrical appliances like 
    dishwashers or washingmachines.
    """
    
    def __init__(self, environment, capacity, gains, socMayrun, socInit=0, timeGains=900, thermalConnection=False,
                 pathElectric="", delEl="\t", loadEl=[], timeEl=900, dataOnFileEl=True,
                 pathThermal="",  delTh="\t", loadTh=[], timeTh=900, dataOnFileTh=True):
        """
        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        capacity : float
            maximum capacity of the electrical device (e.g. clothes/dishes)
        gains : array-like
            load curve describing how the capacity of the device is used over 
            time (e.g. 2 dishes in time step 0, 5 in time step 1)
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
        self._kind = "electricalappliance"
        # Create thermal and electrical loads
        self.loadElectrical = Load.Load(environment, pathElectric, delimiter=delEl, 
                                         timeDiscretization=timeEl, dataOnFile=dataOnFileEl)
                                         
        if thermalConnection:
            self.loadThermal = Load.Load(environment, pathThermal, delimiter=delTh, 
                                          timeDiscretization=timeTh, dataOnFile=dataOnFileTh)
        else:
            loadThermal_loadcurve = np.zeros_like(self.loadElectrical.loadcurve)
            self.loadThermal = Load.Load(environment, "", delimiter=delTh, loadcurve=loadThermal_loadcurve, 
                                          timeDiscretization=environment.getTimeDiscretization(), dataOnFile=False)

        timestepsTotal = environment.getTimestepsTotal()
        timestepsUsedHorizon = environment.getTimestepsUsedHorizon()        
        
        self.environment = environment
        self.capacity = capacity
        self.socMayrun = socMayrun
        self.socInit = socInit
        self.thermalConnection = thermalConnection
        self.totalSchedule     = np.zeros(timestepsTotal)
        self.totalSoc          = np.zeros(timestepsTotal)
        self.totalPConsumption = np.zeros(timestepsTotal)
        self.totalQConsumption = np.zeros(timestepsTotal)
        self.currentSchedule     = np.zeros(timestepsUsedHorizon)
        self.currentSoc          = np.zeros(timestepsUsedHorizon)
        self.currentPConsumption = np.zeros(timestepsUsedHorizon)
        self.currentQConsumption = np.zeros(timestepsUsedHorizon)
        if timeGains == environment.getTimeDiscretization():
            # The given gains curve already uses the common time discretization
            self.gains = gains
        else:
            # Adjust the given gains curve to the used time discretization
            self.gains = functions.changeResolution.changeResolution(gains, timeGains, environment.getTimeDiscretization())
        

    def setSchedule(self, schedule):
        """ Save the computed schedule """
        (self.currentSchedule, self.totalSchedule, self.xInit) = functions.handleData.saveResultInit(self.environment.getTimer(), self.currentSchedule, self.totalSchedule, schedule)
        
    def setSoc(self, SOC):
        """ Save the computed device's state of charge and update new initial SOC """
        (self.currentSoc, self.totalSoc, self.socInit) = functions.handleData.saveResultInit(self.environment.getTimer(), self.currentSoc, self.totalSoc, SOC)

    def setPConsumption(self, pConsumption):
        """ Save the computed electricity consumption """
        (self.currentPConsumption, self.totalPConsumption) = functions.handleData.saveResult(self.environment.getTimer(), self.currentPConsumption, self.totalPConsumption, pConsumption)
        
    def setQConsumption(self, qConsumption):
        """ Save the computed heat consumption """
        (self.currentQConsumption, self.totalQConsumption) = functions.handleData.saveResult(self.environment.getTimer(), self.currentQConsumption, self.totalQConsumption, qConsumption)
        
    def _getXInitYInit(self):
        """ Compute initial activity levels and starting indicators """
        xInit = np.zeros(len(self.loadElectrical.getLoadcurve()) + 1)
        t = self.environment.getCurrentTimestep()
        for i in xrange(min(t+1, len(xInit))):
            xInit[-1-i] = self.totalSchedule[t-1-i]

        xPrevious = xInit[0:len(xInit)-1]
        xInit = xInit[1:len(xInit)]
        yInit = (xPrevious < xInit) * 1
        
        return (np.round(xInit[-1]), np.round(yInit))
    
    def getInitialState(self):
        """ Return the device's initial state of charge, activity level and starting variable """
        (self.xInit, self.yInit) = self._getXInitYInit()
        return (self.socInit, self.xInit, self.yInit)
        
    def getGains(self):
        """ Return the device's (current) charging rate / gains """
        if self.environment.getTimestepsTotal() > len(self.gains):
            # Assumption: Gains are only provided for one forecasting horizon
            return self.gains
        else:
            # Assumption: Gans are provided for the entire computation period
            # Get the "current" gains
            currentTimestep = self.environment.getCurrentTimestep()
            finalTimestep = currentTimestep + self.environment.getTimestepsHorizon()
            return self.gains[currentTimestep : finalTimestep]
    
    def getNominals(self):
        """
        """
        return (self.capacity, self.socMayrun, self.getGains(), self.thermalConnection, self.loadElectrical.getLoadcurve(), self.loadThermal.getLoadcurve())