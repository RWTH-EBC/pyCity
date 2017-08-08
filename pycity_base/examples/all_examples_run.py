"""
Script executes example files in examples folder
(except ASHRAE140 validation)
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


def run_all_examples():
    """
    Function execute examples within example folder
    """
    print('## Example: solar radiation on tilted surface ####################')
    sol.run_example()
    print('## Example: apartment ############################################')
    ap.run_test()
    print('## Example: battery ##############################################')
    batt.run_test()
    print('## Example: building energy system (BES) #########################')
    bes.run_test()
    print('## Example: boiler ###############################################')
    boil.run_test()
    print('## Example: building #############################################')
    build.run_test()
    print('## Example: chp ##################################################')
    chp.run_test()
    print('## Example: city district ########################################')
    city.run_test()
    print('## Example: domestic hot water function ##########################')
    dhw.run_test()
    print('## Example: electrical demand ####################################')
    eld.run_test()
    print('## Example: electrical heater ####################################')
    elh.run_test()
    print('## Example: environment ##########################################')
    env.run_test()
    print('## Example: heating device #######################################')
    heatd.run_test()
    print('## Example: heatpumpt ############################################')
    hp.run_test()
    print('## Example: inverter #############################################')
    inv.run_test()
    print('## Example: occupancy ############################################')
    occ.exampe_occupancy()
    print('## Example: photovoltaic #########################################')
    pv.run_test()
    print('## Example: space heating ########################################')
    sph.run_test()
    print('## Example: thermal storage system ###############################')
    tes.run_test()
    print('## Example: timer ################################################')
    timer.run_test()
    print('## Example: weather ##############################################')
    weat.run_test()
    print('## Example: wind #################################################')
    wind.run_test()

if __name__ == '__main__':
    run_all_examples()
