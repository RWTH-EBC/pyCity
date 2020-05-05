#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Room test.
"""

import pycity_base.classes.demand.room as room
from pycity_base.test.pycity_fixtures import create_environment


class TestRoom():

    def test_room(self, create_environment):

        room.Room(environment=create_environment)
