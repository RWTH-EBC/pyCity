#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

import os

import pycity_base.classes.Timer as Timer
import pycity_base.classes.Weather as Weather




class Test_Weather():

    def test_weather(self):

        timer = Timer.Timer()

        weather = Weather.Weather(timer=timer)

        weather.setLocation(location=(50.76, 6.07),
                            timeZone=1,
                            altitude=200)
