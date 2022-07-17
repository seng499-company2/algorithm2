# heuristic.py
# Author: Sean McAuliffe,
# Date: June 17th, 2022
# This module applies  heuristics to determine guarantee capacity
# assignments for every course offering.

from enum import Enum
from math import floor, pow
import logging

from forecaster.preprocessor import PROGRAM_GROWTH
from forecaster.constants import *

def get_course_type(course_offering: str):
    code = ''.join(c for c in course_offering if c.isdigit())
    year = code[0]
    semester = course_offering[-1]
    return year + semester


def average_capacity(capacities: list) -> int:
    seats = sum(capacities)
    total = 0
    for capacity in capacities:
        if capacity > 0:
            total += 1
    if total == 0:
        return 0
    return floor(seats/total)


# Module API
def apply_heuristics(internal_series: dict, enrolment: dict) -> None:
    """ Given an intermediate_object, for each course offering marked for
    the heuristic approach, guarantee a course capacity to be applied to
    each course.

    Heuristic 1: current_enrollment =
    (most_recent_enrolment/total_enrollment_that_year)*(1.0855^years_since_last_data)

    Heuristic 2: seat capacity = average of all similar courses predicted so far
    (similar = same year and same semester)

    Heuristic 3: hard coded "best guess" values

    Use heuristic 1 if at least 1 data point
    Use heuristic 2 if no data points, but similar courses have been predicted
    Use heuristic 3 if no data and no similar courses have been predicted

    :param internal_series: Data series collated by course offering
    :param enrolment: program enrollment loaded from JSON object
    :param low_bound: minimum number of global seats
    :param high_bound: maximum number of global seats
    :return: None, the internal series is modified in place
    """

    # Assign capacities to courses which have a data point
    for course in internal_series.keys():
        if internal_series[course]["capacity"] <= 0:
            logging.debug('%s Trying Heuristics with data' % (str(course).ljust(15, ' ')))
            for i, enrolment in enumerate(reversed(internal_series[course]["data"])):
                if enrolment != 0:
                    capacity = floor(enrolment * pow(PROGRAM_GROWTH, (i+1)))
                    internal_series[course]["capacity"] = capacity
                    logging.debug('%s Success Heuristics forecasted %d' % (str(course).ljust(15, ' '), capacity))

                    break

    # Assign capacities to courses which have no data point
    # but are similar to a course with data
    course_types = set()
    for course in internal_series.keys():
        if internal_series[course]["capacity"] <= 0:
            course_types.add(get_course_type(course))

    # Initialize average assignments to 0
    average_assignments = {course_type: [0] for course_type in course_types}

    # Calculate average assignments
    for course in internal_series.keys():
        type = get_course_type(course)
        if type in course_types:
            average_assignments[type].append(internal_series[course]["capacity"])
    
    for assignment in average_assignments.keys():
        average = floor(average_capacity(average_assignments[assignment]))
        logging.debug('Average of %s is %d' % (str(assignment).ljust(15, ' '), average))
        average_assignments[assignment] = average

    for course in internal_series.keys():
        if internal_series[course]["capacity"] <= 0:
            logging.debug('%s Trying Heuristics 2 with forecasted averages' % (str(course).ljust(15, ' ')))
            type = get_course_type(course)
            if type in average_assignments.keys():
                internal_series[course]["capacity"] = average_assignments[type]
                logging.debug('%s Success Heuristics 2 forecasted %d' % (str(course).ljust(15, ' '),
                                                                         average_assignments[type]))
            
    # Assign remaining courses via heuristic 3
    for course in internal_series.keys():
        if int(internal_series[course]["capacity"]) <= 0:
            logging.debug('%s Trying Heuristics 3 with default averages' % (str(course).ljust(15, ' ')))
            course_code = ''.join(c for c in course if c.isdigit())
            if course_code[0] >= '4': # fourth year or greater
                internal_series[course]["capacity"] = FOURTH_YEAR_CAPACITY
                logging.debug(
                    '%s Success Heuristics 3 forecasted 4th year %d' % (str(course).ljust(15, ' '),
                                                                        FOURTH_YEAR_CAPACITY))
            elif course_code.startswith('3'):
                internal_series[course]["capacity"] = THIRD_YEAR_CAPACITY
                logging.debug(
                    '%s Success Heuristics 3 forecasted 3rd year %d' % (str(course).ljust(15, ' '),
                                                                        THIRD_YEAR_CAPACITY))
            elif course_code.startswith('2'):
                internal_series[course]["capacity"] = SECOND_YEAR_CAPACITY
                logging.debug(
                    '%s Success Heuristics 3 forecasted 2nd year %d' % (str(course).ljust(15, ' '),
                                                                        SECOND_YEAR_CAPACITY))
            elif course_code.startswith('1'):
                internal_series[course]["capacity"] = FIRST_YEAR_CAPACITY
                logging.debug(
                    '%s Success Heuristics 3 forecasted 1st year %d' % (str(course).ljust(15, ' '),
                                                                        FIRST_YEAR_CAPACITY))
            else: # What else could it be? Who knows but we must guarantee an output
                internal_series[course]["capacity"] = UNKNOWN_YEAR_CAPACITY
                logging.debug(
                    '%s Success Heuristics 3 forecasted unknown year %d' % (str(course).ljust(15, ' '),
                                                                            UNKNOWN_YEAR_CAPACITY))
