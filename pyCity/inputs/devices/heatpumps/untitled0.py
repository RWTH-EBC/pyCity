# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 13:28:53 2015

@author: tsz
"""

import characteristics
import numpy as np

import scipy as sp
import math

hp = characteristics.HPCharacteristics(10000)

timesteps = 5

t_ambient = np.sin(np.arange(timesteps) / math.pi)*10

t_flow = np.ones(timesteps) * 50

(tAmbient, tFlow, heat, power) = hp.getCharacteristics()

q = np.zeros((timesteps, len(tFlow)))
p = np.zeros((timesteps, len(tFlow)))
for i in xrange(len(tFlow)):
    q[:,i] = np.interp(t_ambient, tAmbient, heat[:,i])
    p[:,i] = np.interp(t_ambient, tAmbient, power[:,i])
    
resHeat = np.zeros(timesteps)
resPower = np.zeros(timesteps)
for j in xrange(timesteps):
    resHeat[j]  = np.interp(t_flow[j], tFlow, q[j,:])
    resPower[j] = np.interp(t_flow[j], tFlow, p[j,:])

