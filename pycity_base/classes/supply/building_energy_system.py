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
        
        self._kind = "bes"
        
        # Initialize all devices as empty lists
        self.battery = []
        self.boiler = []
        self.chp = []
        self.electricalHeater = []
        self.heatpump = []
        self.inverterAcdc = []
        self.inverterDcac = []
        self.pv = []
        self.tes = []
        
        # The new BES is still empty
        self.has_battery = False
        self.has_boiler = False
        self.has_chp = False
        self.has_electrical_heater = False
        self.has_heatpump = False
        self.has_inverter_acdc = False
        self.has_inverter_dcac = False
        self.has_pv = False
        self.has_tes = False

    @property
    def kind(self):
        return self._kind
        
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
            self.battery.append(objectInstance)
            self.has_battery = True
        
        elif objectInstance.kind == "boiler":
            self.boiler.append(objectInstance)
            self.has_boiler = True
        
        elif objectInstance.kind == "chp":
            self.chp.append(objectInstance)
            self.has_chp = True
        
        elif objectInstance.kind == "electricalheater":
            self.electricalHeater.append(objectInstance)
            self.has_electrical_heater = True
        
        elif objectInstance.kind == "heatpump":
            self.heatpump.append(objectInstance)
            self.has_heatpump = True
        
        elif objectInstance.kind == "inverter":
            if objectInstance.input_AC:
                self.inverterAcdc.append(objectInstance)
                self.has_inverter_acdc = True
            else:
                self.inverterDcac.append(objectInstance)
                self.has_inverter_dcac = True
        
        elif objectInstance.kind == "pv":
            self.pv.append(objectInstance)
            self.has_pv = True
            
        elif objectInstance.kind == "tes":
            self.tes.append(objectInstance)
            self.has_tes = True
            
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
            result = (self.has_battery,
                      self.has_boiler,
                      self.has_chp,
                      self.has_electrical_heater,
                      self.has_heatpump,
                      self.has_inverter_acdc,
                      self.has_inverter_dcac,
                      self.has_pv,
                      self.has_tes)

        else:
            result = ()
            if battery:
                result += (self.has_battery,)
                
            if boiler:
                result += (self.has_boiler,)

            if chp:
                result += (self.has_chp,)

            if electricalHeater:
                result += (self.has_electrical_heater,)

            if heatpump:
                result += (self.has_heatpump,)

            if inverterAcdc:
                result += (self.has_inverter_acdc,)

            if inverterDcac:
                result += (self.has_inverter_dcac,)

            if pv:
                result += (self.has_pv,)
                
            if tes:
                result += (self.has_tes,)
        
        return result
