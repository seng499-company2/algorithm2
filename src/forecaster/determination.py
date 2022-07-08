# determination.py
# Author:
# Date: June 17th, 2022
# This module determines the approach to use
from .constants import *

# Private Module Variables, Classes


# Private Module Helper Functions
def is_year_recent_enough(course_data: list):
    for count, capacity in enumerate(reversed(course_data)):
        if count < MAX_TERMS_SINCE_LAST_OFFERING and capacity > 0:
            return True
        if count > MAX_TERMS_SINCE_LAST_OFFERING:
            break

    return False


def is_enough_data(course_data: list):
    count = 0
    for capacity in course_data:
        if capacity > 0:
            count = count + 1

    if count >= MIN_DATA_POINTS:
        return True

    return False


# API Functions
def determine_approach(internal_series: dict) -> None:
    """ For each course offering in the internal data series, determine
    whether to apply statical or heuristic methods for capacity assignment:
    by filling in the approach field for each offering in internal series.

    :param internal_series: Data series collated by course offering
    :return: None, internal_series is modified in place
    """

    for key, course in internal_series.items():
        print(course)
        course['approach'] = 0

        if course['capacity'] is not 0:
            course["approach"] = -1
            continue

        # The most recent data is too old
        if not is_year_recent_enough(course['data']):
            continue
        # There isn't enough data
        if not is_enough_data(course['data']):
            continue

        # If all check passed we have enough information for statistical forecasting
        course['approach'] = 1

    return
