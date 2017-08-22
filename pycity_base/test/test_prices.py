#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

import pycity_base.classes.Prices as Prices


class Test_Prices():

    def test_prices(self):

        price = Prices.Prices()

        price.getAllData()

        price.setAllData()
