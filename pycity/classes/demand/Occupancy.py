#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Occupancy class. Holds information about number of occupants and their
occupancy profile.
"""

from __future__ import division
import os
import numpy as np
import random

import pycity_base.functions.occupancy_model as occupancy_model


class Occupancy(object):
    """
    """

    # Define class variables for transition_probability_matrixes and initial 
    # occupancy 
    tpm = {}

    occ_start_states = {}
    occ_start_states_loaded = False

    type_weekday = ["wd", "we"]  # weekday, weekend

    def __init__(self, environment, number_occupants, initial_day=1,
                 do_profile=True):
        """
        This class loads all input data before 
        
        Parameters
        ----------
        number_occupants : integer
            How many active occupants live in this apartment?
        initial_day : integer, optional
            Initial day. 1-5 correspond to Monday-Friday, 6-7 to Saturday and 
            Sunday
        do_profile : bool, optional
            Defines, if user profile should be generated (default: True).
            If set to False, only number of occupants is saved and no
            profile is generated.
        """

        assert number_occupants > 0, ('At least 1 person has to be defined ' +
                                      'as occupant')
        assert number_occupants <= 5, ('Max. allowed number of occupants ' +
                                       'per apartment is 5')

        self._kind = 'occupancy'
        self.number_occupants = number_occupants
        self.environment = environment
        self.occupancy = None  # Occupancy profile
        self.initial_day = initial_day

        if do_profile:
            self.gen_occ_profile()

    def gen_occ_profile(self):
        """
        Generate stochastic occupancy profile based on number of occupants
        and weekday.
        """
        src_path = os.path.dirname(os.path.dirname(os.path.dirname
            (os.path.abspath(
            __file__))))
        folder_path = os.path.join(src_path, 'inputs',
                                   'stochastic_electrical_load',
                                   'constants')
        if not Occupancy.occ_start_states_loaded:
            # Load start states matrixes
            Occupancy.occ_start_states_loaded = True

            for weekday in self.type_weekday:
                filename = str("occ_start_states_" + weekday + ".csv")
                file_path = os.path.join(folder_path, filename)
                temp = (np.loadtxt(file_path, delimiter=";")).tolist()
                Occupancy.occ_start_states[weekday] = temp

        if not (self.number_occupants, "wd") in list(Occupancy.tpm.keys()):
            # Load transition probability matrixes
            for weekday in self.type_weekday:
                fname = str(
                    "tpm" + str(
                        self.number_occupants) + "_" + weekday + ".csv")
                file_path = os.path.join(folder_path, fname)
                temp = (np.loadtxt(file_path, delimiter=";")).tolist()
                Occupancy.tpm[self.number_occupants, weekday] = temp

        # Determine initial occupancy:
        # Determine if the current day is a weekend-day
        if self.initial_day <= 5:
            self.weekend = False
        else:
            self.weekend = True
        # Get starting states and starting probabilities
        start_states = Occupancy.occ_start_states
        start_probs = start_states[self.type_weekday[self.weekend]]
        self.initial_occupancy = self._get_start_state(
                                      start_probs[:][self.number_occupants])

        # Make a full year occupancy computation
        occupancy = []
        # Loop over all days
        for i in range(self.environment.timer.totalDays):
            if (i + self.initial_day) % 7 in (0, 6):
                weekend = True
            else:
                weekend = False

            occupancy.append(self._get_occupancy(weekend))

        occupancy = np.array(occupancy)
        self.occupancy = np.reshape(occupancy, occupancy.size)

    def _get_start_state(self, start_probabilities):
        """
        Determine the active occupancy start state.
        """
        # Pick a random number to determine the start state
        fRand = random.random()

        # Reset the cumulative probability count
        fCumulativeP = 0

        # Return value
        result = 0

        # Loop construction
        found = False  # Boolean variable instead of using break
        i = 0

        while not found:
            fCumulativeP += start_probabilities[i]
            if (fRand < fCumulativeP or i >= len(start_probabilities) - 1):
                result = i
                found = True
            i += 1

        return result

    def _get_occupancy(self, weekend):
        """
        """
        # Select appropriate transition probability matrix
        tpm = self.tpm[self.number_occupants, self.type_weekday[weekend]]

        # Compute occupancy for all required time steps
        occupancy = occupancy_model.all_states(tpm, self.initial_occupancy)

        # Make the last computed occupancy the new initial value
        self.initial_occupancy = occupancy[-1]

        return occupancy
