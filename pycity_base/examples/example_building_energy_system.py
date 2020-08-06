#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script on how to generate and use building energy system (BES) object instances.
"""

from __future__ import division

import pycity_base.classes.timer
import pycity_base.classes.weather
import pycity_base.classes.environment
import pycity_base.classes.prices

import pycity_base.classes.supply.battery as bat
import pycity_base.classes.supply.building_energy_system as build_es
import pycity_base.classes.supply.boiler as boil
import pycity_base.classes.supply.combined_heat_power as chp
import pycity_base.classes.supply.electrical_heater as eh
import pycity_base.classes.supply.inverter as inv
import pycity_base.classes.supply.photovoltaic as pv
import pycity_base.classes.supply.thermal_energy_storage as tes


def print_bes_attributes(bes):
    print(("Has Battery: " + str(bes.has_battery)))
    print(("Has Boiler: " + str(bes.has_boiler)))
    print(("Has CHP unit: " + str(bes.has_chp)))
    print(("Has Electrical Heater: " + str(bes.has_electrical_heater)))
    print(("Has AC/DC inverter: " + str(bes.has_inverter_acdc)))
    print(("Has DC/AC inverter: " + str(bes.has_inverter_dcac)))
    print(("Has PV: " + str(bes.has_pv)))


def run_example():
    #  Generate environment
    timer = pycity_base.classes.timer.Timer()
    weather = pycity_base.classes.weather.Weather(timer, use_TRY=True)
    prices = pycity_base.classes.prices.Prices()
    environment = pycity_base.classes.environment.Environment(timer, weather,
                                                              prices)

    # Create different energy systems
    battery = bat.Battery(environment, 0.5, 4 * 3600 * 1000)
    boiler = boil.Boiler(environment, 10000, 0.8)
    chp_unit = chp.CHP(environment, 1000, 2000, 0.9)
    elh = eh.ElectricalHeater(environment, 3000, 0.99)
    inverter_ac_dc = inv.Inverter(environment, 0.98, 10000, True)
    inverter_dc_ac = inv.Inverter(environment, 0.98, 10000, False)
    pv_unit = pv.PV(environment=environment, method=0, area=50, eta_noct=0.15)
    thermal_storage = tes.ThermalEnergyStorage(environment, 50, 1000, 85)

    # Instantiate BES
    bes = build_es.BES(environment)

    # Print "status quo"
    print()
    print("Original BES - before adding devices")
    print_bes_attributes(bes)

    # Add appliances to bes
    bes.addDevice(battery)
    bes.addDevice(boiler)
    bes.addDevice(chp_unit)
    bes.addDevice(elh)
    bes.addDevice(inverter_ac_dc)
    bes.addDevice(inverter_dc_ac)

    bes.addMultipleDevices([pv_unit, thermal_storage])

    # Print current status
    print()
    print("Final BES - after adding devices")
    print_bes_attributes(bes)

    # Check if objects stored in BES are the same as the original objects:
    print()
    print("Battery: " + str(battery in bes.battery_units))
    print("Boiler: " + str(boiler in bes.boilers))
    print("CHP: " + str(chp in bes.chp_units))
    print("Electrical heater: " + str(elh in bes.electrical_heaters))
    print("Inverter AC to DC: " + str(inverter_ac_dc in bes.inverters_acdc))
    print("Inverter DC to AC: " + str(inverter_dc_ac in bes.inverters_dcac))
    print("PV: " + str(pv in bes.pv_units))
    print("TES: " + str(tes in bes.tes_units))

    bes.getHasDevices(all_devices=True)

    bes.getHasDevices(all_devices=False,
                      battery=True,
                      boiler=True,
                      chp=True,
                      compression_chiller=True,
                      electrical_heater=True,
                      heatpump=True,
                      inverter_acdc=True,
                      inverter_dcac=True,
                      pv=True,
                      tes=True)


if __name__ == '__main__':
    #  Run program
    run_example()
