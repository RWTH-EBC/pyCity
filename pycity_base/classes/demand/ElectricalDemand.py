#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Electrical demand class
"""

from __future__ import division
import os
import pycity_base.classes.demand.Load
import pycity_base.functions.slp_electrical as slp_el
import pycity_base.functions.changeResolution as cr
import pycity_base.functions.load_el_profiles as eloader
import richardsonpy.classes.electric_load as eload


class ElectricalDemand(pycity_base.classes.demand.Load.Load):
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
                 annualDemand=None, profileType="H0",
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
            (default: None)
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

        if method == 0:
            super(ElectricalDemand, self).__init__(environment, loadcurve)

        #  Use standardized load profiles (SLP)
        elif method == 1:
            if not ElectricalDemand.loaded_slp:
                filename = os.path.join(src_path, 'inputs',
                                        'standard_load_profile',
                                        'slp_electrical.xlsx')
                ElectricalDemand.slp = slp_el.load(filename,
                                                   time_discretization=environment.timer.timeDiscretization)
                ElectricalDemand.loaded_slp = True

            loadcurve = slp_el.get_demand(annualDemand,
                                          ElectricalDemand.slp[profileType],
                                          environment.timer.timeDiscretization)

            super(ElectricalDemand, self).__init__(environment, loadcurve)

        #  Usage of stochastic, el. profile generator for residential buildings
        elif method == 2:

            #  Extract radiation values of weather
            q_direct = environment.weather.qDirect
            q_diffuse = environment.weather.qDiffuse

            #  Extract initial_day
            initial_day = environment.timer.initialDay

            #  Get timestep
            timestep = environment.timer.timeDiscretization

            #  Generate Richadsonpy el. load object instance
            electr_lodad = \
                eload.ElectricLoad(occ_profile=occupancy,
                                   total_nb_occ=total_nb_occupants,
                                   q_direct=q_direct,
                                   q_diffuse=q_diffuse,
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

            # if app_filename is None:   # Use default
            #     pathApps = os.path.join(src_path, 'inputs',
            #                             'stochastic_electrical_load',
            #                             'Appliances.csv')
            # else:  # Use user defined path
            #     pathApps = app_filename
            #
            # if light_filename is None:  # Use default
            #     pathLights = os.path.join(src_path, 'inputs',
            #                               'stochastic_electrical_load',
            #                               'LightBulbs.csv')
            # else:  # Use user defined path
            #     pathLights = light_filename
            #
            # # Initialize appliances and lights
            # if annualDemand == 0:
            #     if singleFamilyHouse:
            #         annualDemand = self.standard_consumption["SFH"][
            #             total_nb_occupants]
            #     else:
            #         annualDemand = self.standard_consumption["MFH"][
            #             total_nb_occupants]
            #
            # # According to http://www.die-stromsparinitiative.de/fileadmin/
            # # bilder/Stromspiegel/Brosch%C3%BCre/Stromspiegel2014web_final.pdf
            # # roughly 9% of the electricity consumption are due to lighting.
            # # This has to be excluded from the appliances' demand:
            # appliancesDemand = 0.91 * annualDemand
            #
            # #  Get appliances
            # self.appliances = app_model.Appliances(pathApps,
            #                                        annual_consumption=appliancesDemand,
            #                                        randomize_appliances=randomizeAppliances,
            #                                        prev_heat_dev=prev_heat_dev)
            #
            # #  Get lighting configuration
            # self.lights = light_model.load_lighting_profile(pathLights,
            #                                                 lightConfiguration)
            #
            # # Create wrapper object
            # timeDis = environment.timer.timeDiscretization
            # timestepsDay = int(86400 / timeDis)
            # day = environment.timer.currentWeekday
            # self.wrapper = wrapper.Electricity_profile(self.appliances,
            #                                            self.lights)
            #
            # # Make full year simulation
            # demand = []
            # light_load = []
            # app_load = []
            #
            # beam = environment.weather.qDirect
            # diffuse = environment.weather.qDiffuse
            # irradiance = beam + diffuse
            # required_timestamp = np.arange(1440)
            # given_timestamp = timeDis * np.arange(timestepsDay)
            #
            # # Loop over all days
            # for i in range(int(len(irradiance) * timeDis / 86400)):
            #     if (i + day) % 7 in (0, 6):
            #         weekend = True
            #     else:
            #         weekend = False
            #
            #     irrad_day = irradiance[
            #                 timestepsDay * i: timestepsDay * (i + 1)]
            #     current_irradiation = np.interp(required_timestamp,
            #                                     given_timestamp, irrad_day)
            #
            #     current_occupancy = occupancy[144 * i: 144 * (i + 1)]
            #
            #     (el_p_curve, light_p_curve, app_p_curve) = \
            #         self.wrapper.demands(current_irradiation,
            #                              weekend,
            #                              i,
            #                              current_occupancy)
            #
            #     demand.append(el_p_curve)
            #     light_load.append(light_p_curve)
            #     app_load.append(app_p_curve)
            #
            # res = np.array(demand)
            # light_load = np.array(light_load)
            # app_load = np.array(app_load)
            #
            # res = np.reshape(res, res.size)
            # light_load = np.reshape(light_load, light_load.size)
            # app_load = np.reshape(app_load, app_load.size)
            #
            # if season_light_mod:
            #     #  Put cosine-wave on lighting over the year to estimate
            #     #  seasonal influence
            #
            #     light_energy = sum(light_load) * 60
            #
            #     time_array = np.arange(start=0, stop=len(app_load))
            #     time_pi_array = time_array * 2 * np.pi / len(app_load)
            #
            #     cos_array = 0.5 * np.cos(time_pi_array) + 0.5
            #
            #     ref_light_power = max(light_load)
            #
            #     light_load_new = np.zeros(len(light_load))
            #
            #     for i in range(len(light_load)):
            #         if light_load[i] == 0:
            #             light_load_new[i] = 0
            #         elif light_load[i] > 0:
            #             light_load_new[i] = light_load[i] + \
            #                                 light_mod_fac * ref_light_power \
            #                                 * cos_array[i]
            #
            #     light_energy_new = sum(light_load_new) * 60
            #
            #     #  Rescale to original lighting energy demand
            #     light_load_new *= light_energy / light_energy_new
            #
            #     res = light_load_new + app_load
            #
            # #  Change time resolution
            # loadcurve = cr.changeResolution(res, 60, timeDis)
            # # light_load = cr.changeResolution(light_load, 60, timeDis)
            # # app_load = cr.changeResolution(app_load, 60, timeDis)
            #
            # #  Normalize el. load profile to annualDemand
            # if do_normalization:
            #     #  Convert power to energy values
            #     energy_curve = loadcurve * timeDis  # in Ws
            #
            #     #  Sum up energy values (plus conversion from Ws to kWh)
            #     curr_el_dem = sum(energy_curve) / (3600 * 1000)
            #
            #     con_factor = annualDemand / curr_el_dem
            #
            #     #  Rescale load curve
            #     loadcurve *= con_factor

            super(ElectricalDemand, self).__init__(environment,
                                                   electr_lodad.loadcurve)

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
