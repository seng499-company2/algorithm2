# guarantor.py
# Author:
# Date: June 17th, 2022
# This module checks the intermediate object against the inputted schedule object and verifies
# that no classes have been dropped or added, that each course has an assigned capacity, and that
# the total number of allocated seats is within our bounds.

from enum import Enum
from .constants import *

import logging

# =============================================================================
# Module Private Variables and Classes
# =============================================================================


class Status(Enum):
    GOOD = 1
    MISSING_CLASS = 2
    MISSING_ASSIGMENT = 3
    BOUNDS_ERROR = 4
    MALFORMED_OUTPUT = 5


# =============================================================================
# Private Module Helper Functions
# =============================================================================


def scale_capacities_down(internal_series: dict, high_bound: int, current: int) -> None:
    """ In the case that global seat assignment is outside of bounds, scale
    course capacity assignments until a bound is reached.

    :param current: The current number of assigned seats
    :param high_bound: global maximum number of seats
    :param internal_series: internal data series representing course offerings
    :return: None, internal_series is modified in place
    """

    # Overflow is the number of seats that need to be removed
    overflow = current - high_bound
    capacities = []

    # Create a list of course offerings sorted in descending order by capacity
    for offering in internal_series.keys():
        capacities.append((offering, internal_series[offering]))

    sorted_capacities = sorted(capacities, key=lambda x: x[1]["capacity"], reverse=True)

    # Remove seats from the highest capacity courses first, then lower capacity seats
    # Until the overflow is zero
    i = 0
    while overflow > 0:
        internal_series[sorted_capacities[i][0]]["capacity"] -= 1
        overflow -= 1
        i += 1
        i %= len(sorted_capacities)


def scale_capacities_up(internal_series: dict, low_bound: int, current: int) -> None:
    """ In the case that global seat assignment is outside of bounds, scale
    course capacity assignments until a bound is reached.

    :param current: The current number of assigned seats
    :param low_bound: global minimum number of seats
    :param internal_series: internal data series representing course offerings
    :return: None, internal_series is modified in place
    """

    # Underflow is the number of additional seats which need to be assigned
    underflow = low_bound - current
    capacities = []

    # Create a list of offerings in ascending order of capacity
    for offering in internal_series.keys():
        capacities.append((offering, internal_series[offering]))

    sorted_capacities = sorted(capacities, key=lambda x: x[1]["capacity"])

    # Assign seats to the lowest capacity courses first, until the
    # underflow is zero
    i = 0
    while underflow > 0:
        internal_series[sorted_capacities[i][0]]["capacity"] += 1
        underflow -= 1
        i += 1
        i %= len(sorted_capacities)


def check_bounds(internal_series: dict, low: int, high: int) -> bool:
    total_seats = 0
    for course_offering in internal_series.keys():
        if internal_series[course_offering]["approach"] != -1:
            total_seats += internal_series[course_offering]["capacity"]

    if total_seats > high or total_seats < low:
        return False

    return True


def get_capacity(course):
    sum = 0
    for section in course["sections"]:
        sum += int(section["capacity"])
    return sum


def compare_offerings(course_a, course_b):
    if course_a["course"]["code"] != course_b["course"]["code"]:
        return False
    if course_a["course"]["title"] != course_b["course"]["title"]:
        return False
    if len(course_a["sections"]) != len(course_b["sections"]):
        return False
    for section_a, section_b in zip(course_a["sections"], course_b["sections"]):
        if section_a["professor"] != section_b["professor"]:
            return False
    return True


# =============================================================================
# API Functions
# =============================================================================


def verify_intermediate(internal_series: dict, schedule: dict, low_bound: int, high_bound: int) -> Status:
    """ Apply validation checks to the internal_series which is the intermediate
    object our algorithm operates on.

    :param internal_series: internal data series representing course offerings
    :param schedule: object provided by caller, against which to check internal_series
    :param low_bound: global minimum number of seats
    :param high_bound: global maximum number of seats
    :return: status code representing result of verification
    """

    total_seats = 0
    semester_courses = {
        "fall": [],
        "spring": [],
        "summer": []
        }

    for course_offering in internal_series.keys():
        logging.debug('%s Checking intermediate capacity' % (str(course_offering).ljust(15, ' ')))
        if course_offering.endswith("F"):
            semester_courses["fall"].append(course_offering.split('-')[0])
        elif course_offering.endswith("SP"):
            semester_courses["spring"].append(course_offering.split('-')[0])
        elif course_offering.endswith("SU"):
            semester_courses["summer"].append(course_offering.split('-')[0])
        capacity = internal_series[course_offering]["capacity"]
        if capacity <= 0:
            return Status.MISSING_ASSIGMENT
        if internal_series[course_offering]["approach"] != -1:
            total_seats += capacity

    if SCALING_FEATURE_FLAG:
        logging.debug('Applying scaling')
        if total_seats > high_bound:
            scale_capacities_down(internal_series, high_bound, total_seats)
        elif total_seats < low_bound:
            scale_capacities_up(internal_series, low_bound, total_seats)

        if not check_bounds(internal_series, low_bound, high_bound):
            return Status.BOUNDS_ERROR
    else:
        logging.debug('Skipping scaling')

    for semester in ["fall", "spring", "summer"]:
        number_courses = 0
        for course in schedule[semester]:
            number_courses += 1
            if course["course"]["code"] not in semester_courses[semester]:
                return Status.MISSING_CLASS
        if number_courses != len(semester_courses[semester]):
            return Status.MALFORMED_OUTPUT

    return Status.GOOD


def verify_final(new_schedule: dict, old_schedule: dict) -> Status:
    """ After postprocessor creates a new schedule object to be returned to caller,
    we need to verify that the new schedule does not contain any errors

    :param new_schedule: schedule created by postprocessor
    :param old_schedule: schedule provided by backend caller
    :return: status code representing result of verification
    """

    for semester in ["fall", "spring", "summer"]:
        for course_a, course_b in zip(old_schedule[semester], new_schedule[semester]):
            if not compare_offerings(course_a, course_b):
                return Status.MISSING_CLASS
            if get_capacity(course_b) <=0:
                return Status.MISSING_ASSIGMENT
        if len(new_schedule[semester]) != len(old_schedule[semester]):
            return Status.MALFORMED_OUTPUT

    return Status.GOOD
