#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Weather test.
"""

import os

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
