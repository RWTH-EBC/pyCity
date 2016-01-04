# coding=utf-8

from __future__ import division

import numpy as np
import pycity.functions.slp_thermal as slp_thermal

class Test_ThermalSLP(object):
    """
    Test class for thermal standardized load profile generation (SLP)
    """

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
        assert sum(test_temp_array)/len(test_temp_array) == average_temp[0]
