#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Electrical demand class
"""

from __future__ import division
import os

import pycity.classes.demand.Load
import pycity.functions.slp_electrical as slp_el
import pycity.functions.changeResolution as cr
import pycity.functions.load_el_profiles as eloader

import richardsonpy.classes.electric_load as eload


class ElectricalDemand(pycity.classes.demand.Load.Load):
    """
    Implementation of the electrical demand object
    """

    loaded_slp = False
    slp = []

    loaded_weekly_data = False
    weekly_data = None

    load_ann_data = False
    ann_data = None

    standard_consumption = {"SFH": {1: 2700,
                                    2: 3200,
                                    3: 4000,
                                    4: 4400,
                                    5: 5500},
                            "MFH": {1: 1500,
                                    2: 2200,
                                    3: 3000,
                                    4: 3400,
                                    5: 4100}}

    def __init__(self,
                 environment,
                 method=0,
                 loadcurve=[],
                 annualDemand=0, profileType="H0",
                 singleFamilyHouse=True, total_nb_occupants=0,
                 randomizeAppliances=True, lightConfiguration=0, occupancy=[],
                 do_normalization=False, method_3_type=None,
                 method_4_type=None, prev_heat_dev=False, app_filename=None,
                 light_filename=None, season_light_mod=False,
                 light_mod_fac=0.25):
        """
        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        method : Integer, optional
            - `0` : Provide load curve directly (for all timesteps!)
            - `1` : Standard load profile
            - `2` : Stochastic electrical load model (only residential)
            - `3` : Annual profile based on measured weekly profiles
                    (non-residential)
            - `4` : Annual profile based on measured annual profiles
                    (non-residential)
        loadcurve : Array-like, optional
            Load curve for all investigated time steps
        annualDemand : Float (required for SLP and recommended for method 2)
            Annual electrical demand in kWh.
            If method 2 is chosen but no value is given, a standard value for
            Germany (http://www.die-stromsparinitiative.de/fileadmin/bilder/
            Stromspiegel/Brosch%C3%BCre/Stromspiegel2014web_final.pdf) is used.
        profileType : String (required for SLP; method=1)
            - H0 : Household
            - L0 : Farms
            - L1 : Farms with breeding / cattle
            - L2 : Farms without cattle
            - G0 : Business (general)
            - G1 : Business (workingdays 8:00 AM - 6:00 PM)
            - G2 : Business with high loads in the evening
            - G3 : Business (24 hours)
            - G4 : Shops / Barbers
            - G5 : Bakery
            - G6 : Weekend operation
        total_nb_occupants : int, optional (used in method 2)
            Number of people living in the household.
        randomizeAppliances : Boolean (only required in method 2)
            - True : Distribute installed appliances randomly
            - False : Use the standard distribution
        lightConfiguration : Integer (only optional in method 2)
            There are 100 light bulb configurations predefined for the
            Stochastic model. Select one by entering an integer in [0, ..., 99]
        occupancy : Array-like (optional, but recommended in method 2)
            Occupancy given at 10-minute intervals for a full year
        do_normalization : bool, optional
            Defines, if stochastic profile (method=2) should be
            normalized to given annualDemand value (default: False).
            If set to False, annual el. demand depends on stochastic el. load
            profile generation. If set to True, does normalization with
            annualDemand
        method_3_type : str, optional
            Defines type of profile for method=3 (default: None)
            Options:
            - 'food_pro': Food production
            - 'metal': Metal company
            - 'rest': Restaurant (with large cooling load)
            - 'sports': Sports hall
            - 'repair': Repair / metal shop
        method_4_type : str, optional
            Defines type of profile for method=4 (default: None)
            - 'metal_1' : Metal company with smooth profile
            - 'metal_2' : Metal company with fluctuation in profile
            - 'warehouse' : Warehouse
        prev_heat_dev : bool, optional
            Defines, if heating devices should be prevented within chosen
            appliances (default: False). If set to True, DESWH, E-INST,
            Electric shower, Storage heaters and Other electric space heating
            are set to zero. Only relevant for method == 2
        app_filename : str, optional
            Path to Appliances file
            (default: None). If set to None, uses default file Appliances.csv
            in \inputs\stochastic_electrical_load\.
            Only relevant, if method == 2.
        light_filename : str, optional
            Path to Lighting configuration file
            (default: None). If set to None, uses default file Appliances.csv
            in \inputs\stochastic_electrical_load\.
            Only relevant, if method == 2.
        season_light_mod : bool, optional
            Defines, if cosine-wave should be used to strengthen seasonal
            influence on lighting (default: False). If True, enlarges
            lighting power demand in winter month and reduces lighting power
            demand in summer month
        light_mod_fac : float, optional
            Define factor, related to maximal lighting power, which is used
            to implement seasonal influence (default: 0.25). Only relevant,
            if season_light_mod == True

        Info
        ----
        The standard load profile can be downloaded here:
        http://www.ewe-netz.de/strom/1988.php

        Average German electricity consumption per household can be found here:
        http://www.die-stromsparinitiative.de/fileadmin/bilder/Stromspiegel/
        Brosch%C3%BCre/Stromspiegel2014web_final.pdf
        """
        src_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

        self.eload_obj = None  # El. load object of richardsonpy

        if method == 0:
            super(ElectricalDemand, self).__init__(environment, loadcurve)

        #  Use standardized load profiles (SLP)
        elif method == 1:
            if not ElectricalDemand.loaded_slp:
                filename = os.path.join(src_path, 'inputs',
                                        'standard_load_profile',
                                        'slp_electrical.xlsx')
                ElectricalDemand.slp = \
                    slp_el.load(filename,
                                time_discretization=environment.timer.timeDiscretization)
                ElectricalDemand.loaded_slp = True

            loadcurve = slp_el.get_demand(annualDemand,
                                          ElectricalDemand.slp[profileType],
                                          environment.timer.timeDiscretization)

            super(ElectricalDemand, self).__init__(environment, loadcurve)

        #  Usage of stochastic, el. profile generator for residential buildings
        elif method == 2:

            q_dir = environment.weather.qDirect
            q_diff = environment.weather.qDiffuse
            timestep = environment.timer.timeDiscretization
            initial_day = environment.timer.currentWeekday

            #  Generate electric load object of richardsonpy
            self.eload_obj = \
                eload.ElectricLoad(occ_profile=occupancy,
                                   total_nb_occ=total_nb_occupants,
                                   q_direct=q_dir,
                                   q_diffuse=q_diff,
                                   annual_demand=annualDemand,
                                   is_sfh=singleFamilyHouse,
                                   path_app=app_filename,
                                   path_light=light_filename,
                                   randomize_appliances=randomizeAppliances,
                                   prev_heat_dev=prev_heat_dev,
                                   light_config=lightConfiguration,
                                   timestep=timestep,
                                   initial_day=initial_day,
                                   season_light_mod=season_light_mod,
                                   light_mod_fac=light_mod_fac,
                                   do_normalization=do_normalization,
                                   calc_profile=True,
                                   save_app_light=False)

            #  Pointer to loadcurve of richardsonpy el. load object
            loadcurve = self.eload_obj.loadcurve

            super(ElectricalDemand, self).__init__(environment, loadcurve)

        #  Generate el. load based on measured, weekly profile
        elif method == 3:

            assert type is not None, 'You need to define a valid type for method 3!'
            assert annualDemand > 0, 'annualDemand has to be larger than 0!'

            if not ElectricalDemand.loaded_weekly_data:
                fpath = os.path.join(src_path, 'inputs',
                                     'measured_el_loads',
                                     'Non_res_weekly_el_profiles.txt')
                ElectricalDemand.weekly_data = \
                    eloader.load_non_res_load_data_weekly(fpath)
                ElectricalDemand.loaded_weekly_data = True

            loadcurve = eloader.gen_annual_el_load(
                ElectricalDemand.weekly_data,
                type=method_3_type,
                start_wd=environment.timer.currentWeekday,
                annual_demand=annualDemand)

            loadcurve = cr.changeResolution(loadcurve,
                                            oldResolution=900,
                                            newResolution=
                                            environment.timer.timeDiscretization)

            super(ElectricalDemand, self).__init__(environment, loadcurve)

        #  Generate el. load based on measured, annual profiles
        elif method == 4:

            assert type is not None, 'You need to define a valid type for method 4!'
            assert annualDemand > 0, 'annualDemand has to be larger than 0!'

            if not ElectricalDemand.load_ann_data:
                fpath = os.path.join(src_path, 'inputs',
                                     'measured_el_loads',
                                     'non_res_annual_el_profiles.txt')
                ElectricalDemand.ann_data = \
                    eloader.load_non_res_load_data_annual(fpath)
                ElectricalDemand.load_ann_data = True

            loadcurve = eloader.get_annual_el_load(
                ElectricalDemand.ann_data,
                type=method_4_type,
                annual_demand=annualDemand)

            loadcurve = cr.changeResolution(loadcurve,
                                            oldResolution=900,
                                            newResolution=
                                            environment.timer.timeDiscretization)

            super(ElectricalDemand, self).__init__(environment, loadcurve)

        self._kind = "electricaldemand"
        self.method = method

    def get_power(self, currentValues=True):
        """
        Return electrical power curve

        Parameters
        ----------
        currentValues : bool, optional
            Return only current values (True) or the entire load (False)
            (default: True)

        Return
        ------
        loadcurve : np.array
            Electrical power curve
        """
        if self.method in (0, 1, 2, 3, 4):
            return self._getLoadcurve(currentValues)
