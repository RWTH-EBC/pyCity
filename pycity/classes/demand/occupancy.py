#!/usr/bin/env python
# coding=utf-8
"""

"""

import richardsonpy.classes.occupancy as richocc


class Occupancy(richocc.Occupancy):
    """
    Occupancy class of pycity
    """

    def __init__(self, environment, number_occupants, do_profile=True):
        """
        Constructor of occupancy object

        Parameters
        ----------
        environment : object
            Environment object of pycity
        number_occupants : int
            Maximum number of occupants within apartment (range from 1 to 5)
        do_profile : bool, optional
            Defines, if user profile should be generated (default: True).
            If set to False, only number of occupants is saved and no
            profile is generated.
        """

        self.environment = environment

        initial_day = environment.timer.currentWeekday
        nb_days = int(environment.timer.timestepsTotal *
                      environment.timer.timeDiscretization / (24 * 3600))

        super(Occupancy, self).__init__(number_occupants=number_occupants,
                                        initial_day=initial_day,
                                        nb_days=nb_days, do_profile=do_profile)
