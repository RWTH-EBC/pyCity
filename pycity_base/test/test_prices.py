#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prices test.
"""

import pycity_base.classes.prices as prices


class TestPrices():

    def test_prices(self):

        price = prices.Prices()

        price.getAllData()

        price.setAllData()
