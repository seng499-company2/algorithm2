# preprocessor.py
# Author:
# Date: June 17th, 2022
# This module preprocesses data for use in the forecaster

# Private Module Variables, Classes
# Private Module Helper Functions
# API Functions

def compute_bounds(program_enrolment: dict) -> (int, int):
    """ This function computes the upper and lower bound on the global
    seat allocation

    :param program_enrolment:
    :return:
    """

    lower_bound = 0
    upper_bound = 100
    # Implement this
    return lower_bound, upper_bound


def pre_process(course_enrollment: dict) -> dict:
    """ Takes class enrollment JSON and generates an intermediate object with data-series
     organized by class-term

    :param course_enrollment: object loaded from course enrolment JSON file
    :return: internal intermediate course data series object
    """

    return {"CSC110-F": {"data": [0, 0, 500, 200, 400], "approach": 0, "capacity": 500}}
