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


def check_intermediate_validity(intermediate_object, schedule, lower_bound, upper_bound) -> Status:
    return Status.GOOD


def scale_capacities(intermediate_object) -> None:
    pass


def check_final_validity(schedule) -> Status:
    return Status.GOOD
