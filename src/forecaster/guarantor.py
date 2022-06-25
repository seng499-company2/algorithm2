# guarantor.py
# Author:
# Date: June 17th, 2022
# This module checks the intermediate object against the inputted schedule object and verifies
# that no classes have been dropped or added, that each course has an assigned capacity, and that
# the total number of allocated seats is within our bounds.

from enum import Enum


class Status(Enum):
    GOOD = 1
    MISSING_CLASS = 2
    MISSING_ASSIGMENT = 3
    BOUNDS_ERROR = 4
    FATAL_ERROR = 5


def verify_intermediate(internal_series: dict, schedule: dict, low_bound: int, high_bound: int) -> Status:
    """ Apply validation checks to the internal_series which is the intermediate
    object our algorithm operates on.

    :param internal_series: internal data series representing course offerings
    :param schedule: object provided by caller, against which to check internal_series
    :param low_bound: global minimum number of seats
    :param high_bound: global maximum number of seats
    :return: status code representing result of verification
    """


    return Status.GOOD


def scale_capacities(internal_series: dict, low_bound: int, high_bound: int) -> None:
    """ In the case that global seat assignment is outside of bounds, scale
    course capacity assignments until a bound is reached.

    :param low_bound: global minimum number of seats
    :param high_bound: global maximum number of seats
    :param internal_series: internal data series representing course offerings
    :return: None, internal_series is modified in place
    """

    pass


def verify_final(new_schedule: dict, old_schedule: dict) -> Status:
    """ After postprocessor creates a new schedule object to be returned to caller,
    we need to verify that the new schedule does not contain any errors

    :param new_schedule: schedule created by postprocessor
    :param old_schedule: schedule provided by backend caller
    :return: status code representing result of verification
    """

    return Status.GOOD
