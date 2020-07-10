#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Occupancy class. Holds information about number of occupants and their
occupancy profile.
"""

from __future__ import division

import copy

import richardsonpy.classes.occupancy as occ
from pycity_base.functions import change_resolution as chres


class Occupancy(object):
    """
    """

    def __init__(self, environment, number_occupants, initial_day=1, nb_days=365, do_profile=True):
        """
        Constructor of occupancy object.

        If occupancy profile is generated with do_profile == True, profile
        is saved with timestep of 600 seconds on Occupancy.occupancy.
        To return profile in other timestep, use method
        get_occ_profile_in_curr_timestep.

        Parameters
        ----------
        environment : object
            Environment of pyCity
        number_occupants : int
            Maximum number of occupants within apartment (range from 1 to 5)
        initial_day : int, optional
            Initial day. 1-5 correspond to Monday-Friday, 6-7 to Saturday and
            Sunday
        nb_days : int, optional
            Number of days, which should be used to generate profile
            (default: 365)
        do_profile : bool, optional
            Defines, if user profile should be generated (default: True).
            If set to False, only number of occupants is saved and no
            profile is generated.
        """

        assert number_occupants > 0, ('At least 1 person has to be defined ' +
                                      'as occupant')
        assert number_occupants <= 5, ('Max. allowed number of occupants ' +
                                       'per apartment is 5')

        assert nb_days > 0, 'Number of days must be larger than zero.'

        assert initial_day in [1, 2, 3, 4, 5, 6, 7]

        self._kind = 'occupancy'
        self.environment = environment
        self.number_occupants = number_occupants
        self.initial_day = initial_day
        self.nb_days = nb_days
        self.occupancy = None  # Occupancy profile

        if do_profile:
            occupancy = occ.Occupancy(number_occupants=number_occupants,
                                      initial_day=initial_day,
                                      nb_days=nb_days,
                                      do_profile=do_profile)

            occupancy.gen_occ_profile(nb_days=nb_days)

            #  Save occupancy profile
            self.occupancy = copy.copy(occupancy.occupancy)

    @property
    def kind(self):
        return self._kind

    def get_occ_profile_in_curr_timestep(self, timestep=None, int_con=False):
        """
        Returns occupancy profile in current timestep (as occupancy profile
        is saved with 600 seconds timestep, per default)

        Parameters
        ----------
        timestep : int, optional
            Defines specific timestep to return occupancy profile in
            (default: None). If None is chosen, returns profile with
            timestep found in environment.timer
        int_con : bool, optional
            Defines, if output values should be converted into integer
            numbers (conversion might lead to float numbers, depending
            on chosen timesteps) (default: False)

        Returns
        -------
        occ_profile : np.array
            Numpy array holding number of persons, present within
            zone
        """

        occ_profile = copy.copy(self.occupancy)

        if timestep is None:
            timestep = self.environment.timer.time_discretization

        occ_profile = chres.changeResolution(values=occ_profile,
                                             oldResolution=600,
                                             newResolution=timestep)

        if int_con:
            for i in range(len(occ_profile)):
                occ_profile[i] = int(round(occ_profile[i]))

        return occ_profile
