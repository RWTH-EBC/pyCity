#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
City generator test.
"""

import pycity_base.functions.scripts.city_generators.city_generator as citygen


class TestCityGen():

    def test_city_gen(self):

        citygen.run_city_generator()
