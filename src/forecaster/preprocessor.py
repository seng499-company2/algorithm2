# preprocessor.py
# Author:
# Date: June 17th, 2022
# This module preprocesses data for use in the forecaster

import math


# Private Module Variables, Classes
_MIN_COURSES = 1
_MAX_COURSES = 6
_RATIO_ACADEMIC = float(11/15)
_PROGRAM_GROWTH = 1.0855

# Private Module Helper Functions
# API Functions


def compute_bounds(program_enrolment: dict) -> (int, int):
    """ This function computes the upper and lower bound on the global
    seat allocation

    :param program_enrolment: historical course enrollment data
    :return: lower and upper bound for global seat assignment
    """

    prev_enrollment = 0
    for year in program_enrolment["2021"].keys():
        prev_enrollment += program_enrolment["2021"][year]

    # TODO: It might be worthwhile to actually recompute the trend line
    # In this function, rather than hard coding 8.55%
    current_enrolment = math.ceil(prev_enrollment * _PROGRAM_GROWTH)

    lower_bound = _MIN_COURSES * math.ceil((current_enrolment * _RATIO_ACADEMIC))
    upper_bound = _MAX_COURSES * math.ceil((current_enrolment * _RATIO_ACADEMIC))

    return lower_bound, upper_bound


def pre_process(course_enrollment: dict) -> dict:
    """ Takes class enrollment JSON and generates an intermediate object with data-series
     organized by class-term

    :param course_enrollment: object loaded from course enrolment JSON file
    :return: internal intermediate course data series object
    """

    return {"CSC110-F": {"data": [0, 0, 500, 200, 400], "approach": 0, "capacity": 500}}
