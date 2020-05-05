#!/usr/bin/env python
# coding=utf-8
"""
Test all pycity_base examples.
"""

import pycity_base.examples.example_absorption_chiller as ach
import pycity_base.examples.example_apartment as ap
import pycity_base.examples.example_battery as batt
import pycity_base.examples.example_boiler as boil
import pycity_base.examples.example_building as build
import pycity_base.examples.example_building_energy_system as bes
import pycity_base.examples.example_city_disctrict as city
import pycity_base.examples.example_combined_heat_power as chp
import pycity_base.examples.example_compression_chiller as ch
import pycity_base.examples.example_cooling_device as cd
import pycity_base.examples.example_domestic_hot_water as dhw
import pycity_base.examples.example_electrical_demand as eld
import pycity_base.examples.example_electrical_heater as elh
import pycity_base.examples.example_environment as env
import pycity_base.examples.example_heat_pump as hp
import pycity_base.examples.example_heating_device as heatd
import pycity_base.examples.example_inverter as inv
import pycity_base.examples.example_occupancy as occ
import pycity_base.examples.example_photovoltaic as pv
import pycity_base.examples.example_readme as rm
import pycity_base.examples.example_solar_radiation_tilted_surface as sol
import pycity_base.examples.example_space_heating as sph
import pycity_base.examples.example_thermal_energy_storage as tes
import pycity_base.examples.example_timer as timer
import pycity_base.examples.example_weather as weat
import pycity_base.examples.example_wind_energy_converter as wec


class TestExamples():

    def test_examples(self):

        ach.run_example()

        ap.run_example()

        batt.run_example()

        boil.run_example()

        build.run_example()

        bes.run_example()

        city.run_example()

        chp.run_example()

        ch.run_example()

        cd.run_example()

        dhw.run_example()

        eld.run_example()

        elh.run_example()

        env.run_example()

        hp.run_example()

        heatd.run_example()

        inv.run_example()

        occ.run_example()

        pv.run_example()

        rm.run_example()

        sol.run_example()

        sph.run_example()

        tes.run_example()

        timer.run_example()

        weat.run_example()

        wec.run_example()
