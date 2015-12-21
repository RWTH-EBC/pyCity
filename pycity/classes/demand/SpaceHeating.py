#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 09:12:35 2015

@author: Thomas
"""

from __future__ import division
import os
import numpy as np
import pycity.classes.demand.Load
import pycity.classes.demand.ZoneInputs as zi
import pycity.functions.slp_thermal as slp_th
import pycity.functions.zoneModel


class SpaceHeating(pycity.classes.demand.Load.Load):
    """
    Implementation of the space heating object
    """
    
    loaded_slp = False
    slp_hour = []
    slp_prof = []
    slp_week = []
    
    def __init__(self, environment, method=0,
                 loadcurve=[], 
                 livingArea=0, specificDemand=0, profile_type='HEF',
                 zoneParameters=None, T_m_init=None, ventilation=0,
                 TCoolingSet=200, THeatingSet=-50, occupancy=0,
                 appliances=0, lighting=0):
        """
        Parameters
        ----------
        environment : Environment object
            Common to all other objects. Includes time and weather instances
        method : integer, optional
            - `0` : Provide load curve directly
            - `1` : Use thermal standard load profile
            - `2` : Use ISO 13790 standard to compute thermal load
        loadcurve : Array-like, optional
            Load curve for all investigated time steps
            Requires ``method=0``.
        livingArea : Float, optional
            Living area of the apartment in m2
            Requires ``method=1``
        specificDemand : Float, optional
            Specific thermal demand of the building in kWh/(m2 a)
            Requires ``method=1``
        profile_type : str, optional
            Thermal SLP profile name
            Requires ``method=1``
            - `HEF` : Single family household
            - `HMF` : Multi family household
            - `GBA` : Bakeries
            - `GBD` : Other services
            - `GBH` : Accomodations
            - `GGA` : Restaurants
            - `GGB` : Gardening
            - `GHA` : Retailers
            - `GHD` : Summed load profile business, trade and services
            - `GKO` : Banks, insurances, public institutions
            - `GMF` : Household similar businesses
            - `GMK` : Automotive
            - `GPD` : Paper and printing
            - `GWA` : Laundries
        zoneParameters : ZoneParameters object, optional
            Parameters of the building (floor area, building class, etc.). 
            Requires ``method=2``.
        T_m_init : Float, optional
            Initial temperature of the internal heat capacity.
            Requires ``method=2``.
        ventilation : Array-like, optional
            Ventilation rate in 1/h.
            Requires ``method=2``.
        TCoolingSet : Array-like, optional
            Cooling starts if the room temperature exceeds this value.
            Requires ``method=2``.
        THeatingSet : Array-like, optional
            Heating starts if the room temperature drops below this value.
            Requires ``method=2``.
        occupancy : Array-like, optional
            Full year occupancy profile.
            Requires ``method=2``.
        appliances : Array-like, optional
            Internal gains from electrical appliances in Watt.
            Requires ``method=2``.
        lighting : Array-like, optional
            Internal gains from lighting in Watt.
            Requires ``method=2``.
        
        Info
        ----
        The thermal standard load profile is based on the disseratation of
        Mark Hellwig. 
        "Entwicklung und Anwendung parametrisierter Standard-Lastprofile",
        TU München, Germany, 2003.
        
        URL : http://mediatum.ub.tum.de/doc/601557/601557.pdf
        """
        self.method = method
        
        if method == 0:
            super(SpaceHeating, self).__init__(environment, loadcurve)
        elif method == 1:
            timeDis = environment.timer.timeDiscretization
            if not SpaceHeating.loaded_slp:
                src_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                folder = os.path.join(src_path, 'inputs', 'standard_load_profile')
                f_hour = os.path.join(folder, 'slp_thermal_hourly_factors.xlsx')
                f_prof = os.path.join(folder, 'slp_thermal_profile_factors.xlsx')
                f_week = os.path.join(folder, 'slp_thermal_week_day_factors.xlsx')
                SpaceHeating.slp_hour = slp_th.load_hourly_factors(f_hour,
                                                                   timeDis)
                SpaceHeating.slp_prof = slp_th.load_profile_factors(f_prof)
                SpaceHeating.slp_week = slp_th.load_week_day_factors(f_week)
                                
                SpaceHeating.loaded_slp = True
            
            annual_demand = livingArea * specificDemand # kWh
            profile = 3
    
            fun = slp_th.calculate
            loadcurve = fun(environment.weather.tAmbient,
                            environment.timer.currentDay,
                            SpaceHeating.slp_prof[profile_type][profile],
                            SpaceHeating.slp_week[profile_type],
                            SpaceHeating.slp_hour[profile_type],
                            annual_demand)
            
            super(SpaceHeating, self).__init__(environment, loadcurve)
            
        elif method == 2:
            self.zoneParameters = zoneParameters
            # Create zoneInputs (this already creates the full year inputs!)
            self.zoneInputs = zi.ZoneInputs(environment,
                                            zoneParameters,
                                            T_m_init,
                                            ventilation=ventilation,
                                            occupancy=occupancy,
                                            appliances=appliances,
                                            lighting=lighting)
            
            calc = pycity.functions.zoneModel.calc
            res = calc(zoneParameters=self.zoneParameters,
                           zoneInputs=self.zoneInputs, 
                           TCoolingSet=TCoolingSet,
                           THeatingSet=THeatingSet,
                           limitHeating=np.inf, 
                           limitCooling=-np.inf, 
                           beQuiet=True)
            
            self.loadcurve = res[0]
            self.T_op = res[1]
            self.T_m = res[2]
            self.T_i = res[3]
            self.T_s = res[4]
            
        self._kind = "spaceheating"
        
    def getDemand(self, currentValues=True):
        """
        """
        if self.method in (0, 1, 2):
            return self._getLoadcurve(currentValues)
#        elif self.method == 2:
#            if currentValues:
#                self.zoneInputs.update(occupancy, appliances, lighting)
#                calc = pycity.functions.zoneModel.calc
#                res = calc(zoneParameters=self.zoneParameters,
#                           zoneInputs=self.zoneInputs, 
#                           TCoolingSet=TCoolingSet,
#                           THeatingSet=THeatingSet,
#                           limitHeating=np.inf, 
#                           limitCooling=-np.inf, 
#                           beQuiet=True)
#            return res[0]
