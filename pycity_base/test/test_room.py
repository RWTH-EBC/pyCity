#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

import pycity_base.classes.demand.Room as Room
from pycity_base.test.pycity_fixtures import create_environment



class Test_Room():

    def test_room(self, create_environment):

        room = Room.Room(environment=create_environment)
