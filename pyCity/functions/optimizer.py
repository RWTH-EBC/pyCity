# -*- coding: utf-8 -*-
"""
Created on Mon Feb 09 12:24:08 2015

@author: tsz
"""

from __future__ import division

from gurobipy import *

def optimize(bes, prices):
    """
    """
    
#    self.timer               = timer
#        
#    self.battery             = []
#    self.boiler              = []
#    self.chp                 = []
#    self.demand_dhw          = []
#    self.demand_electrical   = []
#    self.demand_spaceheating = []
#    self.dishwasher          = []
#    self.electrical_heater   = []
#    self.heatpump            = []
#    self.inverter_acdc       = []
#    self.inverter_dcac       = []
#    self.pv                  = []
#    self.tes                 = []
#    self.washingmachine      = []
#    self.weather             = []
    
    timesteps = bes.timer.timesteps_horizon
    dt = bes.timer.time_discretization

    c_w = 4180 # Heat capacity of water in J/(kg K)

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
        soc_battery = {}
        p_increase = {} # Output of the AC/DC inverter
        p_decrease = {} # Input of the DC/AC inverter
        
        # Boiler
        q_boiler = {}
        x_boiler = {}
        
        # CHP
        q_chp = {}
        p_chp = {}
        x_chp = {}
        
        # Dishwasher
        soc_dishwasher = {}
        x_dishwasher   = {}
        y_dishwasher   = {}
        z_dishwasher   = {}
        l_dishwasher   = {} # Linearization of y * soc
        p_dishwasher   = {}
        q_dishwasher   = {}
        # Dishwasher - all installed devices
        p_dishwasher_total = {}
        q_dishwasher_total = {}
        
        # Electrical heater
        x_el_heater = {}
        p_el_heater = {}
        q_el_heater = {}
        
        # Heat pump
        x_heatpump = {}
        p_heatpump = {}
        q_heatpump = {}
        
        # Inverter - AC to DC
        p_inverter_ac_dc = {} # Input -> electrical sink of the building
        
        # Inverter - DC to AC
        p_inverter_dc_ac = {} # Output -> electrical gain of the building
        
        # Thermal energy storage (TES)
        t_tes = {}
        q_tes_losses = {}
        q_tes_charge = {}
        q_tes_discharge = {}
        
        # Wasching machine
        soc_washingmachine = {}
        x_washingmachine   = {}
        y_washingmachine   = {}
        z_washingmachine   = {}
        l_washingmachine   = {} # Linearization of y * soc
        p_washingmachine   = {}
        q_washingmachine   = {}
        # Washing machine - all installed devices
        p_washingmachine_total = {}
        q_washingmachine_total = {}
        
        # Interaction with environment
        p_surplus = {}
        p_additional = {}
        
        # Fill the empty dictionaries if the device is installed
        for t in timesteps:
            # Every house has a TES unit and the interaction with its environment:
            # TES
            t_tes[t]           = model.addVar(vtype=GRB.CONTINUOUS, name="T_TES_"+str(t),           lb=bes.tes.t_flow_min[t], ub=bes.tes.t_max)
            q_tes_losses[t]    = model.addVar(vtype=GRB.CONTINUOUS, name="Q_TES_losses_"+str(t),    lb=0)
            q_tes_charge[t]    = model.addVar(vtype=GRB.CONTINUOUS, name="Q_TES_charge_"+str(t),    lb=0)
            q_tes_discharge[t] = model.addVar(vtype=GRB.CONTINUOUS, name="Q_TES_discharge_"+str(t), lb=0)
            # Interaction
            p_surplus[t]    = model.addVar(vtype=GRB.CONTINUOUS, name="P_surplus_"+str(t),    lb=0)
            p_additional[t] = model.addVar(vtype=GRB.CONTINUOUS, name="P_additional_"+str(t), lb=0)
            
            if bes.has_battery:
                soc_battery[t]      = model.addVar(vtype=GRB.CONTINUOUS, name="SOC_Battery_"+str(t), lb=0, ub=bes.battery.capacity)
                p_increase[t]       = model.addVar(vtype=GRB.CONTINUOUS, name="P_increase_"+str(t),  lb=0, ub=bes.inverter_acdc.p_nominal * bes.inverter_acdc.eta)
                p_decrease[t]       = model.addVar(vtype=GRB.CONTINUOUS, name="P_decrease_"+str(t),  lb=0, ub=bes.inverter_dcac.p_nominal)
                p_inverter_ac_dc[t] = model.addVar(vtype=GRB.CONTINUOUS, name="P_inv_ac_dc_"+str(t), lb=0, ub=bes.inverter_acdc.p_nominal)
                p_inverter_dc_ac[t] = model.addVar(vtype=GRB.CONTINUOUS, name="P_inv_dc_ac_"+str(t), lb=0, ub=bes.inverter_dcac.p_nominal * bes.inverter_dcac.eta)
            
            if bes.has_boiler:
                q_boiler[t] = model.addVar(vtype=GRB.CONTINUOUS, name="Q_Boiler_"+str(t), lb=0, ub=bes.boiler.q_nominal)
                x_boiler[t] = model.addVar(vtype=GRB.BINARY,     name="X_Boiler_"+str(t))

            if bes.has_chp:
                q_chp[t] = model.addVar(vtype=GRB.CONTINUOUS, name="Q_CHP_"+str(t), lb=0, ub=bes.chp.q_nominal)
                p_chp[t] = model.addVar(vtype=GRB.CONTINUOUS, name="P_CHP_"+str(t), lb=0, ub=bes.chp.p_nominal)
                x_chp[t] = model.addVar(vtype=GRB.BINARY,     name="X_CHP_"+str(t))
                
            if bes.has_dishwasher:
                for k in range(len(bes.dishwasher)):
                    soc_dishwasher[k,t] = model.addVar(vtype=GRB.CONTINUOUS, name="SOC_Dishwasher_"+str(t)+"_"+str(k), lb=0)
                    p_dishwasher[k,t]   = model.addVar(vtype=GRB.CONTINUOUS, name="P_Dishwasher_"+str(t)+"_"+str(k),   lb=0, ub=bes.dishwasher[k].load_electrical.loadcurve[t])
                    q_dishwasher[k,t]   = model.addVar(vtype=GRB.CONTINUOUS, name="Q_Dishwasher_"+str(t)+"_"+str(k),   lb=0, ub=bes.dishwasher[k].load_thermal.loadcurve[t])
                    l_dishwasher[k,t]   = model.addVar(vtype=GRB.CONTINUOUS, name="L_Dishwasher_"+str(t)+"_"+str(k),   lb=0)
                    x_dishwasher[k,t]   = model.addVar(vtype=GRB.BINARY,     name="X_Dishwasher_"+str(t)+"_"+str(k))
                    y_dishwasher[k,t]   = model.addVar(vtype=GRB.BINARY,     name="Y_Dishwasher_"+str(t)+"_"+str(k))
                    z_dishwasher[k,t]   = model.addVar(vtype=GRB.BINARY,     name="Z_Dishwasher_"+str(t)+"_"+str(k))
                # Dishwasher - all installed devices
                p_dishwasher_total[t] = model.addVar(vtype=GRB.CONTINUOUS, name="P_Dishwasher_total_"+str(t), lb=0)
                q_dishwasher_total[t] = model.addVar(vtype=GRB.CONTINUOUS, name="Q_Dishwasher_total_"+str(t), lb=0)
                
            if bes.has_electrical_heater:
                x_el_heater[t] = model.addVar(vtype=GRB.BINARY,     name="X_El_Heater_"+str(t))
                p_el_heater[t] = model.addVar(vtype=GRB.CONTINUOUS, name="P_El_Heater_"+str(t), lb=0, ub=bes.electrical_heater.p_nominal)
                q_el_heater[t] = model.addVar(vtype=GRB.CONTINUOUS, name="Q_El_Heater_"+str(t), lb=0, ub=bes.electrical_heater.q_nominal)
            
            if bes.has_heatpump:
                x_heatpump[t] = model.addVar(vtype=GRB.BINARY,     name="X_Heatpump_"+str(t))
                p_heatpump[t] = model.addVar(vtype=GRB.CONTINUOUS, name="P_Heatpump_"+str(t), lb=0, ub=bes.heatpump.p_nominal[t])
                q_heatpump[t] = model.addVar(vtype=GRB.CONTINUOUS, name="Q_Heatpump_"+str(t), lb=0, ub=bes.heatpump.q_nominal[t])
                
            if bes.has_washingmachine:
                for k in range(len(bes.washingmachine)):
                    soc_washingmachine[k,t] = model.addVar(vtype=GRB.CONTINUOUS, name="SOC_Washingmachine_"+str(t)+"_"+str(k), lb=0)
                    p_washingmachine[k,t]   = model.addVar(vtype=GRB.CONTINUOUS, name="P_Washingmachine_"+str(t)+"_"+str(k),   lb=0, ub=bes.washingmachine[k].load_electrical.loadcurve[t])
                    q_washingmachine[k,t]   = model.addVar(vtype=GRB.CONTINUOUS, name="Q_Washingmachine_"+str(t)+"_"+str(k),   lb=0, ub=bes.washingmachine[k].load_thermal.loadcurve[t])
                    l_washingmachine[k,t]   = model.addVar(vtype=GRB.CONTINUOUS, name="L_Washingmachine_"+str(t)+"_"+str(k),   lb=0)
                    x_washingmachine[k,t]   = model.addVar(vtype=GRB.BINARY,     name="X_Washingmachine_"+str(t)+"_"+str(k))
                    y_washingmachine[k,t]   = model.addVar(vtype=GRB.BINARY,     name="Y_Washingmachine_"+str(t)+"_"+str(k))
                    z_washingmachine[k,t]   = model.addVar(vtype=GRB.BINARY,     name="Z_Washingmachine_"+str(t)+"_"+str(k))
                # Washing machine - all installed devices
                p_washingmachine_total[t] = model.addVar(vtype=GRB.CONTINUOUS, name="P_Washingmachine_total_"+str(t), lb=0)
                q_washingmachine_total[t] = model.addVar(vtype=GRB.CONTINUOUS, name="Q_Washingmachine_total_"+str(t), lb=0)
        
        
        # Integrate new variables into the model
        model.update()


        # Set objective function
        # Costs from boiler usage
        if bes.has_boiler:
            gas_boiler = quicksum(1/bes.boiler.eta * q_boiler[t] * prices.c_gas * dt for t in range(timesteps))
        else:
            gas_boiler = 0
        
        # Costs from CHP usage
        if bes.has_chp:
            rev_chp = quicksum(p_chp[t] * prices.rev_chp * dt for t in range(timesteps))
            gas_chp = quicksum(1/bes.chp.omega * (p_chp[t] + q_chp[t]) * prices.c_gas * dt for t in range(timesteps))
        else:
            rev_chp = 0
            gas_chp = 0
        
        # Grid interaction
        costs_electricity_import   = quicksum(p_additional[t] * prices.c_el * dt for t in range(timesteps))
        revenue_electricity_export = quicksum(p_surplus[t] * prices.rev_el * dt for t in range(timesteps))
        
        # Objective function
        model.setObjective(gas_boiler - rev_chp + gas_chp + costs_electricity_import - revenue_electricity_export, GRB.MINIMIZE)
        
        for t in range(timesteps):
            # Handle time step zero (necessary for storage-like equations)
            if t == 0:
                t_tes_previous = bes.tes.t_init
                soc_battery_previous = bes.battery.SOC_init
                if bes.has_dishwasher:
                    soc_dishwasher_previous = []
                    x_dishwasher_previous = []
                    l_dishwasher_previous = []
                    for k in range(len(bes.dishwasher)):
                        soc_dishwasher_previous.append(bes.dishwasher[k].SOC_init)
                        x_dishwasher_previous.append(bes.dishwasher[k].x_init)
                        l_dishwasher_previous.append(soc_dishwasher_previous[k] * (1-y_dishwasher[k,t]))
                if bes.has_washingmachine:
                    soc_washingmachine_previous = []
                    x_washingmachine_previous = []
                    l_washingmachine_previous = []
                    for k in range(len(bes.washingmachine)):
                        soc_washingmachine_previous.append(bes.washingmachine[k].SOC_init)
                        x_washingmachine_previous.append(bes.washingmachine[k].x_init)
                        l_washingmachine_previous.append(soc_washingmachine_previous[k] * (1-y_washingmachine[k,t]))
            else:
                t_tes_previous = t_tes[t-1]
                soc_battery_previous = soc_battery[t-1]
                if bes.has_dishwasher:
                    soc_dishwasher_previous = []
                    x_dishwasher_previous = []
                    l_dishwasher_previous = []
                    for k in range(len(bes.dishwasher)):
                        soc_dishwasher_previous.append(soc_dishwasher[k,t-1])
                        x_dishwasher_previous.append(x_dishwasher[k,t-1])
                        l_dishwasher_previous.append(soc_dishwasher_previous[k] - l_dishwasher[k,t])
                if bes.has_washingmachine:
                    soc_washingmachine_previous = []
                    x_washingmachine_previous = []
                    l_washingmachine_previous = []
                    for k in range(len(bes.washingmachine)):
                        soc_washingmachine_previous.append(soc_washingmachine[k,t-1])
                        x_washingmachine_previous.append(x_washingmachine[k,t-1])
                        l_washingmachine_previous.append(soc_washingmachine_previous[k] - l_washingmachine[k,t])
            
            # Compute inputs and outputs of each device
            q_storage_charge = 0
            q_storage_discharge = 0
            p_production = 0
            p_consumption = 0

            if bes.has_battery:
                model.addConstr(p_increase[t] == p_inverter_ac_dc[t] * bes.inverter_acdc.eta)
                model.addConstr(p_decrease[t] * bes.inverter_dcac.eta == p_inverter_dc_ac[t])
                model.addConstr(soc_battery[t] == (1-bes.battery.self_discharge) * soc_battery_previous + dt * (bes.battery.eta_charge * P_increase_[t] - 1/bes.battery.eta_discharge * P_decrease_[t]))
                p_production  += p_inverter_dc_ac[t]
                p_consumption += p_inverter_ac_dc[t]
            
            if bes.has_boiler:
                model.addConstr(q_boiler[t] >= x_boiler[t] * bes.boiler.q_nominal * bes.boiler.lower_activation_limit)
                model.addConstr(q_boiler[t] <= x_boiler[t] * bes.boiler.q_nominal)
                q_storage_charge += q_boiler[t]
            
            if bes.has_chp:
                model.addConstr(q_chp[t] >= x_chp[t] * bes.chp.q_nominal * bes.chp.lower_activation_limit)
                model.addConstr(q_chp[t] <= x_chp[t] * bes.chp.q_nominal)
                model.addConstr(p_chp[t] == q_chp[t] * bes.chp.sigma)
                q_storage_charge += q_chp[t]
                p_production += p_chp[t]
        
            if bes.has_dishwasher:
                for k in range(len(bes.dishwasher)):
                    # Mode transitions
                    model.addConstr(x_dishwasher[k,t] - x_dishwasher_previous[k] == y_dishwasher[k,t] - z_dishwasher[k,t])
                    model.addConstr(y_dishwasher[k,t] + z_dishwasher[k,t] <= 1)
                    # Electricity and heat consumption
                    if t >= len(bes.dishwasher[k].load_electrical.loadcurve) - 1:
                        model.addConstr(p_dishwasher[k,t] == quicksum(y_dishwasher[k,t-tau] * bes.dishwasher[k].load_electrical.loadcurve[t] for tau in range(len(bes.dishwasher[k].load_electrical.loadcurve))))
                        model.addConstr(q_dishwasher[k,t] == quicksum(y_dishwasher[k,t-tau] * bes.dishwasher[k].load_thermal.loadcurve[t]    for tau in range(len(bes.dishwasher[k].load_electrical.loadcurve))))
                    else:
                        model.addConstr(p_dishwasher[k,t] == quicksum(y_dishwasher[k,t-tau] * bes.dishwasher[k].load_electrical.loadcurve[t] for tau in range(t+1)))
                        model.addConstr(q_dishwasher[k,t] == quicksum(y_dishwasher[k,t-tau] * bes.dishwasher[k].load_thermal.loadcurve[t]    for tau in range(t+1)))
                    # Minimum runtime
                    if t >= len(bes.dishwasher[k].load_electrical.loadcurve):
                        model.addConstr(quicksum(y_dishwasher[k,t-tau] for k in range(1, len(bes.dishwasher[k].load_electrical.loadcurve))) <= 1-z_dishwasher[k,t])
                    else:
                        model.addConstr(z_dishwasher[k,t] == 0) # Only exception: Device has been started in the previous scheduling period
                    # Storage equations
                    model.addConstr(soc_dishwasher[k,t] == l_dishwasher_previous[k] + bes.dishwasher[k].gains[t])
                    model.addConstr(l_dishwasher[k,t] <= y_dishwasher[k,t] * 10 * bes.dishwasher[k].capacity)
                    model.addConstr(soc_dishwasher[k,t] - l_dishwasher[k,t] <= (1 - y_dishwasher[k,t]) * 10 * bes.dishwasher[k].capacity)
                    model.addConstr(soc_dishwasher[k,t] - l_dishwasher[k,t] >= 0)
                
                # Aggregate total electricity and heat consumption
                model.addConstr(p_dishwasher_total[t] == quicksum(p_dishwasher[k,t] for k in range(len(bes.dishwasher))))
                model.addConstr(q_dishwasher_total[t] == quicksum(q_dishwasher[k,t] for k in range(len(bes.dishwasher))))
        
            if bes.has_electrical_heater:
                model.addConstr(q_el_heater[t] >= x_el_heater[t] * bes.electrical_heater.q_nominal * bes.electrical_heater.lower_activation_limit)
                model.addConstr(q_el_heater[t] <= x_el_heater[t] * bes.electrical_heater.q_nominal)
                model.addConstr(p_el_heater[t] == 1/bes.electrical_heater.eta * q_el_heater[t])
                q_storage_charge += q_el_heater[t]
                p_consumption += p_el_heater[t]
        
            if bes.has_heatpump:
                model.addConstr(q_heatpump[t] >= x_el_heater[t] * bes.heatpump.q_nominal * bes.heatpump.lower_activation_limit)
                model.addConstr(q_heatpump[t] <= x_el_heater[t] * bes.heatpump.q_nominal)
                model.addConstr(p_heatpump[t] == 1/bes.heatpump.cop[t] * q_heatpump[t])
                q_storage_charge += q_heatpump[t]
                p_consumption += p_heatpump[t]

            if bes.has_pv:
                p_production += bes.pv.power[t]                
            
            if bes.has_washingmachine:
                for k in range(len(bes.washingmachine)):
                    # Mode transitions
                    model.addConstr(x_washingmachine[k,t] - x_washingmachine_previous[k] == y_washingmachine[k,t] - z_washingmachine[k,t])
                    model.addConstr(y_washingmachine[k,t] + z_washingmachine[k,t] <= 1)
                    # Electricity and heat consumption
                    if t >= len(bes.washingmachine[k].load_electrical.loadcurve) - 1:
                        model.addConstr(p_washingmachine[k,t] == quicksum(y_washingmachine[k,t-tau] * bes.washingmachine[k].load_electrical.loadcurve[t] for tau in range(len(bes.washingmachine[k].load_electrical.loadcurve))))
                        model.addConstr(q_washingmachine[k,t] == quicksum(y_washingmachine[k,t-tau] * bes.washingmachine[k].load_thermal.loadcurve[t]    for tau in range(len(bes.washingmachine[k].load_electrical.loadcurve))))
                    else:
                        model.addConstr(p_washingmachine[k,t] == quicksum(y_washingmachine[k,t-tau] * bes.washingmachine[k].load_electrical.loadcurve[t] for tau in range(t+1)))
                        model.addConstr(q_washingmachine[k,t] == quicksum(y_washingmachine[k,t-tau] * bes.washingmachine[k].load_thermal.loadcurve[t]    for tau in range(t+1)))
                    # Minimum runtime
                    if t >= len(bes.washingmachine[k].load_electrical.loadcurve):
                        model.addConstr(quicksum(y_washingmachine[k,t-tau] for k in range(1, len(bes.washingmachine[k].load_electrical.loadcurve))) <= 1-z_washingmachine[k,t])
                    else:
                        model.addConstr(z_washingmachine[k,t] == 0) # Only exception: Device has been started in the previous scheduling period
                    # Storage equations
                    model.addConstr(soc_washingmachine[k,t] == l_washingmachine_previous[k] + bes.washingmachine[k].gains[t])
                    # Linearization of l=soc*y
                    model.addConstr(l_washingmachine[k,t] <= y_dishwasher[k,t] * 10 * bes.washingmachine[k].capacity)
                    model.addConstr(soc_washingmachine[k,t] - l_washingmachine[k,t] <= (1 - y_washingmachine[k,t]) * 10 * bes.washingmachine[k].capacity)
                    model.addConstr(soc_washingmachine[k,t] - l_washingmachine[k,t] >= 0)
                    
                    # If SOC > capacity: force a starting event
                    model.addConstr(soc_washingmachine[k,t] <= bes.washingmachine[k].capacity + y_washingmachine[k,t] * bes.washingmachine[k].capacity)
                    # If SOC < SOC_mayrun: forbid a starting event
                    model.addConstr(soc_washingmachine[k,t] <= y_washingmachine[k,t] * bes.washingmachine[k].SOC_mayrun)
                    
                # Aggregate total electricity and heat consumption
                model.addConstr(p_washingmachine_total[t] == quicksum(p_washingmachine[k,t] for k in range(len(bes.washingmachine))))
                model.addConstr(q_washingmachine_total[t] == quicksum(q_washingmachine[k,t] for k in range(len(bes.washingmachine))))
            
            # TES equations
            model.addConstr(q_tes_charge[t] == q_storage_charge)
            model.addConstr(q_tes_discharge[t] == q_storage_discharge)
            model.addConstr(q_tes_losses[t] == bes.tes.k_losses * (t_tes[t] - bes.tes.t_surroundings))
            model.addConstr(bes.tes.capacity * c_w / dt * (t_tes[t] - t_tes_previous) == q_tes_charge[t] - q_tes_discharge[t] - q_tes_losses[t])
            
            # Electricity balance
            model.addConstr(p_additional[t] - p_surplus[t] == p_consumption - p_production)
        
#    self.boiler              = []
#    self.chp                 = []
#    self.demand_dhw          = []
#    self.demand_electrical   = []
#    self.demand_spaceheating = []
#    self.dishwasher          = []
#    self.electrical_heater   = []
#    self.heatpump            = []
#    self.inverter_acdc       = []
#    self.inverter_dcac       = []
#    self.pv                  = []
#    self.tes                 = []
#    self.washingmachine      = []
#    self.weather             = []
        
    except GurobiError:
        print('Error!')
    
    
    return bes