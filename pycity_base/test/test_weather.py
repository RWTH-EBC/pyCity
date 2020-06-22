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

        weather = we.Weather(timer=timer)

        weather.setLocation(location=(50.76, 6.07),
                            time_zone=1,
                            altitude=200)
