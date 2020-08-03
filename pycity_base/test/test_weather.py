#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Weather test.
"""

import os
import pytest

import pycity_base.classes.timer as ti
import pycity_base.classes.weather as we


class TestWeather():

    def test_weather(self):

        timer = ti.Timer()

        weather = we.Weather(timer=timer, use_TRY=True, use_TMY3=False)

        weather.setLocation(location=(50.76, 6.07),
                            time_zone=1,
                            altitude=200)

        assert(weather.weather_dataset_name == "TRY2010_05_Jahr")

        weather = we.Weather(timer=timer, use_TRY=False, use_TMY3=True)

        assert (weather.weather_dataset_name == "tmy3_744860_new_york_jfk_airport")

    def test_downscaled(self):
        timer1 = ti.Timer(900)
        timer2 = ti.Timer(3600)
        timer3 = ti.Timer(5400)
        timer4 = ti.Timer(86400)

        weather1 = we.Weather(timer=timer1, use_TRY=True, use_TMY3=False)
        weather2 = we.Weather(timer=timer2, use_TRY=True, use_TMY3=False)
        weather3 = we.Weather(timer=timer3, use_TRY=True, use_TMY3=False)
        weather4 = we.Weather(timer=timer4, use_TRY=True, use_TMY3=False)

        for i, v in enumerate(weather4.q_direct):
            assert sum(weather1.q_direct[i * 96:(i + 1) * 96]) / 96 == pytest.approx(v)
            assert sum(weather2.q_direct[i * 24:(i + 1) * 24]) / 24 == pytest.approx(v)
            assert sum(weather3.q_direct[i * 16:(i + 1) * 16]) / 16 == pytest.approx(v)
