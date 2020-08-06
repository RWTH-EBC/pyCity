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
        
        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        """
        self.environment = environment
        
        self._kind = "bes"
        
        # Initialize all devices as empty lists
        self.battery_units = []
        self.boilers = []
        self.chp_units = []
        self.electrical_heaters = []
        self.heatpumps = []
        self.compression_chillers = []
        self.inverters_acdc = []
        self.inverters_dcac = []
        self.pv_units = []
        self.tes_units = []
        
        # The new BES is still empty
        self.has_battery = False
        self.has_boiler = False
        self.has_chp = False
        self.has_electrical_heater = False
        self.has_heatpump = False
        self.has_compression_chiller = False
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
        
        Examples
        --------
        >>> myChp = CHP(...)
        >>> myBes = BES(...)
        >>> myBes.addDevice(myChp)
        """
        if objectInstance.kind == "battery":
            self.battery_units.append(objectInstance)
            self.has_battery = True
        
        elif objectInstance.kind == "boiler":
            self.boilers.append(objectInstance)
            self.has_boiler = True
        
        elif objectInstance.kind == "chp":
            self.chp_units.append(objectInstance)
            self.has_chp = True
        
        elif objectInstance.kind == "electricalheater":
            self.electrical_heaters.append(objectInstance)
            self.has_electrical_heater = True
        
        elif objectInstance.kind == "heatpump":
            self.heatpumps.append(objectInstance)
            self.has_heatpump = True

        elif objectInstance.kind == "compressionchiller":
            self.compression_chillers.append(objectInstance)
            self.has_compression_chiller = True
        
        elif objectInstance.kind == "inverter":
            if objectInstance.input_AC:
                self.inverters_acdc.append(objectInstance)
                self.has_inverter_acdc = True
            else:
                self.inverters_dcac.append(objectInstance)
                self.has_inverter_dcac = True
        
        elif objectInstance.kind == "pv":
            self.pv_units.append(objectInstance)
            self.has_pv = True
            
        elif objectInstance.kind == "tes":
            self.tes_units.append(objectInstance)
            self.has_tes = True
            
    def addMultipleDevices(self, devices):
        """
        Add multiple devices to the existing BES
        
        Parameters
        ----------
        devices : List-like
            List (or tuple) of devices that are added to the BES
            
        Examples
        --------
        >>> myBoiler = Boiler(...)
        >>> myChp = CHP(...)
        >>> myBes = BES(...)
        >>> myBes.addMultipleDevices([myBoiler, myChp])
        """
        for device in devices:
            self.addDevice(device)
    
    def getHasDevices(self, 
                      all_devices=True,
                      battery=False, 
                      boiler=False, 
                      chp=False,
                      compression_chiller=False,
                      electrical_heater=False,
                      heatpump=False,
                      inverter_acdc=False,
                      inverter_dcac=False,
                      pv=False, 
                      tes=False):
        """
        Get information if certain devices are installed devices.
        The result is in alphabetical order, starting with "battery"
        
        Parameters
        ----------
        all_devices : boolean, optional
            If true: Return all installed devices
            If false: Only return the specified devices
        battery : boolean, optional
            Return information on the battery
        boiler : boolean, optional
            Return information on the boiler
        chp : boolean, optional
            Return information on the chp unit
        compression_chiller : boolean, optional
            Return information on the compression chiller unit
        electrical_heater : boolean, optional
            Return information on the electrical heater
        heatpump : boolean, optional
            Return information on the heat pump
        inverter_acdc : boolean, optional
            Return information on the AC-DC inverter
        inverter_dcac : boolean, optional
            Return information on the DC-AC inverter
        pv : boolean, optional
            Return information on the PV modules
        tes : boolean, optional
            Return information on the thermal energy storage
        """
        if all_devices:
            result = (self.has_battery,
                      self.has_boiler,
                      self.has_chp,
                      self.has_compression_chiller,
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

            if compression_chiller:
                result += (self.has_compression_chiller,)

            if electrical_heater:
                result += (self.has_electrical_heater,)

            if heatpump:
                result += (self.has_heatpump,)

            if inverter_acdc:
                result += (self.has_inverter_acdc,)

            if inverter_dcac:
                result += (self.has_inverter_dcac,)

            if pv:
                result += (self.has_pv,)
                
            if tes:
                result += (self.has_tes,)
        
        return result
