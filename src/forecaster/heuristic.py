# heuristic.py
# Author: Sean McAuliffe,
# Date: June 17th, 2022
# This module applies the heuristics to determine course capacities

from enum import Enum
import math
from forecaster.preprocessor import PROGRAM_GROWTH


# Helper Functions
def year_from_index(index: int) -> int:
    return 2008 + index


# Module API
def apply_heuristics(internal_series: dict, enrolment: dict, low_bound: int, high_bound: int) -> None:
    """ Given an intermediate_object, for each course offering marked for
    the heuristic approach, guarantee a course capacity to be applied to
    each course.

    Heuristic 1: current_enrollment =
    (most_recent_enrolment/total_enrollment_that_year)*(1.0855^years_since_last_data)
    Heuristic 2: current_enrollment = (remaining_seats/number_unassigned_courses)
    remaining_seats = high_bound - sum(assigned_capacities)
    Use heuristic 1 if at least 1 data point
    Use heuristic 2 if no data points at all

    :param internal_series: Data series collated by course offering
    :param enrolment: program enrollment loaded from JSON object
    :param low_bound: minimum number of global seats
    :param high_bound: maximum number of global seats
    :return: None, the internal series is modified in place
    """

    remaining_seats = high_bound
    unassigned_courses = 0

    # Assign capacities to courses which have a data point
    for course in internal_series.keys():
        if internal_series[course]["capacity"] <= 0:
            for i, enrolment in enumerate(reversed(internal_series[course]["data"])):
                if enrolment != 0:
                    internal_series[course]["capacity"] = math.floor(enrolment * math.pow(PROGRAM_GROWTH, (i+1)))
                    break

    # Assign remaining courses via temporary heuristic
    for course in internal_series.keys():
        if int(internal_series[course]["capacity"]) <= 0:
            course_code = ''.join(c for c in course if c.isdigit())
            if course_code[0] >= '4': # fourth year or greater
                internal_series[course]["capacity"] = 50
            elif course_code.startswith('3'):
                internal_series[course]["capacity"] = 60
            elif course_code.startswith('2'):
                internal_series[course]["capacity"] = 80
            elif course_code.startswith('1'):
                internal_series[course]["capacity"] = 100
            else: # What else could it be? Who knows but we must guarantee an output
                internal_series[course]["capacity"] = 80

