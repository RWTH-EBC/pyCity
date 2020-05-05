#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Ashrae test.
"""

import pycity_base.examples.validation_ashrae140.zone_case_600 as zone_case_600

class TestAshrae140():

    def test_ashrae140(self):
        zone_case_600.run_validation()
