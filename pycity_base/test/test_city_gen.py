#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
City generator test.
"""

from pycity_base.functions.scripts.city_generators import city_generator as citygen


class TestCityGen():

    def test_city_gen(self):

        citygen.run_city_generator()
