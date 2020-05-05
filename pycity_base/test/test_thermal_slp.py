#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test case for thermal standardized load profile generation (SLP)
"""

from __future__ import division

import numpy as np
import pycity_base.functions.slp_thermal as slp_thermal


class TestThermalSLP(object):

    def test_average_temperature(self):
        """
        Test method for average temperature calculation
        """
        test_temp_array = np.array([0, 0, 0, 0, 10, 10, 10, 10, 0, 0, 0, 0,
                                    10, 10, 10, 10, 0, 0, 0, 0, 10, 10, 10,
                                    10])
        average_temp = slp_thermal._average_temperature(test_temp_array)
        assert sum(test_temp_array)/len(test_temp_array) == average_temp[0]

        test_temp_array_2 = np.zeros(24*4)
        average_temp_2 = slp_thermal._average_temperature(test_temp_array_2)
        assert average_temp_2 == [0.0, 0.0, 0.0, 0.0]
