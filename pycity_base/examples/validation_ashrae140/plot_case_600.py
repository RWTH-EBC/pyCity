#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 22:40:02 2015

@author: tsz
"""

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

# Table B8.1 (Excel: Tables 1) - MWh
annualHeatingLoad = np.array([4.296, 4.773, 5.709, 5.226, 5.596, 4.882, 4.872, 5.362])

# Table B8.2 (Excel: Tables 1) - MWh
annualCoolingLoad = np.array([6.137, 6.433, 7.079, 7.278, 7.964, 6.492, 6.492, 6.778])

# Table B8.3 (Excel: Tables 2) - kW
peakHeatingLoad = np.array([3.437, 3.940, 4.045, 4.258, 4.037, 3.931, 4.354])

# Table B8.4 (Excel: Tables 2) - kW
peakCoolingLoad = np.array([6.194, 5.965, 6.656, 6.827, 6.286, 6.486, 6.812])

loadsYErr = [[np.mean(annualHeatingLoad) - np.min(annualHeatingLoad), 
              np.mean(annualCoolingLoad) - np.min(annualCoolingLoad), 
              np.mean(peakHeatingLoad) - np.min(peakHeatingLoad), 
              np.mean(peakCoolingLoad) - np.min(peakCoolingLoad)],
             [np.max(annualHeatingLoad) - np.mean(annualHeatingLoad), 
              np.max(annualCoolingLoad) - np.mean(annualCoolingLoad), 
              np.max(peakHeatingLoad) - np.mean(peakHeatingLoad), 
              np.max(peakCoolingLoad) - np.mean(peakCoolingLoad)]]
loads = [np.mean(annualHeatingLoad), 
         np.mean(annualCoolingLoad), 
         np.mean(peakHeatingLoad), 
         np.mean(peakCoolingLoad)]

# Table B8.13 (Excel: Tables 6) - kWh/m^2a
solarRadiationNorth = np.array([427, 434, 456, 407, 457, 367, 453])
solarRadiationEast  = np.array([959, 1155, 1083, 1217, 1082, 1101, 962])
solarRadiationWest  = np.array([1086, 1079, 1003, 857, 1002, 1012, 1090])
solarRadiationSouth = np.array([1456, 1566, 1476, 1468, 1474, 1522, 1468])
solarRadiationHorizontal = np.array([1797, 1831, 1832, 1832, 1832, 1832, 1832])

# Table B8.14 (Excel: Tables 6) - kWh/m^2a
solarRadiationWindowSouth = np.array([946, 1051, 962, 954, 926, 984, 914])

# HOURLY HEATING & COOLING LOAD DATA
# CASE 600 JAN 4
# Data extracted from RESULTS5-2.xls, sheet "data for charts", cells B687-I710
# all values in kWh
ESP_jan4 = [3.25, 3.409, 3.392, 3.381, 3.417, 3.432, 3.421, 3.337, 2.767, 
            1.497, 0.151, -0.771, -2.66, -3.575, -3.527, -2.435, -0.356, 
            0.243, 1.53, 2.321, 2.641, 2.899, 3.017, 3.008]

BLAST_jan4 = [3.801823, 3.910936, 3.865797, 3.919602, 3.940134, 3.925815, 
              3.936957, 3.702264, 2.675222, 1.383322, 0, -1.225471, -2.487117, 
              -2.957941, -2.631008, -1.34913, 0, 0.9501685, 2.377919, 
              2.866487, 3.212612, 3.284511, 3.330747, 3.387975]

DOE21D_jan4 = [3.926, 4.035, 4.013, 4.041, 4.045, 4.036, 4.045, 3.857, 2.559, 
               0.843, 0, -1.552, -2.854, -3.398, -3.116, -1.82, 0, 0.775, 
               2.232, 2.933, 3.323, 3.487, 3.514, 3.561]

SRES_SUN_jan4 = [4.127, 4.258, 4.229, 4.22, 4.22, 4.221, 4.222, 4.09, 2.902, 
                 1.275, 0, -1.066, -2.586, -3.225, -2.826, -1.552, -0.001, 
                 0.8, 2.34, 2.988, 3.365, 3.532, 3.605, 3.663]

# No data for SRES 

S3PAS_jan4 = [3.925, 4.037, 4.003, 4.001, 4.001, 4.001, 4.001, 3.898, 2.706, 
              1.151, 0, -1.036, -2.498, -3.085, -2.637, -1.345, 0, 0.88, 
              2.331, 2.949, 3.309, 3.347, 3.494, 3.527]

TRNSYS_jan4 = [3.767, 3.867, 3.903, 3.894, 3.917, 3.931, 3.931, 3.753, 2.423, 
               0.797, -0.035, -1.435, -2.720, -3.156, -2.844, -1.716, 0, 
               0.773, 2.301, 2.967, 3.278, 3.461, 3.5, 3.472]

TASE_jan4 = [4.225, 4.354, 4.321, 4.308, 4.303, 4.307, 4.307, 4.167, 2.912, 
             1.466, 0, -0.424, -2.364, -2.759, -2.431, -1.14, 0, 1.292, 2.445, 
             2.941, 3.405, 3.594, 3.696, 3.769]
             
ref_jan4 = np.vstack((ESP_jan4, BLAST_jan4, DOE21D_jan4, SRES_SUN_jan4, 
                      S3PAS_jan4, TRNSYS_jan4, TASE_jan4))

#HOURLY INCIDENT SOLAR RADIATION, CLEAR DAY, JULY 27
#CASE 600
#WEST SURFACE
# Data extracted from RESULTS5-2.xls, sheet "data for charts", cells B483-I506
# all values in Wh/m^2
ESP_jul27_west = [0, 0, 0, 0, 0.4, 17.9, 58.5, 91.8, 113.7, 131.2, 145.7, 153.8, 
            267.7, 464.8, 635.1, 738.3, 623.9, 296.9, 68.8, 1.6, 0, 0, 0, 0]

# no data for BLAST

DOE21D_jul27_west = [0, 0, 0, 0, 0, 19.96, 65.86, 97.11, 116.89, 128.97, 138.05, 
               141.34, 243.51, 462.83, 664.62, 786.35, 649.05, 243.11, 43.19, 
               0, 0, 0, 0, 0]

SRES_SUN_jul27_west = [0, 0, 0, 0, 0.1667, 27.8275, 77.3025, 99.989, 120.051, 
                 134.9631, 149.5847, 153.134, 266.449, 461.2772, 635.5103, 
                 719.323, 502.7889, 141.2425, 25.2472, 0, 0, 0, 0, 0]

SRES_jul27_west = [0, 0, 0, 0, 0.14, 29.94, 89.2, 112.85, 121.41, 123.51, 125.06, 
             121.07, 117.94, 333.68, 525.35, 634.59, 478.44, 140.3, 21.96, 
             0, 0, 0, 0, 0]

S3PAS_jul27_west = [0, 0, 0, 0, 0, 28, 80, 104, 125, 140, 154, 157, 270, 463, 635, 
              715, 497, 139, 24, 0, 0, 0, 0, 0]

TRNSYS_jul27_west = [0, 0, 0, 0, 0.17, 27.01, 63, 71.22, 85.58, 98.03, 109.14, 
               113.06, 235.17, 453.89, 652.5, 762.78, 568.33, 158, 26.6, 
               0, 0, 0, 0, 0]

TASE_jul27_west = [0, 0, 0, 0, 0.2, 25.7, 62.1, 72, 92.6, 112.8, 136.75, 150.9, 
             382.5, 576.81, 744.52, 807.29, 541.68, 145.25, 24.9, 0, 0, 
             0, 0, 0]
             
ref_jul27_west = np.vstack((ESP_jul27_west, DOE21D_jul27_west, 
                            SRES_SUN_jul27_west, SRES_jul27_west,
                            S3PAS_jul27_west, TRNSYS_jul27_west,
                            TASE_jul27_west))

#HOURLY INCIDENT SOLAR RADIATION, CLEAR DAY, JULY 27
#CASE 600
#SOUTH SURFACE
# Data extracted from RESULTS5-2.xls, sheet "data for charts", cells B442-I465
# all values in Wh/m^2
ESP_jul27_south = [0, 0, 0, 0, 0.5, 17.9, 58.6, 100.4, 205.9, 326, 415.1, 
                   454.8, 455.6, 408.6, 321.2, 200.6, 102.3, 78.8, 37.1, 
                   1.1, 0, 0, 0, 0]

# no data for BLAST

DOE21D_jul27_south = [0, 0, 0, 0, 0, 20.11, 70.22, 108.13, 219.58, 343.67, 
                      435.54, 475.37, 488.49, 443.66, 367.07, 246.71, 119.19, 
                      68.86, 19.75, 0, 0, 0, 0, 0]

SRES_SUN_jul27_south = [0, 0, 0, 0, 0.167, 27.8275, 77.3025, 99.9892, 211.006, 
                        331.006, 418.1717, 454.9942, 464.5689, 413.6364, 
                        334.284, 211.9439, 111.7408, 73.07917, 17.7025, 
                        0, 0, 0, 0, 0]

SRES_jul27_south = [0, 0, 0, 0, 0.14, 29.94, 89.2, 112.85, 164.86, 291.84, 
                    389.26, 437.2, 455.75, 413.67, 341.53, 223.71, 105.72, 
                    68.47, 14.35, 0, 0, 0, 0, 0]

S3PAS_jul27_south = [0, 0, 0, 0, 0, 28, 80, 104, 217, 336, 423, 459, 469, 
                     418, 340, 218, 115, 74, 18, 0, 0, 0, 0, 0]

TRNSYS_jul27_south = [0, 0, 0, 0, 0.17, 27.01, 63, 71.22, 187.72, 314.17, 
                      404.44, 443.61, 452.5, 400.56, 316.94, 188.89, 86.03, 
                      69.78, 17.61, 0, 0, 0, 0, 0]

TASE_jul27_south = [0, 0, 0, 0, 0.2, 25.7, 62.1, 107.47, 232.33, 349.16, 
                    430.22, 459.85, 462.28, 404.57, 319.26, 193.61, 132.3, 
                    76.6, 18.05, 0, 0, 0, 0, 0]
                    
ref_jul27_south = np.vstack((ESP_jul27_south, DOE21D_jul27_south, 
                             SRES_SUN_jul27_south, SRES_jul27_south,
                             S3PAS_jul27_south, TRNSYS_jul27_south,
                             TASE_jul27_south))


#HOURLY INCIDENT SOLAR RADIATION CLOUDY DAY, MARCH 5
#CASE 600
#WEST SURFACE
# Data extracted from RESULTS5-2.xls, sheet "data for charts", cells B401-I424
# all values in Wh/m^2
ESP_mar5_west = [0, 0, 0, 0, 0, 0, 1.6, 13.5, 31, 47.1, 59.7, 67.4, 70.1, 
                 67.3, 58.9, 44.9, 27.6, 9, 0, 0, 0, 0, 0, 0]

# no data for BLAST

DOE21D_mar5_west = [0, 0, 0, 0, 0, 0, 1.8, 13.92, 31.75, 45.24, 56.63, 
                    61.58, 63.7, 61.46, 51.67, 37.2, 16.72, 2.52, 0, 0, 
                    0, 0, 0, 0]

SRES_SUN_mar5_west = [0, 0, 0, 0, 0, 0, 2.997, 20.183, 37.955, 53.244, 64.467, 
                      69.982, 70.806, 65.663, 54.921, 39.487, 21.291, 3.27, 
                      0, 0, 0, 0, 0, 0]

SRES_mar5_west = [0, 0, 0, 0, 0, 0, 3, 20.24, 38.01, 53.27, 53.37, 57.91, 
                  58.3, 54.15, 45.38, 32.7, 17.7, 2.73, 0, 0, 0, 0, 0, 0]

S3PAS_mar5_west = [0, 0, 0, 0, 0, 0, 3, 20, 38, 53, 64, 70, 71, 66, 55, 40, 
                   21, 3, 0, 0, 0, 0, 0, 0]

TRNSYS_mar5_west = [0, 0, 0, 0, 0, 0, 2.99, 20.17, 37.92, 53.17, 64.39, 
                    69.89, 70.75, 65.69, 55.03, 39.61, 21.42, 3.28, 0, 0, 
                    0, 0, 0, 0]

TASE_mar5_west = [0, 0, 0, 0, 0, 0, 3, 20.15, 37.9, 53.15, 64.4, 69.95, 
                  71.16, 66.02, 55.16, 39.73, 21.6, 0, 0, 0, 0, 0, 0, 0]

ref_mar5_west = np.vstack((ESP_mar5_west, DOE21D_mar5_west, 
                            SRES_SUN_mar5_west, SRES_mar5_west,
                            S3PAS_mar5_west, TRNSYS_mar5_west,
                            TASE_mar5_west))


#HOURLY INCIDENT SOLAR RADIATION CLOUDY DAY, MARCH 5
#CASE 600
#SOUTH SURFACE
# Data extracted from RESULTS5-2.xls, sheet "data for charts", cells B360-I383
# all values in Wh/m^2
ESP_mar5_south = [0, 0, 0, 0, 0, 0, 1.6, 13.8, 31.6, 48.3, 61.6, 69.3, 71.7, 
                  68.1, 58.9, 44.4, 26.9, 8.7, 0, 0, 0, 0, 0, 0]

# no data for BLAST

DOE21D_mar5_south = [0, 0, 0, 0, 0, 0, 1.5, 12.59, 30.01, 46.23, 59.31, 
                     65.05, 66.98, 63.11, 51.79, 37.13, 19.14, 4.62, 0, 
                     0, 0, 0, 0, 0]

SRES_SUN_mar5_south = [0, 0, 0, 0, 0, 0, 3.0447, 20.646, 38.884, 54.566, 
                       65.973, 71.784, 72.2839, 66.4075, 54.8997, 38.8836, 
                       20.4797, 3.0447, 0, 0, 0, 0, 0, 0]

SRES_mar5_south = [0, 0, 0, 0, 0, 0, 3.02, 20.59, 38.83, 54.53, 54.77, 59.65, 
                   60.1, 55.24, 45.68, 32.37, 17.06, 2.54, 0, 0, 0, 0, 0, 0]

S3PAS_mar5_south = [0, 0, 0, 0, 0, 0, 3, 21, 39, 55, 66, 72, 72, 66, 55, 39, 
                    20, 3, 0, 0, 0, 0, 0, 0]

TRNSYS_mar5_south = [0, 0, 0, 0, 0, 0, 3.05, 20.69, 38.94, 54.67, 66.08, 
                     71.92, 72.42, 66.53, 55, 38.94, 20.52, 3.05, 0, 0, 0, 
                     0, 0, 0]

TASE_mar5_south = [0, 0, 0, 0, 0, 0, 3, 20.68, 38.94, 54.56, 65.99, 71.74, 
                   72.3, 66.38, 54.8, 38.84, 20.46, 0, 0, 0, 0, 0, 0, 0]

ref_mar5_south = np.vstack((ESP_mar5_south, DOE21D_mar5_south, 
                            SRES_SUN_mar5_south, SRES_mar5_south,
                            S3PAS_mar5_south, TRNSYS_mar5_south,
                            TASE_mar5_south))


def plot_results(results):
    """
    """
    # Extract results
    heatingLoad = results.heatingLoad
    coolingLoad = results.coolingLoad
    heatingPeak = results.heatingPeak
    coolingPeak = results.coolingPeak

    solarNorth = results.solarGainsNorth
    solarEast  = results.solarGainsEast
    solarWest  = results.solarGainsWest
    solarSouth = results.solarGainsSouth
    solarHorizontal = results.solarGainsHorizontal
    
    solarWindowSouth = results.solarGainsWindowSouth
    
    values = [heatingLoad, coolingLoad, heatingPeak, coolingPeak]
    
    fig = plt.figure(figsize=(9, 6))

    # Create an axes instance
    ax = fig.add_subplot(111)
    
    # Create the boxplot
    plt.plot(range(len(values)), values, marker="o", ms=10, ls="none", color="red", label="Results")
    plt.plot(range(len(values)), loads, marker='_', ms=10, ls="none", label="Reference", color="blue")

    plt.errorbar(x=range(len(values)), 
                 y=loads,
                 yerr=loadsYErr,
                 marker='_', ms=10,
                 ls='none', mec='blue', capsize=10)
    
    plt.xlim(-1, 4)
    plt.legend(numpoints=1)


def plot_west_surface(results):
    mar5  = results.solarWestMarch5
    jul27 = results.solarWestJuly27

    time = np.linspace(1, 24, 24)
    
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.plot(time, mar5,  label="result mar5")
    ax1.plot(time, np.min(ref_mar5_west, axis=0), 
             "k--", label="ref_mar5_min")
    ax1.plot(time, np.max(ref_mar5_west, axis=0), 
             "k--", label="ref_mar5_max")
    ax1.legend()
    plt.show()
    
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    ax2.plot(time, jul27, label="result jul27")
    ax2.plot(time, np.min(ref_jul27_west, axis=0), 
             "k--", label="ref_jul27_min")
    ax2.plot(time, np.max(ref_jul27_west, axis=0), 
             "k--", label="ref_jul27_max")
    ax2.legend()
    plt.show()


def plot_south_surface(results):
    mar5  = results.solarSouthMarch5
    jul27 = results.solarSouthJuly27

    time = np.linspace(1, 24, 24)
    
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.plot(time, mar5,  label="result mar5")
    ax1.plot(time, np.min(ref_mar5_south, axis=0), 
             "k--", label="ref_mar5_min")
    ax1.plot(time, np.max(ref_mar5_south, axis=0), 
             "k--", label="ref_mar5_max")
    ax1.legend()
    
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    ax2.plot(time, jul27, label="result jul27")
    ax2.plot(time, np.min(ref_jul27_south, axis=0), 
             "k--", label="ref_jul27_min")
    ax2.plot(time, np.max(ref_jul27_south, axis=0), 
             "k--", label="ref_jul27_max")
    ax2.legend()


def plot_january_4(results):
    jan4 = results.january4
    
    time = np.linspace(1, 24, 24)
    
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.plot(time, jan4,  label="result jan4")
    ax1.plot(time, np.min(ref_jan4, axis=0), 
             "k--", label="ref_jan4_min")
    ax1.plot(time, np.max(ref_jan4, axis=0), 
             "k--", label="ref_jan4_max")
    ax1.legend(loc=3)
