#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 21:22:29 2015

@author: tsz

Inputs:
A_f (section 6.4) - used area in m^2
"""

from __future__ import division

import numpy as np
import math


class ZoneParameters(object):
    """
    This class holds all relevant parameters of a single zone as described in
    DIN EN ISO 13790:2008 (German version of ISO 13790:2008).
    
    This class also provides a function to compute the resistance 
    corresponding to ventilation.
    """
    
    def __init__(self, 
                 A_f=0, 
                 A_w=[], 
                 U_w=[],
                 g_gln=[],
                 epsilon_w=[],
                 R_se_w=0.04,
                 A_op=[],
                 U_op=[],
                 alpha_Sc=[],
                 R_se_op=0.04,
                 epsilon_op=0,
                 V=0,
                 sampling_rate=3600,
                 building_class=0,
                 kappa_j=[], 
                 A_j=[], 
                 simplified_capacity=True,
                 albedo=0.2,
                 gamma=[0, 90, 180, 270, 0, 0],
                 beta=[90, 90, 90, 90, 0, 0]):
        """
        Set up a thermal zone as required for calculations according to 
        DIN EN ISO 13790:2008 (German version of ISO 13790:2008).
        
        Simplifications
        ---------------
        Glazings : Windows, doors
            DIN EN ISO 13790, section 11.3.2, equation 43, page 67. Neglecting 
            the shading factor (F_sh,ob,k=1).

            DIN EN ISO 13790, section 11.3.3, equation 44, page 67. Neglecting
            the shading factor (F_sh,gl=1). Neglecting borders (F_F=0).
            Consequently, A_w,p is assumed to be A_w (see parameters). In this
            manner, the number of parameters is largely reduced.
            
            DIN EN ISO 13790, section 11.4.2, equation 47, page 70. Usage of 
            the simplified, averaged solar energy transmittance (reduction
            of required parameters).
            
        Opaque components : Walls, roofs
            DIN EN ISO 13790, section 11.3.4, equation 45, page 68. U_c and A_c
            are assumed to be equal to U_op and W_op (see parameters).
            
        Index-convention for parameters
        -------------------------------
        - 0 : South
        - 1 : West
        - 2 : North
        - 3 : East
        - 4 : Roof / Ceiling
        - 5 : Floor
        This convention is derived from the definition of the surface azimuth 
        angles. See Duffie and Beckman: Solar Engineering of Thermal Processes
        (4th ed.), section 1.6, page 13. If a surface for example does not 
        contain any windows, enter 0 in this entry.
        
        Parameters
        ----------
        A_f : float
            Used floor area in m^2 (cf. DIN EN ISO 13790, section 6.4, page 30)
        A_w : array-like
            Surface area of each window-like component (window, door,...) in m^2
        U_w : array-like
            U-values for each window-like component (window, door,...) in W/m^2K
        g_gln : float or array-like
            Energy transmittance of window-like components (without unit).
            See DIN EN ISO 13790, section 11.4.2, page 70.
            The fifth entry (floor) is typically 0, since the sun does not 
            directly affect the floor.
        epsilon_w : float or array-like
            Emissivity of window-like components.
            See DIN EN ISO 13790, section 11.3.4, page 73, equation 51
        R_se_w : float or array-like
            Surface thermal resistance of window-like components.
            See DIN EN ISO 13790, section 11.3.4, page 68 or ISO 6946
        A_op : array-like
            Surface area of each opaque component (walls, roof) in m^2
        U_op : array-like
            U-values for each opaque component (walls, roof) in W/m^2K
        alpha_Sc : array-like
            Attenuation coefficient for each opaque component, without unit.
            The fifth entry (floor) is typically 0, since the sun does not 
            directly affect the floor.
        R_se_op : float or array-like
            Surface thermal resistance of opaque components.
            See DIN EN ISO 13790, section 11.3.4, page 68 or ISO 6946
        epsilon_op : float or array-like
            Emissivity of opaque components.
            See DIN EN ISO 13790, section 11.3.4, page 73, equation 51
        V : float
            Zone's volume in m3
        sampling_rate : integer, optional
            Sampling rate required for the computation and converting the 
            ventilation profile
        building_class : integer, optional
            - 0: very light
            - 1: light
            - 2: medium
            - 3: heavy
            - 4: very heavy
            Optional. Only used if ``simplified_capacity==True``
        kappa_j : array-like, optional
            Heat capacity of each component that is in contact with the indoor
            air in J/m^2K. Optional. Only used if ``simplified_capacity==False``
        A_j : array-like, optional
            Surface area of each component that is in contact with the indoor 
            air in m^2. Optional. Only used if ``simplified_capacity==False``
        simplified_capacity : boolean, optional
            - ``True``: Simplified computation of effective area and capacity
            - ``False``: Detailed computation of effective area and capacity
        albedo : float, optional
            Average reflectivity of the ground.
            Typical values are between 0.2 and 0.3.
        gamma : array-like, optional
            Surface azimuth angle, according to the index convention. 
            0 represents Southern orientation and 90 Western orientation.
        beta : array-like, optional
            Slope angle. 0 stands for horizontal surfaces and 90 for vertical.
        """
        self._kind = "zoneparameters"

        # Note: We are not consequently using CamelCase in this function, 
        # because many variables introduced in ISO 13790 have short indices,
        # which makes CamelCase not harder to read.
        
        # Note: If not stated differently, all equations, pages and sections
        # refer to DIN EN ISO 13790:2008 (the official German version of 
        # ISO 13790:2008).

        # Save sampling rate
        self.sampling_rate = sampling_rate
        
        # Compute A_t and H_tr_is
        # Equation 9, section 7.2.2.2 (pages 35, 36)
        h_is = 3.45                     # m^2, section 7.2.2.2, page 35
        lambda_at = 4.5                 # section 7.2.2.2, page 36
        self.A_t = A_f * lambda_at      # m^2
        self.H_tr_is = self.A_t * h_is  # W/K
        
        # Compute C_m and A_m
        # Equations 65 and 66, resp. table 12 if the simplified method is used
        # Pages 79-81, sections 12.2.2 and 12.3.1
        if simplified_capacity:
            # Table 12, section 12.3.1.2, page 81
            if building_class == 0:
                self.A_m = 2.5 * A_f
                self.C_m = 80000 * A_f
            elif building_class == 1:
                self.A_m = 2.5 * A_f
                self.C_m = 11000 * A_f
            elif building_class == 2:
                self.A_m = 2.5 * A_f
                self.C_m = 165000 * A_f
            elif building_class == 3:
                self.A_m = 3 * A_f
                self.C_m = 260000 * A_f
            else:
                self.A_m = 3.5 * A_f
                self.C_m = 370000 * A_f
        else:
            # Equations 65 and 66, sections 12.2.2 and 12.3.1.1., pages 79, 80
            kappa_j = np.array(kappa_j)
            A_j = np.array(A_j)
            self.C_m = np.sum(kappa_j * A_j)
            self.A_m = math.pow(self.C_m, 2) / np.sum(A_j * np.power(kappa_j, 2))
        
        # Compute heat transmission through windows (also doors, glazed walls,
        # curtain walls...)
        # DIN EN ISO 13790:2008, equation 18, section 8.3.1, page 44
        # Point- and line-based heat transfer is neglected to simplify the 
        # parametrization (l_k, Psi_k, chi_j = 0)
        # As only one thermal zone is considered, b_tr_x = 1
        self.A_windows = np.array(A_w)
        self.U_windows = np.array(U_w)
        self.H_tr_w = np.sum(self.A_windows * self.U_windows)
        
        # Save effective area and radiative heat losses to the sky of window-
        # like components.
        # DIN EN ISO 13790:2008, section 11.4.2, equation 47
        F_w = 0.9  # without unit
        g_gln = np.array(g_gln)
        self.g_gl = F_w * g_gln
        # DIN EN ISO 13790:2008, section 11.3.2, equation 44
        F_sh_gl = 1.0
        F_F = 0
        self.A_windows_sol = F_sh_gl * self.g_gl * (1 - F_F) * self.A_windows
        # Simplification of external radiative heat exchange coefficient
        # Slightly below DIN EN ISO 13790, section 11.4.6, equation 51, page 73
        epsilon_w = np.array(epsilon_w)
        h_r_windows = 5 * epsilon_w
        # Simplification of average difference between ambient air temperature
        # and sky's temperature.
        # Slightly below DIN EN ISO 13790, section 11.4.6, equation 51, page 73
        Delta_theta_er = 11  # K
        # DIN EN ISO 13790, section 11.3.5, equation 46, page 69
        R_se_op = np.array(R_se_op)
        self.Psi_r_windows = (R_se_w * self.U_windows * self.A_windows * h_r_windows * Delta_theta_er)
        
        # H_tr_ms, based on equation 64, section 12.2.2, page 79
        h_ms = 9.1                      # W/m^2K, section 12.2.2, page 79
        self.H_tr_ms = h_ms * self.A_m  # W/K

        # Compute heat transmission through opaque parts (walls, roof)
        # Compute total heat transmission through opaque parts
        # Same source as for heat transmissions through windows and same 
        # simplifications (no 0-dimensional and 1-dimensional heat transfer)
        self.A_opaque = np.array(A_op)
        self.U_opaque = np.array(U_op)
        
        if len(self.U_opaque.shape) > 1:
            self.H_tr_op = np.zeros(self.U_opaque.shape[0])
            self.H_tr_em = np.zeros(self.U_opaque.shape[0])
        
            for i in range(len(self.H_tr_op)):
                self.H_tr_op[i] = np.sum(self.A_opaque * self.U_opaque[i, :])
                # H_tr_em, based on equation 63, section 12.2.2, page 79
                self.H_tr_em[i] = 1 / (1 / self.H_tr_op[i] - 1 / self.H_tr_ms)
        else:
            self.H_tr_op = np.sum(self.A_opaque * self.U_opaque)
            self.H_tr_em = 1 / (1 / self.H_tr_op - 1 / self.H_tr_ms)

        # Save effective area and radiative heat losses to the sky of opaque 
        # components.
        # DIN EN ISO 13790:2008, section 11.4.2, equation 45, page 68
        alpha_Sc = np.array(alpha_Sc)
        R_se_op = np.array(R_se_op)
        
        # Simplification of external radiative heat exchange coefficient
        # Slightly below DIN EN ISO 13790, section 11.4.6, equation 51, page 73
        epsilon_op = np.array(epsilon_op)
        h_r_opaque = 5 * epsilon_op
        
        if len(self.U_opaque.shape) > 1:
            self.A_opaque_sol = alpha_Sc * R_se_op * self.U_opaque[0] * self.A_opaque
            # DIN EN ISO 13790, section 11.3.5, equation 46, page 69
            self.Psi_r_opaque = (R_se_op * self.U_opaque[0] * self.A_opaque
                               * h_r_opaque * Delta_theta_er)
        else:
            self.A_opaque_sol = alpha_Sc * R_se_op * self.U_opaque * self.A_opaque
            # DIN EN ISO 13790, section 11.3.5, equation 46, page 69
            self.Psi_r_opaque = (R_se_op * self.U_opaque * self.A_opaque * h_r_opaque * Delta_theta_er)
        
        # H_tr_em, based on equation 63, section 12.2.2, page 79
        # self.H_tr_em = 1 / (1 / self.H_tr_op - 1 / self.H_tr_ms)
        
        # Save zone's volume for later computing the ventilation
        # As ventilation is a dynamic effect, a scalar heat transfer 
        # coefficient is insufficient. Instead a vector/array will be computed
        self.V = V
        
        # Initialize ventilation
        ventilationRate = np.zeros(int(8760 / 3600 * sampling_rate))
        self.updateVentilation(ventilationRate)
        
        # Save Albedo
        self.albedo = albedo
        
        # Save beta and gamma
        self.beta = beta
        self.gamma = gamma
        
        # Compute interaction between outside surfaces (indexes 0-4) and sky
        # 0.5 describes vertical walls and 1 horizontal roofs 
        # (see DIN EN ISO 13790:2008, section 11.4.6, page 73)
        self.F_r = [0.5 if beta[i] > 0 else 1 for i in range(5)]

    @property
    def kind(self):
        return self._kind

    def updateVentilation(self, 
                          ventilationRate, 
                          ventilationRateMinimum=0.5):
        """
        Compute the heat transfer due to ventilation for the given
        ventilationRate.
        
        ventilationRate : array-like
            Infiltration due to window opening, etc.
        ventilationRateMinimum : float, optional
            Minimum air exchange rate.
        """
        
        ventilationRate = np.maximum(ventilationRate, ventilationRateMinimum)

        rhoAir = 1.2  # kg/m^3
        cPAir = 1000  # J/kgK
        
        # Confirm DIN EN ISO 13789:2008-04, page 11, section 5, equation 4.
        self.H_ve = (rhoAir * cPAir * ventilationRate * 
                     self.V / self.sampling_rate)
