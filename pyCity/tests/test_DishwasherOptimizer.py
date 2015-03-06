# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 09:29:44 2015

@author: tsz
"""

from __future__ import division
import numpy as np

from gurobipy import *

def optimize(pv, dishwasher, environment):
    
    # PV:
    pvPower = pv.getPower()

    # Dishwasher:
    # Initial values
    initialValuesDishwashers = dishwasher.getInitialState()
    dishwashersInitialSoc = initialValuesDishwashers[0]
    dishwashersInitialX   = initialValuesDishwashers[1]
    dishwashersInitialY   = initialValuesDishwashers[2]
    dishwashersInitialY_f = np.flipud(dishwashersInitialY)
    if dishwashersInitialY_f[0] == 1:
        pass
#    dishwashersInitialY[4] = 1
    # Nominals
    nominalsDishwashers = dishwasher.getNominals()
    dishwashersCapacity          = nominalsDishwashers[0]
    dishwashersSocMayrun         = nominalsDishwashers[1]
    dishwashersGains             = nominalsDishwashers[2]
    dishwashersLoadElectrical    = nominalsDishwashers[4]

    (cEl, cGas, revChp, revEl) = environment.getPriceInformation()
    
    timesteps = environment.getTimestepsHorizon()
    timestepsUsedHorizon = environment.getTimestepsUsedHorizon()
    dt = environment.getTimeDiscretization()

    # Gurobi model
    try:
        # Create a new model
        model = Model("BES_optimization")
    
        # Create variables
        """
        Nomenclature: 
            soc -> state of charge (without unit)
            p   -> electrical power in W
            x   -> status variable (on/off - binary)
            y   -> starting procedure (yes/no - binary)
            z   -> shutdown procedure (yes/no - binary)
        """
        # Dishwashers
        socDishwasher = {}
        xDishwasher   = {}
        yDishwasher   = {}
        zDishwasher   = {}
        lDishwasher   = {} # Linearization of y * soc
        pDishwasher   = {}
        
        # Interaction with environment
        pSurplus = {}
        pAdditional = {}
        
        # Fill the empty dictionaries if the device is installed
        for t in xrange(timesteps):
            # Interaction
            pSurplus[t]    = model.addVar(vtype=GRB.CONTINUOUS, name="P_surplus_"+str(t),    lb=0)
            pAdditional[t] = model.addVar(vtype=GRB.CONTINUOUS, name="P_additional_"+str(t), lb=0)
            
            # Dishwasher
            socDishwasher[t] = model.addVar(vtype=GRB.CONTINUOUS, name="SOC_Dishwasher_"+str(t), lb=0, ub=dishwashersCapacity + np.max(dishwashersGains))
            pDishwasher[t]   = model.addVar(vtype=GRB.CONTINUOUS, name="P_Dishwasher_"+str(t),   lb=0)#, ub=np.max(dishwashersLoadElectrical))
            lDishwasher[t]   = model.addVar(vtype=GRB.CONTINUOUS, name="L_Dishwasher_"+str(t),   lb=0)
            xDishwasher[t]   = model.addVar(vtype=GRB.BINARY,     name="X_Dishwasher_"+str(t))
            yDishwasher[t]   = model.addVar(vtype=GRB.BINARY,     name="Y_Dishwasher_"+str(t))
            zDishwasher[t]   = model.addVar(vtype=GRB.BINARY,     name="Z_Dishwasher_"+str(t))
        
        # Integrate new variables into the model
        model.update()
        
        # Set objective function
        # Grid interaction
        costsElectricityImport   = quicksum(pAdditional[t] * cEl * dt for t in range(timesteps))
        revenueElectricityExport = quicksum(pSurplus[t] * revEl * dt for t in range(timesteps))
        
        # Objective function
        model.setObjective(costsElectricityImport - revenueElectricityExport, GRB.MINIMIZE)
        
#        model.addConstr(xDishwasher[0] <= 0)
        
        for t in xrange(timesteps):
            if t == 0:
                socDishwasherPrevious = dishwashersInitialSoc
                xDishwasherPrevious = dishwashersInitialX
            else:
                socDishwasherPrevious = socDishwasher[t-1]
                xDishwasherPrevious = xDishwasher[t-1]
            if t < len(dishwashersLoadElectrical):
                yDishwasherPrevious = dishwashersInitialY[t]
            else:
                yDishwasherPrevious = yDishwasher[t-len(dishwashersLoadElectrical)]
                
            if t < len(dishwashersLoadElectrical) and max(dishwashersInitialY > 0.5) and np.argmax(dishwashersInitialY_f) + t + 1 < len(dishwashersLoadElectrical):
                pDishwasherNow = dishwashersLoadElectrical[np.argmax(dishwashersInitialY_f) + t + 1]
            else:
                pDishwasherNow = quicksum(yDishwasher[t-tau] * (dishwashersLoadElectrical[tau]) for tau in xrange(min(t+1, len(dishwashersLoadElectrical))))
            
            # Electricity balance
            model.addConstr(pSurplus[t] - pAdditional[t] == pvPower[t] - pDishwasher[t], "ElectricityBalance_"+str(t))
            
            # SOC balance
            model.addConstr(socDishwasher[t] == socDishwasherPrevious - lDishwasher[t] + dishwashersGains[t], "SOCBalance_"+str(t))
            
            # Starting procedures
            model.addConstr(xDishwasher[t] - xDishwasherPrevious == yDishwasher[t] - zDishwasher[t], "Start1_"+str(t))
            model.addConstr(yDishwasher[t] + zDishwasher[t] <= 1, "Start2_"+str(t))
            
            # Runtime restriction
            model.addConstr(zDishwasher[t] == yDishwasherPrevious, "Runtime_"+str(t))
            
            # Power output
            model.addConstr(pDishwasher[t] == pDishwasherNow, "PowerConsumption_"+str(t))
            
            # Linearization of y * soc
            mDishwasher = dishwashersCapacity + np.max(dishwashersGains)
            model.addConstr(lDishwasher[t] <= yDishwasher[t] * mDishwasher, "Lin1_"+str(t))
            model.addConstr(socDishwasherPrevious - lDishwasher[t] >= 0, "Lin2_"+str(t))
            model.addConstr(socDishwasherPrevious - lDishwasher[t] <= (1 - yDishwasher[t]) * mDishwasher, "Lin3_"+str(t))
            
            # Device has to start if soc exceeds capacity
            # Big M: gains[t]
            model.addConstr(yDishwasher[t] * dishwashersGains[t] + dishwashersCapacity>= socDishwasherPrevious, "MustRun_"+str(t))
            # Device must not operate until soc > socMayRun
            model.addConstr(yDishwasher[t] * dishwashersSocMayrun <= socDishwasherPrevious, "MayRun_"+str(t))

        # Gurobi parameters
        model.Params.TimeLimit = 20            
            
        # Run model
        model.optimize()
        
        # Print final solution
        if model.status == GRB.OPTIMAL or model.status == GRB.TIME_LIMIT:
            resSocDishwasher = np.array([socDishwasher[t].X for t in xrange(timestepsUsedHorizon)])
            resPDishwasher = np.array([pDishwasher[t].X for t in xrange(timestepsUsedHorizon)])
            resXDishwasher = np.round([xDishwasher[t].X for t in xrange(timestepsUsedHorizon)])
            dishwasher.setSoc(resSocDishwasher)
            dishwasher.setSchedule(resXDishwasher)
            dishwasher.setPConsumption(resPDishwasher)
            
        else:
            model.computeIIS()
            model.write("model.ilp")
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
