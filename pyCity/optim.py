# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 09:39:10 2015

@author: tsz
"""

from __future__ import division
import numpy as np

from gurobipy import *

def optimize(building, environment):
    """
    Simple building optimization.
    Available devices: TES and boiler
    Apartments: 1, without dishwasher and washing machine
    """

    (hasBattery, hasBoiler, hasChp, hasElectricalHeater, hasHeatpump, hasInverterAcdc, hasInverterDcac, hasPv, hasTes) = building.getHasDevices(allDevices=True)
    electricalDevices = building.getHasElectricalAppliance(allDevices=True)
    hasDishwashers     = electricalDevices[:,0]
    hasWashingmachines = electricalDevices[:,1]
    
    # BES devices
    if hasBattery:
        batterySocInit = building.getBatteryInit()
        (batteryCapacity, batterySelfDischarge, batteryEtaCharge, batteryEtaDischarge) = building.getBatteryNominals()
    if hasBoiler:
        (boilerEta, boilerQNominal, boilerTMax, boilerLowerActivationLimit) = building.getBoilerNominals()
    if hasChp:
        (chpOmega, chpSigma, chpPNominal, chpQNominal, chpTMax, chpLowerActivationLimit) = building.getChpNominals()
    if hasElectricalHeater:
        (elHeaterEta, elHeaterPNominal, elHeaterQNominal, elHeaterTMax, elHeaterLowerActivationLimit) = building.getElectricalHeaterNominals()
    if hasHeatpump:
        pass
    if hasInverterAcdc:
        (inverterAcdcEta, inverterAcdcPNominal) = building.getInverterNominals(AcToDc=True)
    if hasInverterDcac:
        (inverterDcacEta, inverterDcacPNominal) = building.getInverterNominals(AcToDc=False)
    if hasPv:
        pvPower = building.getPvProduction()
    if hasTes:
        tInit = building.getTesInit()
        (tesCapacity, tesTMax, tesTSurroundings, tesKLosses) = building.getTesNominals()

    # Electrical appliances:
    if np.max(hasDishwashers):
        initialValuesDishwashers = building.getElectricalApplianceInitialStates(dishwasher=True)
        dishwashersInitialSoc   = initialValuesDishwashers[:,1]
        dishwashersInitialLevel = initialValuesDishwashers[:,2]
        nominalsDishwashers = building.getElectricalApplianceNominals(dishwasher=True)
        dishwashersCapacity          = [nominalsDishwashers[k][1] for k in range(len(nominalsDishwashers))]
        dishwashersSocMayrun         = [nominalsDishwashers[k][2] for k in range(len(nominalsDishwashers))]
        dishwashersGains             = [nominalsDishwashers[k][3] for k in range(len(nominalsDishwashers))]
#        dishwashersThermalConnection = [nominalsDishwashers[k][4] for k in range(len(nominalsDishwashers))]
        dishwashersLoadElectrical    = [nominalsDishwashers[k][5] for k in range(len(nominalsDishwashers))]
        dishwashersLoadThermal       = [nominalsDishwashers[k][6] for k in range(len(nominalsDishwashers))]
    if np.max(hasWashingmachines):
        initialValuesWashingmachines = building.getElectricalApplianceInitialStates(dishwasher=False)
        washingmachinesInitialSoc   = initialValuesWashingmachines[:,1]
        washingmachinesInitialLevel = initialValuesWashingmachines[:,2]
        nominalsWashingmachines = building.getElectricalApplianceNominals(dishwasher=False)
        washingmachinesCapacity          = [nominalsWashingmachines[k][1] for k in range(len(nominalsWashingmachines))]
        washingmachinesSocMayrun         = [nominalsWashingmachines[k][2] for k in range(len(nominalsWashingmachines))]
        washingmachinesGains             = [nominalsWashingmachines[k][3] for k in range(len(nominalsWashingmachines))]
#        washingmachinesThermalConnection = [nominalsWashingmachines[k][4] for k in range(len(nominalsWashingmachines))]
        washingmachinesLoadElectrical    = [nominalsWashingmachines[k][5] for k in range(len(nominalsWashingmachines))]
        washingmachinesLoadThermal       = [nominalsWashingmachines[k][6] for k in range(len(nominalsWashingmachines))]

    (cEl, cGas, revChp, revEl) = environment.getPriceInformation()
    
    timesteps = environment.getTimestepsHorizon()
    timestepsUsedHorizon = environment.getTimestepsUsedHorizon()
    dt = environment.getTimeDiscretization()
    
    tFlowMin = building.getFlowTemperature()
    (demandElectrical, demandThermal) = building.getDemands()
    
    cW = 4180 # Heat capacity of water in J/(kg K)
    
    
    # Gurobi model
    try:
        # Create a new model
        model = Model("BES_optimization")
    
        # Create variables
        """
        Nomenclature: 
            soc -> state of charge (without unit)
            p   -> electrical power in W
            q   -> thermal power in W
            x   -> status variable (on/off - binary)
            y   -> starting procedure (yes/no - binary)
            z   -> shutdown procedure (yes/no - binary)
        """
        # Battery
        socBattery = {}
        pIncrease = {} # Output of the AC/DC inverter
        pDecrease = {} # Input of the DC/AC inverter
        
        # Boiler
        qBoiler = {}
        xBoiler = {}
        
        # CHP
        qChp = {}
        pChp = {}
        xChp = {}
        
        # Dishwashers
        socDishwasher = {}
        xDishwasher   = {}
        yDishwasher   = {}
        zDishwasher   = {}
        lDishwasher   = {} # Linearization of y * soc
        pDishwasher   = {}
        qDishwasher   = {}
        # Dishwashers - all installed devices
        pDishwasherTotal = {}
        qDishwasherTotal = {}
        
        # Electrical heater
        xElHeater = {}
        pElHeater = {}
        qElHeater = {}
        
        # Heat pump
        xHeatpump = {}
        pHeatpump = {}
        qHeatpump = {}
        
        # Inverter - AC to DC
        pInverterAcdc = {} # Input -> electrical sink of the building
        
        # Inverter - DC to AC
        pInverterDcac = {} # Output -> electrical gain of the building
        
        # Thermal energy storage (TES)
        tTes = {}
        qTesLosses = {}
        qTesCharge = {}
        qTesDischarge = {}
        
        # Wasching machines
        socWashingmachine = {}
        xWashingmachine   = {}
        yWashingmachine   = {}
        zWashingmachine   = {}
        lWashingmachine   = {} # Linearization of y * soc
        pWashingmachine   = {}
        qWashingmachine   = {}
        # Washing machines - all installed devices
        pWashingmachineTotal = {}
        qWashingmachineTotal = {}
        
        # Interaction with environment
        pSurplus = {}
        pAdditional = {}
        
        # Fill the empty dictionaries if the device is installed
        for t in xrange(timesteps):
            # Every house interacts with its environment:
            pSurplus[t]    = model.addVar(vtype=GRB.CONTINUOUS, name="P_surplus_"+str(t),    lb=0)
            pAdditional[t] = model.addVar(vtype=GRB.CONTINUOUS, name="P_additional_"+str(t), lb=0)

            if hasTes:
                tTes[t]          = model.addVar(vtype=GRB.CONTINUOUS, name="T_TES_"+str(t),           lb=tFlowMin[t], ub=tesTMax)
                qTesLosses[t]    = model.addVar(vtype=GRB.CONTINUOUS, name="Q_TES_losses_"+str(t),    lb=0)
                qTesCharge[t]    = model.addVar(vtype=GRB.CONTINUOUS, name="Q_TES_charge_"+str(t),    lb=0)
                qTesDischarge[t] = model.addVar(vtype=GRB.CONTINUOUS, name="Q_TES_discharge_"+str(t), lb=0)
            
            if hasBattery:
                socBattery[t] = model.addVar(vtype=GRB.CONTINUOUS, name="SOC_Battery_"+str(t), lb=0, ub=batteryCapacity)
                pIncrease[t]  = model.addVar(vtype=GRB.CONTINUOUS, name="P_increase_"+str(t),  lb=0, ub=inverterAcdcPNominal * inverterAcdcEta)
                pDecrease[t]  = model.addVar(vtype=GRB.CONTINUOUS, name="P_decrease_"+str(t),  lb=0, ub=inverterDcacPNominal)
            
            if hasInverterAcdc:
                pInverterAcdc[t] = model.addVar(vtype=GRB.CONTINUOUS, name="P_inv_ac_dc_"+str(t), lb=0, ub=inverterAcdcPNominal)

            if hasInverterDcac:
                pInverterDcac[t] = model.addVar(vtype=GRB.CONTINUOUS, name="P_inv_dc_ac_"+str(t), lb=0, ub=inverterDcacPNominal * inverterDcacEta)

            if hasBoiler:
                qBoiler[t] = model.addVar(vtype=GRB.CONTINUOUS, name="Q_Boiler_"+str(t), lb=0, ub=boilerQNominal)
                xBoiler[t] = model.addVar(vtype=GRB.BINARY,     name="X_Boiler_"+str(t))

            if hasChp:
                qChp[t] = model.addVar(vtype=GRB.CONTINUOUS, name="Q_CHP_"+str(t), lb=0, ub=chpQNominal)
                pChp[t] = model.addVar(vtype=GRB.CONTINUOUS, name="P_CHP_"+str(t), lb=0, ub=chpPNominal)
                xChp[t] = model.addVar(vtype=GRB.BINARY,     name="X_CHP_"+str(t))
                
            if hasElectricalHeater:
                xElHeater[t] = model.addVar(vtype=GRB.BINARY,     name="X_El_Heater_"+str(t))
                pElHeater[t] = model.addVar(vtype=GRB.CONTINUOUS, name="P_El_Heater_"+str(t), lb=0, ub=elHeaterPNominal)
                qElHeater[t] = model.addVar(vtype=GRB.CONTINUOUS, name="Q_El_Heater_"+str(t), lb=0, ub=elHeaterQNominal)
            
            if hasHeatpump:
                xHeatpump[t] = model.addVar(vtype=GRB.BINARY,     name="X_Heatpump_"+str(t))
                pHeatpump[t] = model.addVar(vtype=GRB.CONTINUOUS, name="P_Heatpump_"+str(t), lb=0, ub=bes.heatpump.p_nominal[t])
                qHeatpump[t] = model.addVar(vtype=GRB.CONTINUOUS, name="Q_Heatpump_"+str(t), lb=0, ub=bes.heatpump.q_nominal[t])
                
            if np.max(hasDishwashers):
                for k in range(len(hasDishwashers)):
                    socDishwasher[k,t] = model.addVar(vtype=GRB.CONTINUOUS, name="SOC_Dishwasher_"+str(t)+"_"+str(k), lb=0, ub=dishwashersCapacity[k] + np.max(dishwashersGains[k]))
                    pDishwasher[k,t]   = model.addVar(vtype=GRB.CONTINUOUS, name="P_Dishwasher_"+str(t)+"_"+str(k),   lb=0, ub=np.max(dishwashersLoadElectrical[k]))
                    qDishwasher[k,t]   = model.addVar(vtype=GRB.CONTINUOUS, name="Q_Dishwasher_"+str(t)+"_"+str(k),   lb=0, ub=np.max(dishwashersLoadThermal[k]))
                    lDishwasher[k,t]   = model.addVar(vtype=GRB.CONTINUOUS, name="L_Dishwasher_"+str(t)+"_"+str(k),   lb=0)
                    xDishwasher[k,t]   = model.addVar(vtype=GRB.BINARY,     name="X_Dishwasher_"+str(t)+"_"+str(k))
                    yDishwasher[k,t]   = model.addVar(vtype=GRB.BINARY,     name="Y_Dishwasher_"+str(t)+"_"+str(k))
                    zDishwasher[k,t]   = model.addVar(vtype=GRB.BINARY,     name="Z_Dishwasher_"+str(t)+"_"+str(k))
                # Dishwasher - all installed devices
                pDishwasherTotal[t] = model.addVar(vtype=GRB.CONTINUOUS, name="P_Dishwasher_total_"+str(t), lb=0)
                qDishwasherTotal[t] = model.addVar(vtype=GRB.CONTINUOUS, name="Q_Dishwasher_total_"+str(t), lb=0)
                
            if np.max(hasWashingmachines):
                for k in range(len(hasWashingmachines)):
                    socWashingmachine[k,t] = model.addVar(vtype=GRB.CONTINUOUS, name="SOC_Washingmachine_"+str(t)+"_"+str(k), lb=0, ub=washingmachinesCapacity[k] + np.max(washingmachinesGains[k]))
                    pWashingmachine[k,t]   = model.addVar(vtype=GRB.CONTINUOUS, name="P_Washingmachine_"+str(t)+"_"+str(k),   lb=0, ub=np.max(washingmachinesLoadElectrical[k][t]))
                    qWashingmachine[k,t]   = model.addVar(vtype=GRB.CONTINUOUS, name="Q_Washingmachine_"+str(t)+"_"+str(k),   lb=0, ub=np.max(washingmachinesLoadThermal[k][t]))
                    lWashingmachine[k,t]   = model.addVar(vtype=GRB.CONTINUOUS, name="L_Washingmachine_"+str(t)+"_"+str(k),   lb=0)
                    xWashingmachine[k,t]   = model.addVar(vtype=GRB.BINARY,     name="X_Washingmachine_"+str(t)+"_"+str(k))
                    yWashingmachine[k,t]   = model.addVar(vtype=GRB.BINARY,     name="Y_Washingmachine_"+str(t)+"_"+str(k))
                    zWashingmachine[k,t]   = model.addVar(vtype=GRB.BINARY,     name="Z_Washingmachine_"+str(t)+"_"+str(k))
                # Dishwasher - all installed devices
                pWashingmachineTotal[t] = model.addVar(vtype=GRB.CONTINUOUS, name="P_Washingmachine_total_"+str(t), lb=0)
                qWashingmachineTotal[t] = model.addVar(vtype=GRB.CONTINUOUS, name="Q_Washingmachine_total_"+str(t), lb=0)

        
        # Integrate new variables into the model
        model.update()
        
        # Set objective function
        # Costs from boiler usage
        if hasBoiler:
            gasBoiler = quicksum(1/boilerEta * qBoiler[t] * cGas * dt for t in range(timesteps))
        else:
            gasBoiler = 0
            
        # Costs from CHP usage
        if hasChp:
            revenueChp = quicksum(pChp[t] * revChp * dt for t in range(timesteps))
            gasChp = quicksum(1/chpOmega * (pChp[t] + qChp[t]) * cGas * dt for t in range(timesteps))
        else:
            revenueChp = 0
            gasChp = 0
        
        # Grid interaction
        costsElectricityImport   = quicksum(pAdditional[t] * cEl * dt for t in range(timesteps))
        revenueElectricityExport = quicksum(pSurplus[t] * revEl * dt for t in range(timesteps))
        
        # Objective function
        model.setObjective(gasBoiler - revenueChp + gasChp + costsElectricityImport - revenueElectricityExport, GRB.MINIMIZE)
        
        for t in xrange(timesteps):
            # Handle time step zero (necessary for storage-like equations)
            if t == 0:
                tTesPrevious = tInit
                if hasBattery:
                    socBatteryPrevious = batterySocInit
                if np.max(hasDishwashers):
                    socDishwasherPrevious = []
                    xDishwasherPrevious = []
                    lDishwasherPrevious = []
                    for k in range(len(hasDishwashers)):
                        socDishwasherPrevious.append(dishwashersInitialSoc[k])
                        xDishwasherPrevious.append(dishwashersInitialLevel[k])
                        lDishwasherPrevious.append(socDishwasherPrevious[k] * (1-yDishwasher[k,t]))
                if np.max(hasWashingmachines):
                    socWashingmachinePrevious = []
                    xWashingmachinePrevious = []
                    lWashingmachinePrevious = []
                    for k in range(len(hasWashingmachines)):
                        socWashingmachinePrevious.append(washingmachinesInitialSoc[k])
                        xWashingmachinePrevious.append(washingmachinesInitialLevel[k])
                        lWashingmachinePrevious.append(socWashingmachinePrevious[k] * (1-yWashingmachine[k,t]))
            else:
                tTesPrevious = tTes[t-1]
                if hasBattery:
                    socBatteryPrevious = socBattery[t-1]
                if np.max(hasDishwashers):
                    socDishwasherPrevious = []
                    xDishwasherPrevious = []
                    lDishwasherPrevious = []
                    for k in range(len(hasDishwashers)):
                        socDishwasherPrevious.append(socDishwasher[k,t-1])
                        xDishwasherPrevious.append(xDishwasher[k,t-1])
                        lDishwasherPrevious.append(socDishwasherPrevious[k] - lDishwasher[k,t-1])
                if np.max(hasWashingmachines):
                    socWashingmachinePrevious = []
                    xWashingmachinePrevious = []
                    lWashingmachinePrevious = []
                    for k in range(len(hasWashingmachines)):
                        socWashingmachinePrevious.append(socWashingmachine[k,t-1])
                        xWashingmachinePrevious.append(xWashingmachine[k,t-1])
                        lWashingmachinePrevious.append(socWashingmachinePrevious[k] - lWashingmachine[k,t])
            
            # Compute inputs and outputs of each device
            qStorageCharge = 0
            qStorageDischarge = demandThermal[t]
            pProduction = 0
            pConsumption = demandElectrical[t]
            
            if hasBattery:
                model.addConstr(pIncrease[t] == pInverterAcdc[t] * inverterAcdcEta)
                model.addConstr(pDecrease[t] * inverterDcacEta == pInverterDcac[t])
                model.addConstr(socBattery[t] == (1-batterySelfDischarge) * socBatteryPrevious + dt * (batteryEtaCharge * pIncrease[t] - 1/batteryEtaDischarge * pDecrease[t]))
                pProduction  += pInverterDcac[t]
                pConsumption += pInverterAcdc[t]

            if hasBoiler:
                model.addConstr(qBoiler[t] >= xBoiler[t] * boilerQNominal * boilerLowerActivationLimit)
                model.addConstr(qBoiler[t] <= xBoiler[t] * boilerQNominal)
                model.addConstr(tTes[t] <= boilerTMax + (1 - xBoiler[t]) * (tesTMax - boilerTMax))
                qStorageCharge += qBoiler[t]
                
            if hasChp:
                model.addConstr(qChp[t] >= xChp[t] * chpQNominal * chpLowerActivationLimit)
                model.addConstr(qChp[t] <= xChp[t] * chpQNominal)
                model.addConstr(pChp[t] == qChp[t] * chpSigma)
                model.addConstr(tTes[t] <= chpTMax+ (1 - xChp[t]) * (tesTMax - chpTMax))
                qStorageCharge += qChp[t]
                pProduction += pChp[t]
            
            if hasElectricalHeater:
                model.addConstr(qElHeater[t] >= xElHeater[t] * elHeaterQNominal * elHeaterLowerActivationLimit)
                model.addConstr(qElHeater[t] <= xElHeater[t] * elHeaterQNominal)
                model.addConstr(pElHeater[t] == 1/elHeaterEta * qElHeater[t])
                model.addConstr(tTes[t] <= elHeaterTMax + (1 - xElHeater[t]) * (tesTMax - elHeaterTMax))
                qStorageCharge += qElHeater[t]
                pConsumption   += pElHeater[t]
        
            if hasHeatpump:
                model.addConstr(qHeatpump[t] >= xHeatpump[t] * bes.heatpump.q_nominal * bes.heatpump.lower_activation_limit)
                model.addConstr(qHeatpump[t] <= xHeatpump[t] * bes.heatpump.q_nominal)
                model.addConstr(pHeatpump[t] == 1/bes.heatpump.cop[t] * qHeatpump[t])
                model.addConstr(tTes[t] <= heatpumpTMax + (1 - xHeatpump[t]) * (tesTMax - heatpumpTMax))
                qStorageCharge += qHeatpump[t]
                pConsumption   += pHeatpump[t]

            if hasPv:
                pProduction += pvPower[t]
                
            if np.max(hasDishwashers):
                for k in range(len(hasDishwashers)):
                    # Mode transitions
                    model.addConstr(xDishwasher[k,t] - xDishwasherPrevious[k] == yDishwasher[k,t] - zDishwasher[k,t])
                    model.addConstr(yDishwasher[k,t] + zDishwasher[k,t] <= 1)
                    # Electricity and heat consumption
                    if t >= len(dishwashersLoadElectrical[k]) - 1:
                        model.addConstr(pDishwasher[k,t] == quicksum(yDishwasher[k,t-tau] * dishwashersLoadElectrical[k][tau] for tau in range(len(dishwashersLoadThermal[k]))))
                        model.addConstr(qDishwasher[k,t] == quicksum(yDishwasher[k,t-tau] * dishwashersLoadThermal[k][tau]    for tau in range(len(dishwashersLoadThermal[k]))))
                    else:
                        model.addConstr(pDishwasher[k,t] == quicksum(yDishwasher[k,t-tau] * dishwashersLoadElectrical[k][tau] for tau in range(t+1)))
                        model.addConstr(qDishwasher[k,t] == quicksum(yDishwasher[k,t-tau] * dishwashersLoadThermal[k][tau]    for tau in range(t+1)))
                    # Minimum runtime
                    if t >= len(dishwashersLoadElectrical[k]):
                        model.addConstr(quicksum(yDishwasher[k,t-tau] for tau in range(1, len(dishwashersLoadThermal[k]))) <= 1-zDishwasher[k,t])
                    else:
                        model.addConstr(zDishwasher[k,t] == 0) # Only exception: Device has been started in the previous scheduling period
                    # Device has to start if soc exceeds capacity
                    # Big M: gains[t]
#                    model.addConstr(socDishwasher[k,t] <= dishwashersCapacity[k] + yDishwasher[k,t] *s dishwashersGains[k][t])
                    # Device must not operate until soc > socMayRun
#                    model.addConstr(socDishwasher[k,t] >= yDishwasher[k,t] * dishwashersSocMayrun[k])
                    # Storage equations
                    model.addConstr(socDishwasher[k,t] == lDishwasherPrevious[k] + dishwashersGains[k][t])
                    # Linearization of y * soc
                    # Upper bound: capacity[k] + gains[k][t]
                    # Lower bound: 0
                    model.addConstr(lDishwasher[k,t] <= yDishwasher[k,t] * (dishwashersCapacity[k] + max(dishwashersGains[k])))
                    model.addConstr(socDishwasherPrevious[k] - lDishwasher[k,t] <= (1 - yDishwasher[k,t]) * (dishwashersCapacity[k] + max(dishwashersGains[k])))
                    model.addConstr(socDishwasherPrevious[k] - lDishwasher[k,t] >= 0)
                
                # Aggregate total electricity and heat consumption
                model.addConstr(pDishwasherTotal[t] == quicksum(pDishwasher[k,t] for k in range(len(hasDishwashers))))
                model.addConstr(qDishwasherTotal[t] == quicksum(qDishwasher[k,t] for k in range(len(hasDishwashers))))
            
            if np.max(hasWashingmachines):
                for k in range(len(hasWashingmachines)):
                    # Mode transitions
                    model.addConstr(xWashingmachine[k,t] - xWashingmachinePrevious[k] == yWashingmachine[k,t] - zWashingmachine[k,t])
                    model.addConstr(yWashingmachine[k,t] + zWashingmachine[k,t] <= 1)
                    # Electricity and heat consumption
                    if t >= len(washingmachinesLoadElectrical[k]) - 1:
                        model.addConstr(pWashingmachine[k,t] == quicksum(yWashingmachine[k,t-tau] * washingmachinesLoadElectrical[k][tau] for tau in range(len(washingmachinesLoadThermal[k]))))
                        model.addConstr(qWashingmachine[k,t] == quicksum(yWashingmachine[k,t-tau] * washingmachinesLoadThermal[k][tau]    for tau in range(len(washingmachinesLoadThermal[k]))))
                    else:
                        model.addConstr(pWashingmachine[k,t] == quicksum(yWashingmachine[k,t-tau] * washingmachinesLoadElectrical[k][tau] for tau in range(t+1)))
                        model.addConstr(qWashingmachine[k,t] == quicksum(yWashingmachine[k,t-tau] * washingmachinesLoadThermal[k][tau]    for tau in range(t+1)))
                    # Minimum runtime
                    if t >= len(washingmachinesLoadElectrical[k]):
                        model.addConstr(quicksum(yWashingmachine[k,t-tau] for k in range(1, len(washingmachinesLoadThermal[k]))) <= 1-zWashingmachine[k,t])
                    else:
                        model.addConstr(zWashingmachine[k,t] == 0) # Only exception: Device has been started in the previous scheduling period
                    # Device has to start if soc exceeds capacity
                    # Big M: gains[t]
                    model.addConstr(socWashingmachine[k,t] <= washingmachinesCapacity[k] + yWashingmachine[k,t] * washingmachinesGains[k][t])
                    # Device must not operate until soc > socMayRun
                    model.addConstr(socWashingmachine[k,t] >= yWashingmachine[k,t] * washingmachinesSocMayrun[k])
                    # Storage equations
                    model.addConstr(socWashingmachine[k,t] == lWashingmachinePrevious[k] + washingmachinesGains[k][t])
                    # Linearization of y * soc
                    # Upper bound: capacity[k] + gains[k][t]
                    # Lower bound: 0
                    model.addConstr(lWashingmachine[k,t] <= yWashingmachine[k,t] * (washingmachinesCapacity[k] + washingmachinesGains[k][t]))
                    model.addConstr(socWashingmachinePrevious[k] - lWashingmachine[k,t] <= (1 - yWashingmachine[k,t]) * (washingmachinesCapacity[k] + washingmachinesGains[k][t]))
                    model.addConstr(socWashingmachinePrevious[k] - lWashingmachine[k,t] >= 0)
                
                # Aggregate total electricity and heat consumption
                model.addConstr(pWashingmachineTotal[t] == quicksum(pWashingmachine[k,t] for k in range(len(hasWashingmachines))))
                model.addConstr(qWashingmachineTotal[t] == quicksum(qWashingmachine[k,t] for k in range(len(hasWashingmachines))))
            
            # TES equations
            model.addConstr(qTesCharge[t] == qStorageCharge)
            model.addConstr(qTesDischarge[t] == qStorageDischarge)
            model.addConstr(qTesLosses[t] == tesKLosses * (tTes[t] - tesTSurroundings))
            model.addConstr(tesCapacity * cW / dt * (tTes[t] - tTesPrevious) == qTesCharge[t] - qTesDischarge[t] - qTesLosses[t])
            
            # Electricity balance
            model.addConstr(pAdditional[t] - pSurplus[t] == pConsumption - pProduction)    
            
        # Gurobi parameters
        model.Params.TimeLimit = 20            
            
        # Run model
        model.optimize()
        
        # Print final solution
        if model.status == GRB.OPTIMAL or model.status == GRB.TIME_LIMIT:
#            timeused = model.Runtime
#            GAP = model.MIPGap
            
#            obj = model.ObjVal
            
            # Save results
            # Info:
            # Schedules should be rounded, as they are binary.
            if hasBattery:
                resBatterySoc        = np.array([socBattery[t].X for t in xrange(timestepsUsedHorizon)])
                resBatteryPCharge    = np.array([pIncrease[t].X for t in xrange(timestepsUsedHorizon)])
                resBatteryPDischarge = np.array([pDecrease[t].X for t in xrange(timestepsUsedHorizon)])
                building.setBatteryResults(resBatterySoc, resBatteryPCharge, resBatteryPDischarge)
            if hasBoiler:
                resQBoiler = np.array([qBoiler[t].X for t in xrange(timestepsUsedHorizon)])
                resXBoiler = np.round([xBoiler[t].X for t in xrange(timestepsUsedHorizon)])
                building.setBoilerResults(resXBoiler, resQBoiler)
            if hasChp:
                resPChp = np.array([pChp[t].X for t in xrange(timestepsUsedHorizon)])
                resQChp = np.array([qChp[t].X for t in xrange(timestepsUsedHorizon)])
                resXChp = np.round([xChp[t].X for t in xrange(timestepsUsedHorizon)])
                building.setChpResults(resXChp, resQChp, resPChp)
            if hasElectricalHeater:
                resPElHeater = np.array([pElHeater[t].X for t in xrange(timestepsUsedHorizon)])
                resXElHeater = np.round([xElHeater[t].X for t in xrange(timestepsUsedHorizon)])
                building.setElectricalHeaterResults(resXElHeater, resPElHeater)
            if hasHeatpump:
                pass
            if hasInverterAcdc:
                resPInverterAcdc = np.array([pInverterAcdc[t].X for t in xrange(timestepsUsedHorizon)])
                building.setInverterResults(resPInverterAcdc, True)
            if hasInverterDcac:
                resPInverterDcac = np.array([pInverterDcac[t].X for t in xrange(timestepsUsedHorizon)])
                building.setInverterResults(resPInverterDcac, False)
            if hasTes:
                resTSto = np.array([tTes[t].X for t in xrange(timestepsUsedHorizon)])
                building.setTesResults(resTSto)
                
            if np.max(hasDishwashers):
                resSocDishwasher = np.array([[socDishwasher[k,t].X for t in xrange(timestepsUsedHorizon)] for k in xrange(len(hasDishwashers))])
                resPDishwasher = np.array([[pDishwasher[k,t].X for t in xrange(timestepsUsedHorizon)] for k in xrange(len(hasDishwashers))])
                resQDishwasher = np.array([[qDishwasher[k,t].X for t in xrange(timestepsUsedHorizon)] for k in xrange(len(hasDishwashers))])
                resXDishwasher = np.array([[xDishwasher[k,t].X for t in xrange(timestepsUsedHorizon)] for k in xrange(len(hasDishwashers))])
                building.setElectricalApplianceResults(resSocDishwasher, resPDishwasher, resQDishwasher, resXDishwasher, dishwasher=True)
            if np.max(hasWashingmachines):
                resSocWashingmachine = np.array([[socWashingmachine[k,t].X for t in xrange(timestepsUsedHorizon)] for k in xrange(len(hasWashingmachines))])
                resPWashingmachine= np.array([[pWashingmachine[k,t].X for t in xrange(timestepsUsedHorizon)] for k in xrange(len(hasWashingmachines))])
                resQWashingmachine= np.array([[qWashingmachine[k,t].X for t in xrange(timestepsUsedHorizon)] for k in xrange(len(hasWashingmachines))])
                resXWashingmachine= np.array([[xWashingmachine[k,t].X for t in xrange(timestepsUsedHorizon)] for k in xrange(len(hasWashingmachines))])
                building.setElectricalApplianceResults(resSocWashingmachine, resPWashingmachine, resQWashingmachine, resXWashingmachine, dishwasher=False)
                
        else:
            model.computeIIS()
            print('\nConstraints:')        
            for c in model.getConstrs():
                if c.IISConstr:
                    print('%s' % c.constrName)
            print('\nBounds:')
            for v in model.getVars():
                if v.IISLB > 0 :
                    print('Lower bound: %s' % v.VarName)
                elif v.IISUB > 0:
                    print('Upper bound: %s' % v.VarName) 
        
    except GurobiError:
        print('Error!')
    
    return resTSto
