# -*- coding: utf-8 -*-
"""
Created on Sun Feb 15 17:01:21 2015

@author: T_ohne_admin
"""

from __future__ import division

import numpy as np

class Building(object):
    """
    Implementation of a building that consists of a single Building Energy 
    System (BES), one controller and multiple apartments
    """
    
    def __init__(self, environment):
        """
        Workflow
        --------
        1 : Create an empty building that only contains the environment 
            pointer
        2 : Add entities such as controller or BES, by invoking the addEntity 
            or addMultipleEntities methods.
        
        Parameter
        ---------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        """
        self._kind = "building"
        
        self.environment = environment
        
        self.apartments = []
        self.bes        = []        
        self.controller = []
        
        self.hasApartments = False
        self.hasBes        = False
        self.hasController = False
    
    def addEntity(self, entity):
        """ 
        Add an entity (apartment, BES or controller) to the building 
        
        Example
        -------
        >>> myBes = BES(...)
        >>> myBuilding = Building(...)
        >>> myBuilding.addEntity(myBes)
        """
        if entity._kind == "apartment":
            self.apartments.append(entity)
            self.hasApartments = True
        
        elif entity._kind == "bes":
            self.bes = entity
            self.hasBes = True

        elif entity._kind == "controller":
            self.controller = entity
            self.hasController = True

    def addMultipleEntities(self, entities):
        """
        Add multiple entities to the existing building
        
        Parameter
        ---------
        entities: List-like
            List (or tuple) of entities that are added to the building
            
        Example
        -------
        >>> myBes = BES(...)
        >>> myController = Controller(...)
        >>> myBuilding = Building(...)
        >>> myBuilding.addEntity([myBes, myController])
        """
        for entity in entities:
            self.addEntity(entity)    
    
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
        return self.bes.getHasDevices(allDevices, battery, boiler, chp, electricalHeater, heatpump, inverterAcdc, inverterDcac, pv, tes)
    
    def getHasApartments(self):
        """ Return if the building has at least one apartment (True) """
        return self.hasApartments

    def getApartment(self, number=-1):
        """ 
        Get an apartment object

        Parameter
        ---------
        number : integer, optional
            Which apartment shall be returned?
            If number=-1, the list of all apartments is returned
        """
        if self.hasApartments:
            if number == -1:
                return self.apartments
            else:
                return self.apartments[number]
        else:
             return []
        
    def getHasBes(self):
        """ Return True if a BES has been added to the building """
        return self.hasBes
        
    def getBes(self):
        """ Return the building's BES """
        return self.bes
        
    def getHasController(self):
        """ Return True if a controller has been added to the building """
        return self.hasController
    
    def getController(self):
        """ Return the building's controller """
        return self.controller
    
    def getDemands(self):
        """
        Get the entire electrical and thermal demand of all apartments in this 
        building.
        
        Order: (resultElectrical, resultThermal)
        """
        return self.controller.getDemands(self.apartments)
        
    def getFlowTemperature(self):
        """ Get the required flow temperature of this building. """
        return self.controller.getFlowTemperature(self.apartments)
        
    def getBatteryInit(self):
        """ 
        Return the battery's initial SOC. If there is not battery installed, 
        return 0 
        """
        return self.bes.getBatteryInit()
    
    def getBatteryNominals(self):
        """ 
        Return the battery's nominal values as a tuple. 
        
        Order: Capacity, rate of self-discharge, efficiency at charging
        efficiency at discharging.
        
        If there is no battery installed, return four zeros.
        """
        return self.bes.getBatteryNominals()
    
    def getBoilerNominals(self):
        """
        Return the boiler's nominal values as a tuple. 
        
        Order: Thermal efficiency, nominal heat output, maximum flow 
        temperature and lower activation limit.
        
        If there is no boiler installed, return four zeros.
        """
        return self.bes.getBoilerNominals()
            
    def getChpNominals(self):
        """
        Return the CHP unit's nominal values as a tuple. 
        
        Order: Overall efficiency, power to heat ratio, nominal electricity 
        output, nominal heat output, maximum flow temperature and lower 
        activation limit.
        
        If there is no CHP unit installed, return six zeros.
        """
        return self.bes.getChpNominals()
            
    def getElectricalHeaterNominals(self):
        """
        Return the electrical heater's nominal values as a tuple. 
        
        Order: Electrical efficiency, nominal electricity consumption, nominal 
        heat output, maximum flow temperature and lower activation limit.
        
        If there is no electrical heater installed, return five zeros.
        """
        return self.bes.getElectricalHeaterNominals()
        
    def getHeatpumpNominals(self):
        """
        Return the nominal electricity consumption, heat output and lower 
        activation limit.
            
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
        tFlow = self.getFlowTemperature()
        return self.bes.getHeatpumpNominals(tFlow)
            
    def getInverterNominals(self, AcToDc=True):
        """
        Return the inverter's nominal values as a tuple. 
        
        If ``AcToDc == True``, the nominals of the AC/DC inverter are returned. 
        Otherwise, the nominals of the DC/AC inverter are returned.
        
        Order: Electrical efficiency, nominal input power.
        
        If there is no inverter installed, return two zeros.
        """
        return self.bes.getInverterNominals()
            
    def getPvProduction(self):
        """
        Return the PV modules' electricity generation for the upcoming 
        optimization period.
        
        Returns array with ``timer.timestepsHorizon`` entries (zeros if the 
        BES does not contain PV modules)
        """
        return self.bes.getPvProduction()
            
    def getTesInit(self):
        """ 
        Return the TES unit's initial temperatur. If there is not TES unit 
        installed, return 0 
        """
        return self.bes.getTesInit()
    
    def getTesNominals(self):
        """ 
        Return the TES unit's nominal values as a tuple. 
        
        Order: capacity, maximum temperature, surroundings' temperature, 
        U*A (loss factor)
        
        If there is no TES unit installed, return four zeros.
        """
        return self.bes.getTesNominals()

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
        self.bes.setBatteryResults(soc, pIncrease, pDecrease)
        
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
        self.bes.setBoilerResults(schedule, heatOutput)

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
        self.bes.setChpResults(schedule, electricityOutput, heatOutput)
    
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
        self.bes.setElectricalHeaterResults(schedule, electricityConsumption)
    
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
        self.bes.setInverterResults(pInverter, AcToDc)

    def setTesResults(self, tSto):
        """
        Save the results of the scheduling
        
        Parameters
        ----------
        tSto : Array-like
            Storage temperature in °C
        """
        self.bes.setTesResults(tSto)
        
    def getPriceInformation(self):
        """
        Return all market information.
        
        Order: Electricity costs, gas costs, CHP revenue, feed-in remuneration
        """
        return self.environment.getPriceInformation()
    
    def getElectricalApplianceNominals(self, dishwasher=True):
        """
        Return the nominals of an electrical appliance (dishwasher or 
        washing machine)

        Parameter
        ---------
        dishwasher : Boolean, optional
            `True` if the dishwasher's values shall be returned.
            `False` if the data of the washing machine shall be returned.
        
        Returns
        -------
        result : Array_like
            One dimensional structure (one entry per house)
        First entry : Boolean
            Is the requested device installed in the current apartment?
        Second entry : Float
            Maximum capacity
        Third entry : Float
            activation border (socMayrun)
        Fourth entry : Array-like
            charging curve (gains)
        Fifth entry : Boolean
            connection to TES unit (ThermalConnection)
        Sixth entry : Array-like
            electrical load curve
        Seventh entry : Array-like
            thermal load curve
        """
        result = []
        
        # Go through all apartments
        for apartment in self.apartments:
            # Get the device's nominal values
            nominals = apartment.getApplianceNominals(dishwasher=dishwasher)
            
            # Check if the device is installed at all
            if apartment.getHasAppliance(dishwasher=dishwasher):
                hasAppliance = False
            else:
                hasAppliance = True
            
            # Append current result to `result`
            result.append((hasAppliance,) + nominals)
        
        # Return `result`
        return result
        
        
    def getElectricalApplianceInitialStates(self, dishwasher=True):
        """
        Return the initial values of all electrical appliances of one type
        (dishwasher or washing machine)

        Parameter
        ---------
        dishwasher : Boolean, optional
            `True` if the dishwasher's initial values shall be returned.
            `False` if the values of the washing machine shall be returned.
        
        Returns
        -------
        hasDevice : Array_like (boolean)
            Is the requested device installed in the current apartment?
        soc: Array_like (float)
            Initial state of charge
        activityLevel : Array_like (binary)
            Initial activity level
        startingEvents : list of arrays (binaries)
            Previous starting event indicators
            The first index indicates the apartment, the second the starting 
            procedure.
            As some of the devices may have different cycles (one hour, two 
            hours), the numpy array seems not to be suitable.
        """
        hasDevice = []
        soc = []
        activityLevel = []
        startingEvents = []
        
        # Go through all apartments
        for apartment in self.apartments:
            # Get the device's nominal values
            initialValues = apartment.getApplianceInitialState(dishwasher=dishwasher)
            
            # Check if the device is installed at all
            if apartment.getHasAppliance(dishwasher=dishwasher):
                hasDevice.append(True)
                soc.append(initialValues[0])
                activityLevel.append(initialValues[1])
                startingEvents.append(initialValues[2])
            else:
                hasDevice.append(False)
                soc.append(0)
                activityLevel.append(0)
                startingEvents.append([0])
            
        # Transform to array of possible
        # startingEvents cannot be transformed, as the cycle length of each 
        # appliance is not necessarily the same.
        hasDevice     = np.array(hasDevice)
        soc           = np.array(soc)
        activityLevel = np.array(activityLevel)
        # Return `result`
        return (hasDevice, soc, activityLevel, startingEvents)
        
    def getHasElectricalAppliance(self, allDevices=True, dishwasher=False, washingmachine=True):
        """
        Return the distribution of electrical devices of all apartments.
        
        Parameters
        ----------
        allDevices : Boolean
            Return information on all devices
        dishwasher : Boolean
            Return information on dishwashers
        washingmachine : Boolean
            Return information on washing machines
            
        Returns: Numpy array
            First column: Dishwashers (if ``allDevices==True or 
            dishwasher==True``).
            Second column: Washing machines (if ``allDevices==True or 
            washingmachine==True``).
        """
        result = []
        
        if allDevices:
            dishwasher = True
            washingmachine = True
        
        for apartment in self.apartments:
            temporaryResult = ()
            if dishwasher:
                temporaryResult += (apartment.getHasAppliance(dishwasher=True),)
            
            if washingmachine:
                temporaryResult += (apartment.getHasAppliance(dishwasher=False),)
            
            result.append(temporaryResult)
        
        return np.array(result)
    
    def setElectricalApplianceResults(self, soc, power, heat, schedule, dishwasher=True):
        """
        Save the scheduling results of all electrical appliances of the same 
        type (dishwashers or washing machines).
        
        Parameters
        ----------
        soc : Array_like
            State of charge
        power : Array_like
            Electrical power consumption
        heat : Array_like
            Heat consumption
        schedule : Array_like
            Binary scheduling results
        """
        i = 0
        for apartment in self.apartments:
            # Extract relevant results
            tempSoc      = soc[i,:]
            tempPower    = power[i,:]
            tempHeat     = heat[i,:]
            tempSchedule = schedule[i,:]
            # Save results
            apartment.setElectricalApplianceResults(tempSoc, tempPower, tempHeat, tempSchedule, dishwasher=dishwasher)
            
            # Increase counter
            i += 1