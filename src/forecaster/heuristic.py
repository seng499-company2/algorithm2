# heuristic.py
# Author: Sean McAuliffe,
# Date: June 17th, 2022
# This module applies  heuristics to determine guarantee capacity
# assignments for every course offering.


from math import floor, pow
from statistics import mean
from forecaster.preprocessor import PROGRAM_GROWTH


def get_course_type(course_offering: str):
    year = course_offering[0]
    semester = course_offering[-1]
    return year + semester


# Module API
def apply_heuristics(internal_series: dict, enrolment: dict, low_bound: int, high_bound: int) -> None:
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
            for i, enrolment in enumerate(reversed(internal_series[course]["data"])):
                if enrolment != 0:
                    internal_series[course]["capacity"] = math.floor(enrolment * math.pow(PROGRAM_GROWTH, (i+1)))
                    break

    # Assign capacities to courses which have no data point
    # but are similar to a course with data
    course_types = set()
    for course in internal_series.keys():
        if internal_series[course]["capacity"] <= 0:
            course_types.add(get_course_type(course))

    # Initialize average assignments to 0
    average_assignments = {course_type: [] for course_type in course_types}

    # Calculate average assignments
    for course in internal_series.keys():
        type = get_course_type(course)
        if type in course_types:
            average_assignments[type].append(internal_series[course]["capacity"])
    
    for assignment in average_assignments.keys():
        average = math.floor(mean(average_assignments[assignment]))
        average_assignments[assignment] = average
            
    # Assign remaining courses via heuristic 3
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
