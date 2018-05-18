#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

import pycity_base.examples.solar_radiation_tilted_surface as sol
import pycity_base.examples.example_apartment as ap
import pycity_base.examples.example_battery as batt
import pycity_base.examples.example_bes as bes
import pycity_base.examples.example_boiler as boil
import pycity_base.examples.example_building as build
import pycity_base.examples.example_chp as chp
import pycity_base.examples.example_cityDisctrict as city
import pycity_base.examples.example_domesticHotWater as dhw
import pycity_base.examples.example_electricalDemand as eld
import pycity_base.examples.example_electricalHeater as elh
import pycity_base.examples.example_environment as env
import pycity_base.examples.example_heatingDevice as heatd
import pycity_base.examples.example_heatpump as hp
import pycity_base.examples.example_inverter as inv
import pycity_base.examples.example_pv as pv
import pycity_base.examples.example_spaceHeating as sph
import pycity_base.examples.example_tes as tes
import pycity_base.examples.example_timer as timer
import pycity_base.examples.example_weather as weat
import pycity_base.examples.example_windEnergyConverter as wind
import pycity_base.examples.example_occupancy as occ
import pycity_base.examples.example_coolingDevice as cd
import pycity_base.examples.example_compressionchiller as ch


class Test_Examples():

    def test_examples(self):

        sol.run_example()

        ap.run_test()

        batt.run_test()

        bes.run_test()

        boil.run_test()

        build.run_test()

        chp.run_test()

        city.run_test()

        dhw.run_test()

        eld.run_test()

        elh.run_test()

        env.run_test()

        heatd.run_test()

        hp.run_test()

        inv.run_test()

        occ.exampe_occupancy()

        pv.run_test()

        sph.run_test()

        tes.run_test()

        timer.run_test()

        weat.run_test()

        wind.run_test()

        cd.run_test()

        ch.run_test()
