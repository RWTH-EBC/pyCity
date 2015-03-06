# -*- coding: utf-8 -*-
"""
Created on Mon Feb 09 12:26:24 2015

@author: tsz
"""

#import classes.Battery
#import classes.Boiler
#import classes.CHP
#import classes.ElectricalHeater
#import classes.Inverter
#import classes.PV
#import classes.ThermalEnergyStorage

import numpy as np

class BES(object):
    """
    Building Energy System (BES) is able to contain the following devices:
        Battery, Boiler, Combined Heat and Power (CHP) unit, Electrical heater, 
        Heatpump, Inverter (AC/DC and DC/AC), Photovoltaics (PV) and 
        Thermal Energy Storage (TES) unit
    """
    
    def __init__(self, environment):
        """
        Workflow
        --------
        1 : Create an empty building energy system (BES) that only contains the 
            environment pointer
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
        
    def addDevice(self, objectInstance):
        """
        Add a device object
        
        Example
        -------
        >>> myChp = CHP(...)
        >>> myBes = BES(...)
        >>> myBes.addDevice(myChp)
        """
        if objectInstance._kind == "battery":
            self.battery = objectInstance
            self.hasBattery = True
        
        elif objectInstance._kind == "boiler":
            self.boiler = objectInstance
            self.hasBoiler = True
        
        elif objectInstance._kind == "chp":
            self.chp = objectInstance
            self.hasChp = True
        
        elif objectInstance._kind == "electricalheater":
            self.electricalHeater = objectInstance
            self.hasElectricalHeater = True
        
        elif objectInstance._kind == "heatpump":
            self.heatpump = objectInstance
            self.hasHeatpump = True
        
        elif objectInstance._kind == "inverter":
            if objectInstance.getInputAC():
                self.inverterAcdc = objectInstance
                self.hasInverterAcdc = True
            else:
                self.inverterDcac = objectInstance
                self.hasInverterDcac = True
        
        elif objectInstance._kind == "pv":
            self.pv = objectInstance
            self.hasPv = True
            
        elif objectInstance._kind == "tes":
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
    
    def getDevices(self, allDevices=True, battery=False, boiler=False, chp=False, electricalHeater=False, heatpump=False, inverterAcdc=False, inverterDcac=False, pv=False, tes=False):
        """
        Get pointers to the installed devices (in alphabetical order, starting with "battery")
        
        Parameters
        ----------
        allDevices : boolean, optional
            If true: Return all installed devices
            If false: Only return the specified devices
        battery : boolean, optional
            Return a pointer to the battery?
        boiler : boolean, optional
            Return a pointer to the boiler?
        chp : boolean, optional
            Return a pointer to the chp unit?
        electricalHeater : boolean, optional
            Return a pointer to the electrical heater?
        heatpump : boolean, optional
            Return a pointer to the heat pump?
        inverterAcdc : boolean, optional
            Return a pointer to the AC-DC inverter?
        inverterDcac : boolean, optional
            Return a pointer to the DC-AC inverter?
        pv : boolean, optional
            Return a pointer to the PV modules?
        tes : boolean, optional
            Return a pointer to the thermal energy storage?
        """
        
        result = ()
        if allDevices:
            battery = True
            boiler = True
            chp = True
            electricalHeater = True
            heatpump = True
            inverterAcdc = True
            inverterDcac = True
            pv = True
            tes = True

        if battery:
            result += (self.battery,)
            
        if boiler:
            result += (self.boiler,)

        if chp:
            result += (self.chp,)

        if electricalHeater:
            result += (self.electricalHeater,)

        if heatpump:
            result += (self.heatpump,)

        if inverterAcdc:
            result += (self.inverterAcdc,)

        if inverterDcac:
            result += (self.inverterDcac,)

        if pv:
            result += (self.pv,)
        
        if tes:
            result += (self.tes,)
        
        return result
        
    def getHasDevices(self, allDevices=True, battery=False, boiler=False, chp=False, electricalHeater=False, heatpump=False, inverterAcdc=False, inverterDcac=False, pv=False, tes=False):
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
            result = (self.hasBattery, self.hasBoiler, self.hasChp, self.hasElectricalHeater, self.hasHeatpump, self.hasInverterAcdc, self.hasInverterDcac, self.hasPv, self.hasTes)

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
        
    def getBatteryInit(self):
        """ 
        Return the battery's initial SOC. If there is not battery installed, 
        return 0 
        """
        if self.hasBattery:
            return self.battery.getSocInit()
        else:
            return 0
    
    def getBatteryNominals(self):
        """ 
        Return the battery's nominal values as a tuple. 
        
        Order: Capacity, rate of self-discharge, efficiency at charging
        efficiency at discharging.
        
        If there is no battery installed, return four zeros.
        """
        if self.hasBattery:
            capacity      = self.battery.getCapacity()
            selfDischarge = self.battery.getSelfDischarge()
            etaCharge     = self.battery.getEtaCharge()
            etaDischarge  = self.battery.getEtaDischarge()
            
            return (capacity, selfDischarge, etaCharge, etaDischarge)
        else:
            return (0, 0, 0, 0)
    
    def getBoilerNominals(self):
        """
        Return the boiler's nominal values as a tuple. 
        
        Order: Thermal efficiency, nominal heat output, maximum flow 
        temperature and lower activation limit.
        
        If there is no boiler installed, return four zeros.
        """
        if self.hasBoiler:
            eta                  = self.boiler.getEta()
            qNominal             = self.boiler.getQNominal()
            tMax                 = self.boiler.getTMax()
            lowerActivationLimit = self.boiler.getLowerActivationLimit()
            
            return (eta, qNominal, tMax, lowerActivationLimit)
        else:
            return (0, 0, 0, 0)
            
    def getChpNominals(self):
        """
        Return the CHP unit's nominal values as a tuple. 
        
        Order: Overall efficiency, power to heat ratio, nominal electricity 
        output, nominal heat output, maximum flow temperature and lower 
        activation limit.
        
        If there is no CHP unit installed, return six zeros.
        """
        if self.hasChp:
            omega                = self.chp.getOmega()
            sigma                = self.chp.getSigma()
            qNominal             = self.chp.getQNominal()
            pNominal             = self.chp.getPNominal()
            tMax                 = self.chp.getTMax()
            lowerActivationLimit = self.chp.getLowerActivationLimit()
            
            return (omega, sigma, pNominal, qNominal, tMax, lowerActivationLimit)
        else:
            return (0, 0, 0, 0, 0, 0)
            
    def getElectricalHeaterNominals(self):
        """
        Return the electrical heater's nominal values as a tuple. 
        
        Order: Electrical efficiency, nominal electricity consumption, nominal 
        heat output, maximum flow temperature and lower activation limit.
        
        If there is no electrical heater installed, return five zeros.
        """
        if self.hasElectricalHeater:
            eta                  = self.electricalHeater.getEta()
            pNominal             = self.electricalHeater.getPNominal()
            qNominal             = self.electricalHeater.getQNominal()
            tMax                 = self.electricalHeater.getTMax()
            lowerActivationLimit = self.electricalHeater.getLowerActivationLimit()
            
            return (eta, pNominal, qNominal, tMax, lowerActivationLimit)
        else:
            return (0, 0, 0, 0, 0)
    
    def getHeatpumpNominals(self, tFlow):
        """
        Return the nominal electricity consumption, heat output and lower 
        activation limit.
        
        Parameters
        ----------
        tFlow : Array_like
            Required flow temperature
            
        Returns
        -------
        pNominal : Array_like
            Nominal electricity consumption at the given flow temperatures and 
            the forecast of the current ambient temperature
        qNominal : Array_like
            Nominal heat output at the given flow temperatures and the 
            forecast of the current ambient temperature
        lowerActivationLimit : float (0 <= lowerActivationLimit <= 1)
            Define the lower activation limit. For example, heat pumps are 
            typically able to operate between 50 % part load and rated load. 
            In this case, lowerActivationLimit would be 0.5
            Two special cases: 
            Linear behavior: lowerActivationLimit = 0
            Two-point controlled: lowerActivationLimit = 1
        """
        if self.hasHeatpump:
            return self.heatpump.getNominals(tFlow)
        else:
            return (0, 0, 0)
            
    def getInverterNominals(self, AcToDc=True):
        """
        Return the inverter's nominal values as a tuple. 
        
        If ``AcToDc == True``, the nominals of the AC/DC inverter are returned. 
        Otherwise, the nominals of the DC/AC inverter are returned.
        
        Order: Electrical efficiency, nominal input power.
        
        If there is no inverter installed, return two zeros.
        """
        if self.hasInverterAcdc and AcToDc:
            eta      = self.inverterAcdc.getEta()
            pNominal = self.inverterAcdc.getPNominal()
            
            return (eta, pNominal)
        elif self.hasInverterDcac and (not AcToDc):
            eta      = self.inverterDcac.getEta()
            pNominal = self.inverterDcac.getPNominal()
            
            return (eta, pNominal)
        else:
            return (0, 0)
            
    def getPvProduction(self):
        """
        Return the PV modules' electricity generation for the upcoming 
        optimization period.
        
        Returns array with ``timer.timestepsHorizon`` entries (zeros if the 
        BES does not contain PV modules)
        """
        if self.hasPv:
            return self.pv.getPower()
        else:
            return np.zeros(self.environment.timer.timestepsHorizon)
            
    def getTesInit(self):
        """ 
        Return the TES unit's initial temperatur. If there is not TES unit 
        installed, return 0 
        """
        if self.hasTes:
            return self.tes.getTInit()
        else:
            return 0
    
    def getTesNominals(self):
        """ 
        Return the TES unit's nominal values as a tuple. 
        
        Order: capacity, maximum temperature, surroundings' temperature, 
        U*A (loss factor)
        
        If there is no TES unit installed, return four zeros.
        """
        if self.hasTes:
            return self.tes.getStorageParameters()
        else:
            return (0, 0, 0, 0)
            
    def setBatteryResults(self, soc, pIncrease, pDecrease):
        """
        Save the results of the battery scheduling
        
        Parameters
        ----------
        soc : Array-like
            State of charge
        pIncrease : Array-like
            Charging power in Watt
        pDecrease : Array-like
            Discharging power in Watt
        """
        if self.hasBattery:
            self.battery.setSoc(soc)
            self.battery.setPCharge(pIncrease)
            self.battery.setPDischarge(pDecrease)

    def setBoilerResults(self, schedule, heatOutput):
        """
        Save the results of the scheduling
        
        Parameters
        ----------
        schedule : Array-like
            Scheduling results (binary values)
        heatOutput : Array-like
            Heat output in Watt
        """
        if self.hasBoiler:
            self.boiler.setSchedule(schedule)
            self.boiler.setQOutput(heatOutput)
    
    def setChpResults(self, schedule, electricityOutput, heatOutput):
        """
        Save the results of the scheduling
        
        Parameters
        ----------
        schedule : Array-like
            Scheduling results (binary values)
        electricityOutput : Array-like
            Electricity output in Watt
        heatOutput : Array-like
            Heat output in Watt
        """
        if self.hasChp:
            self.chp.setSchedule(schedule)
            self.chp.setPOutput(electricityOutput)
            self.chp.setQOutput(heatOutput)
    
    def setElectricalHeaterResults(self, schedule, electricityConsumption):
        """
        Save the results of the scheduling
        
        Parameters
        ----------
        schedule : Array-like
            Scheduling results (binary values)
        electricityConsumption : Array-like
            Electricity consumption in Watt
        """
        if self.hasElectricalHeater:
            self.electricalHeater.setSchedule(schedule)
            self.electricalHeater.setPConsumption(electricityConsumption)
    
    def setHeatpumpResults(self):
        pass
    
    def setInverterResults(self, pInverter, AcToDc=True):
        """
        Save the results of the scheduling
        
        Parameters
        ----------
        pInverter : Array-like
            AC/DC inverter: Input power
            DC/AC inverter: Output power
        AcToDc : Boolean, optional
            ``True``: AC/DC inverter
            ``False``: DC/AC inverter
        """
        if AcToDc:
            eta = self.inverterAcdc.getEta()
            self.inverterAcdc.setPInput(pInverter)
            self.inverterAcdc.setPOutput(pInverter * eta)
        else:
            eta = self.inverterDcac.getEta()
            self.inverterDcac.setPOutput(pInverter)
            self.inverterDcac.setPInput(pInverter / eta)
    
    def setTesResults(self, tSto):
        """
        Save the results of the scheduling
        
        Parameters
        ----------
        tSto : Array-like
            Storage temperature in °C
        """
        if self.hasTes:
            self.tes.setTSto(tSto)