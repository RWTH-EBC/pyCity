#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cooling demand class
"""

from __future__ import division
import numpy as np


class CoolingDemand(pycity_base.classes.demand.Load.Load):
    """
    Implementation of the cooling demand object
    """

    def __init__(self, environment, loadcurve):
        """
        Parameters
        ----------
        Test : Test

        """
