"""
Script executes all files in tests folder
"""

import pycity.tests.test_apartment as ap
import pycity.tests.test_battery as batt
import pycity.tests.test_bes as bes
import pycity.tests.test_boiler as boil
import pycity.tests.test_building as build
import pycity.tests.test_chp as chp
import pycity.tests.test_cityDisctrict as city
import pycity.tests.test_domesticHotWater as dhw
import pycity.tests.test_electricalDemand as eld
import pycity.tests.test_electricalHeater as elh
import pycity.tests.test_environment as env
import pycity.tests.test_heatingDevice as heatd
import pycity.tests.test_heatpump as hp
import pycity.tests.test_inverter as inv
import pycity.tests.test_pv as pv
import pycity.tests.test_spaceHeating as sph
import pycity.tests.test_tes as tes
import pycity.tests.test_timer as timer
import pycity.tests.test_weather as weat
import pycity.tests.test_windEnergyConverter as wind


def run_all_test():
    print('## Test apartment ##################################################################')
    ap.run_test()
    print('## Test battery ##################################################################')
    batt.run_test()
    print('## Test building energy system (BES) ##################################################################')
    bes.run_test()
    print('## Test boiler ##################################################################')
    boil.run_test()
    print('## Test building ##################################################################')
    build.run_test()
    print('## Test chp ##################################################################')
    chp.run_test()
    print('## Test city district ##################################################################')
    city.run_test()
    print('## Test domestic hot water function ##################################################################')
    dhw.run_test()
    print('## Test eletrical demand ##################################################################')
    eld.run_test()
    print('## Test electrical heater ##################################################################')
    elh.run_test()
    print('## Test environment ##################################################################')
    env.run_test()
    print('## Test heating device ##################################################################')
    heatd.run_test()
    print('## Test heatpumpt ##################################################################')
    hp.run_test()
    print('## Test inverter ##################################################################')
    inv.run_test()
    print('## Test photovoltaic ##################################################################')
    pv.run_test()
    print('## Test space heating ##################################################################')
    sph.run_test()
    print('## Test thermal storage system ##################################################################')
    tes.run_test()
    print('## Test timer ##################################################################')
    timer.run_test()
    print('## Test weather ##################################################################')
    weat.run_test()
    print('## Test wind ##################################################################')
    wind.run_test()

if __name__ == '__main__':
    run_all_test()
