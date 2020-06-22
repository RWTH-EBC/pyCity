#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Room class.
"""


class Room(object):
    """
    """

    def __init__(self, environment):
        """
        Constructor of room object.

        Parameters
        ----------
        environment : object
            Environment of pyCity
        """

        self.environment = environment
        self._kind = "room"

    @property
    def kind(self):
        return self._kind
