#!/usr/bin/env python
# coding=utf-8
"""
Script to load and select (random) profiles of profile pool.

Able to load occupancy, el. load and hot water profiles, depending on number
of occupants within apartments.

Requires gen_profile_pool run, first.
Expecting the following name structure:
['1_person_profiles.npz', '2_person_profiles.npz', '3_person_profiles.npz',
'4_person_profiles.npz', '5_person_profiles.npz']

npz internal arrays should hold name labels:
- occ (600 second resolution)
- el (60 second resolution)
- dhw (60 second resolution)
"""

import os
import random
import numpy as np
import matplotlib.pyplot as plt

from pycity_base.functions import change_resolution as chres


def get_list_of_npz_files(path):
    """
    Returns list of npz files found in path (only one level, no os.walk!)

    Parameters
    ----------
    path : str
        Path to folder, which should be searched through

    Returns
    -------
    list_npz : list
        List of npz file names found in path
    """

    list_npz = []

    for elem in os.listdir(path):  # Loop over all elements
        if os.path.isfile(os.path.join(path, elem)):  # if element is file
            if elem.endswith('.npz'):  # If filename endswith '.npz'
                list_npz.append(elem)

    return list_npz


class ProfilePool(object):
    """
    Class to hold profile pool

    Attributes
    ----------
    dict_data : dict
        Dictionary with number of occupants as key and numpy nd-array with
        profiles as values
    """

    def __init__(self, path_to_npz_folder=None):
        """
        Constructor of ProfilePool object

        Parameters
        ----------
        path_to_npz_folder : str, optional
            Path to folder, where profile pool npz files are stored
            (default: None). If set to None, no profiles are loaded.
            If path is given, going to load profiles during init
        """

        self.dict_data = {}

        if path_to_npz_folder is not None:
            #  Load npz files
            self.load_profile_npz(path_to_npz_folder)

    def load_profile_npz(self, path):
        """
        Load all npz numpy arrays into ProfilePool object

        Parameters
        ----------
        path : str
            Path to folder, where profile pool npz files are stored
        """

        #  Get list of npz files found in path
        list_npz = get_list_of_npz_files(path)

        for i in range(len(list_npz)):
            elem = list_npz[i]

            #  Construct path to load data
            path_load = os.path.join(path, elem)

            #  Load npz file
            npz_data = np.load(path_load)

            # Save data to dict_data
            key = i + 1
            self.dict_data[key] = npz_data

    def get_random_number(self):
        """
        Returns random number in the interval of number of different npz
        profiles.

        Returns
        -------
        rand_nb : int
            Random number
        """

        if len(self.dict_data) == 0:
            raise AssertionError('self.dict_data is empty. Load data first!')

        nb_profiles = len(self.dict_data[1]['occ'])

        return random.randint(0, nb_profiles - 1)

    def get_random_profile(self, nb_occupants, type, rand_number=None):
        """
        Returns copy of random occupancy profile with 600 second resolution

        Parameters
        ----------
        nb_occupants : int
            Number of occupants for profile (between 1 - 5)
        type : str
            Type of profile. Options: 'occ', 'el', 'dhw'
        rand_number = int, optional
            Random number to select profile (default: None). If set to None,
            going to select random integer. If integer is given, this integer
            is goint to be used.

        Returns
        -------
        profile : array-like
            Selected profile
        """

        if nb_occupants > 5 or nb_occupants <= 0:
            msg = 'Number of occupants must be between 1 and 5!'
            raise AssertionError(msg)

        if type not in ['occ', 'el', 'dhw']:
            msg = "Type must be ['occ', 'el', 'dhw']!"
            raise AssertionError(msg)

        if rand_number is None:
            #  Choose random number
            rand_number = self.get_random_number()
            print('Choosen random number: ', rand_number)

        return np.copy(self.dict_data[nb_occupants][type][rand_number])

    def get_occ_el_dhw_profile(self, nb_occupants, rand_number=None):
        """
        Returns tuply with occupancy, electrical load and hot water profile

        Parameters
        ----------
        nb_occupants : int
            Number of occupants for profile (between 1 - 5)
        type : str
            Type of profile. Options: 'occ', 'el', 'dhw'
        rand_number = int, optional
            Random number to select profile (default: None). If set to None,
            going to select random integer. If integer is given, this integer
            is goint to be used.

        Returns
        -------
        tuple_profiles : tuple (of array-like structures)
            Tuple with occupancy, electrical load and hot water profile
        """

        if nb_occupants > 5 or nb_occupants <= 0:
            msg = 'Number of occupants must be between 1 and 5!'
            raise AssertionError(msg)

        if rand_number is None:
            #  Choose random number
            rand_number = self.get_random_number()
            print('Choosen random number: ', rand_number)

        # Get occupancy profile
        occ_profile = self.get_random_profile(nb_occupants=nb_occupants,
                                              type='occ',
                                              rand_number=rand_number)

        #  Get el. load profile
        el_profile = self.get_random_profile(nb_occupants=nb_occupants,
                                             type='el',
                                             rand_number=rand_number)

        #  Get dhw load profile
        dhw_profile = self.get_random_profile(nb_occupants=nb_occupants,
                                              type='dhw',
                                              rand_number=rand_number)

        return (occ_profile, el_profile, dhw_profile)


if __name__ == '__main__':
    this_path = os.path.dirname(os.path.abspath(__file__))

    search_path = os.path.join(this_path, 'profiles')

    #  Generate ProfilePool object
    prof_pool = ProfilePool(path_to_npz_folder=search_path)

    #  Get occ, el. and dhw profile
    (occ_profile, el_profile, dhw_profile) = \
        prof_pool.get_occ_el_dhw_profile(nb_occupants=3)

    #  Change resolution of occupancy profile from 600 to 60 seconds
    occ_profile = chres.changeResolution(occ_profile, oldResolution=600, newResolution=60)

    el_energy = sum(el_profile) * 60 / (3600 * 1000)
    print('El. energy in kWh: ', el_energy)

    dhw_energy = sum(dhw_profile) * 60 / (3600 * 1000)
    print('Hot water net energy in kWh: ', dhw_energy)

    time_array = np.arange(0, 365*24*3600, 60)
    time_array = time_array / 3600

    fig = plt.figure()
    plt.subplot(311)
    plt.plot(time_array, occ_profile)
    plt.ylabel('Occupancy')

    plt.subplot(312)
    plt.plot(time_array, el_profile)
    plt.ylabel('El. load in Watt')

    plt.subplot(313)
    plt.plot(time_array, dhw_profile)
    plt.ylabel('Hot water load in Watt')

    plt.xlabel('Time in hours')
    plt.show()
