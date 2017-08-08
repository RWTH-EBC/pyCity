# coding=utf-8

import pytest

import pycity_base.functions.changeResolution as chres


class Test_ChangeResolution(object):
    """
    Test class for change of resolution functions
    """

    def test_change_res_mean_larger_timestep(self):
        input_array = [10, 10, 20, 20]
        output_array = chres.changeResolution(values=input_array,
                                                oldResolution=900,
                                                newResolution=3600,
                                                method="mean")
        assert output_array[0] == 10

    def test_change_res_mean_larger_timestep_2(self):
        input_array = [10, 20, 20, 20, 20, 30]
        output_array = chres.changeResolution(values=input_array,
                                                oldResolution=900,
                                                newResolution=3600,
                                                method="mean")
        assert output_array[0] == 10
        assert output_array[1] == 20


    def test_change_res_mean_smaller_timestep(self):
        input_array = [10, 20]
        output_array = chres.changeResolution(values=input_array,
                                                oldResolution=3600,
                                                newResolution=900,
                                                method="mean")
        assert output_array[0] == 10
        assert output_array[1] == 12.5
        assert output_array[2] == 15.
        assert output_array[3] == 17.5
        assert output_array[4] == 20
        assert output_array[5] == 20
        assert output_array[6] == 20
        assert output_array[7] == 20

    def test_change_res_sum_larger_timestep(self):
        input_array = [10, 10, 20, 20]
        output_array = chres.changeResolution(values=input_array,
                                                oldResolution=900,
                                                newResolution=3600,
                                                method="sum")
        assert output_array == [60]

    def test_change_res_sum_smaller_timestep(self):
        input_array = [10, 20]
        output_array = chres.changeResolution(values=input_array,
                                                oldResolution=3600,
                                                newResolution=900,
                                                method="sum")
        assert output_array[0] == 2.5
        assert output_array[1] == 2.5
        assert output_array[2] == 2.5
        assert output_array[3] == 2.5
        assert output_array[4] == 5
        assert output_array[5] == 5
        assert output_array[6] == 5
        assert output_array[7] == 5
