#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 09 12:26:24 2015

@author: tsz
"""

from __future__ import division


class BES(object):
    """
    Building Energy System (BES) is able to contain the following devices:
        Battery, Boiler, Combined Heat and Power (CHP) unit, Electrical 
        heater, Heatpump, Inverter (AC/DC and DC/AC), Photovoltaics (PV) and 
        Thermal Energy Storage (TES) unit
    """
    
    def __init__(self, environment):
        """
        Workflow
        --------
        1 : Create an empty building energy system (BES) that only contains 
            the environment pointer
        2 : Add devices such as thermal energy storage unit to the BES, by 
            invoking the addDevice or addMultipleDevices methods.
        
        Parameter
        ---------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        """
        self.environment = environment
        
        self.__kind = "bes"
        
        # Initialize all devices as empty lists
        self.battery          = []
        self.boiler           = []
        self.chp              = []
        self.electricalHeater = []
        self.heatpump         = []
        self.inverterAcdc     = []
        self.inverterDcac     = []
        self.pv               = []
        self.tes              = []
        
        # The new BES is still empty
        self.hasBattery          = False
        self.hasBoiler           = False
        self.hasChp              = False
        self.hasElectricalHeater = False
        self.hasHeatpump         = False
        self.hasInverterAcdc     = False
        self.hasInverterDcac     = False
        self.hasPv               = False
        self.hasTes              = False

    def __str__(self):
        return str('<Building energy system (BES) object of pyCity>')

    @property
    def kind(self):
        """
        Return type of pyCity object
        """
        return self.__kind
        
    def addDevice(self, objectInstance):
        """
        Add a device object
        
        Example
        -------
        >>> myChp = CHP(...)
        >>> myBes = BES(...)
        >>> myBes.addDevice(myChp)
        """
        if objectInstance.kind == "battery":
            self.battery = objectInstance
            self.hasBattery = True
        
        elif objectInstance.kind == "boiler":
            self.boiler = objectInstance
            self.hasBoiler = True
        
        elif objectInstance.kind == "chp":
            self.chp = objectInstance
            self.hasChp = True
        
        elif objectInstance.kind == "electricalheater":
            self.electricalHeater = objectInstance
            self.hasElectricalHeater = True
        
        elif objectInstance.kind == "heatpump":
            self.heatpump = objectInstance
            self.hasHeatpump = True
        
        elif objectInstance.kind == "inverter":
            if objectInstance.inputAC:
                self.inverterAcdc = objectInstance
                self.hasInverterAcdc = True
            else:
                self.inverterDcac = objectInstance
                self.hasInverterDcac = True
        
        elif objectInstance.kind == "pv":
            self.pv = objectInstance
            self.hasPv = True
            
        elif objectInstance.kind == "tes":
            self.tes = objectInstance
            self.hasTes = True
            
    def addMultipleDevices(self, devices):
        """
        Add multiple devices to the existing BES
        
        Parameter
        ---------
        devices : List-like
            List (or tuple) of devices that are added to the BES
            
        Example
        -------
        >>> myBoiler = Boiler(...)
        >>> myChp = CHP(...)
        >>> myBes = BES(...)
        >>> myBes.addMultipleDevices([myBoiler, myChp])
        """
        for device in devices:
            self.addDevice(device)
    
    def getHasDevices(self, 
                      allDevices=True, 
                      battery=False, 
                      boiler=False, 
                      chp=False, 
                      electricalHeater=False, 
                      heatpump=False, 
                      inverterAcdc=False, 
                      inverterDcac=False, 
                      pv=False, 
                      tes=False):
        """
        Get information if certain devices are installed devices.
        The result is in alphabetical order, starting with "battery"
        
        Parameters
        ----------
        allDevices : boolean, optional
            If true: Return all installed devices
            If false: Only return the specified devices
        battery : boolean, optional
            Return information on the battery?
        boiler : boolean, optional
            Return information on the boiler?
        chp : boolean, optional
            Return information on the chp unit?
        electricalHeater : boolean, optional
            Return information on the electrical heater?
        heatpump : boolean, optional
            Return information on the heat pump?
        inverterAcdc : boolean, optional
            Return information on the AC-DC inverter?
        inverterDcac : boolean, optional
            Return information on the DC-AC inverter?
        pv : boolean, optional
            Return information on the PV modules?
        tes : boolean, optional
            Return information on the thermal energy storage?
        """
        if allDevices:
            result = (self.hasBattery, 
                      self.hasBoiler, 
                      self.hasChp, 
                      self.hasElectricalHeater, 
                      self.hasHeatpump, 
                      self.hasInverterAcdc, 
                      self.hasInverterDcac, 
                      self.hasPv, 
                      self.hasTes)

        else:
            result = ()
            if battery:
                result += (self.hasBattery,)
                
            if boiler:
                result += (self.hasBoiler,)

            if chp:
                result += (self.hasChp,)

            if electricalHeater:
                result += (self.hasElectricalHeater,)

            if heatpump:
                result += (self.hasHeatpump,)

            if inverterAcdc:
                result += (self.hasInverterAcdc,)

            if inverterDcac:
                result += (self.hasInverterDcac,)

            if pv:
                result += (self.hasPv,)
                
            if tes:
                result += (self.hasTes,)
        
        return result