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
import numpy as np
import matplotlib.pyplot as plt


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


if __name__ == '__main__':

    this_path = os.path.dirname(os.path.abspath(__file__))

    search_path = os.path.join(this_path, 'profiles')

    #  Generate ProfilePool object
    prof_pool = ProfilePool(path_to_npz_folder=search_path)

    #  Access (first) occupancy profile for 3 person apartment
    occ_profile = prof_pool.dict_data[3]['occ'][0]

    print('Occupancy profile:')
    print(occ_profile)
    print('Length of occupancy profile:')
    print(len(occ_profile))
    plt.plot(occ_profile)
    plt.show()