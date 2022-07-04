# preprocessor.py
# Author: Tristan Cusi
# Date: June 17th, 2022
# This module preprocesses data for use in the forecaster
import math

from traitlets import Tuple

# Module Private Variables and Classes
PROGRAM_GROWTH = 1.0855  # TODO: Calculate this dynamically based on program enrolment
MIN_COURSES = 1
MAX_COURSES = 6
RATIO_ACADEMIC = float(11/15)

# Private Module Helper Functions
#=============================================================================


def get_historical_term_codes(course_enrollment: list) -> dict:
    """ This function takes in the historical enrollments, counts up the
    term-course offering codes (eg 201801) and separates them into three terms
    fall, spring and summer"""
    historical_term_codes = {'fall':[], 'spring': [], 'summer': []}

    for course_term_offering in course_enrollment:
        if course_term_offering['term'].endswith('09'):
            historical_term_codes['fall']\
            .append(course_term_offering['term'])
        elif course_term_offering['term'].endswith('01'):
            historical_term_codes['spring']\
            .append(course_term_offering['term'])
        elif course_term_offering['term'].endswith('05'):
            historical_term_codes['summer']\
            .append(course_term_offering['term'])

    for term in ('fall', 'spring', 'summer'):
        historical_term_codes[term] = remove_dups(historical_term_codes[term])
        historical_term_codes[term].sort()

    return historical_term_codes


def remove_dups(input_list: list) -> list:
    """ This function removes duplicates from a list and returns that list"""
    return list(dict.fromkeys(input_list))

def get_set_of_course_codes(schedule: dict) -> set:
    """ This function takes in a schedule object and returns a set (unique
    list) of all course codes in that schedule"""
    list_of_courses = []

    for term in schedule.values():
        for course_offering in term:
            list_of_courses.append(course_offering['course']['code'])
    return set(list_of_courses)


def is_course_in_term(course_code: str, course_obj_list: list) -> bool:
    """ This function checks if a course is in the given schedule term course
    list"""
    for course_obj in course_obj_list:
        if course_obj['course']['code'] == course_code:
            return True
    return False


def get_capacity(course_code: str, course_offerings: list) -> int:
    """ This function retrieves the cumulative capacity for all sections of a
    course in a specified term"""
    capacity = 0;
    for course_offering in course_offerings:
        if course_offering['course']['code'] == course_code:
            for section in course_offering['sections']:
                capacity = capacity + int(section['capacity'])
    return capacity

#=============================================================================
# API Functions
#=============================================================================



def compute_bounds(program_enrolment: dict) -> tuple[int, int]:
    """ This function computes the upper and lower bound on the global
    seat allocation.

    :param program_enrolment: historical course enrollment data
    :return: lower and upper bound for global seat assignment
    """

    prev_enrollment = 0
    for year in program_enrolment["2021"].keys():
        prev_enrollment += program_enrolment["2021"][year]

    # TODO: It might be worthwhile to actually recompute the trend line
    #  in this function, rather than hard coding 8.55%
    current_enrolment = math.ceil(prev_enrollment * PROGRAM_GROWTH)

    lower_bound = MIN_COURSES * math.ceil(current_enrolment * RATIO_ACADEMIC)
    upper_bound = MAX_COURSES * math.ceil(current_enrolment * RATIO_ACADEMIC)

    return lower_bound, upper_bound


def pre_process(course_enrollment: list, schedule: dict) -> dict:
    """ Takes class enrollment JSON and schedule JSON and generates an 
    intermediate object with data-series organized by class-term

    :param course_enrollment: object loaded from course enrolment JSON file
    :param schedule: JSON schedule object

    :return: internal intermediate course data series object
    """
    
    # create a list of course-term codes for each term 
    historical_term_codes = get_historical_term_codes(course_enrollment)

    # create a set of all course codes
    set_of_courses = get_set_of_course_codes(schedule)

    intermediate = {}
    for course in set_of_courses:
        for term in ('fall', 'spring', 'summer'):
            if not is_course_in_term(course, schedule[term]):
                continue
            term_abbreviation = {'fall': 'F', 'spring': 'SP', 'summer': 'SU'}
            key = course + '-' + term_abbreviation[term]
            
            #check if course already has capacity from schedule
            capacity = get_capacity(course, schedule[term])
            if capacity > 0:
                intermediate[key] = {'data': None, 'approach': 0, \
                    'capacity': capacity}
                continue

            data = []
            # for each offering in (200801, 200805....)
            for offering in historical_term_codes[term]:
                # loop through course_enrollment to get enrollment data
                students_enrolled = 0
                for section in course_enrollment:
                    if ((section["term"] == offering) and\
                            (section["subjectCourse"] == course)):
                        # add up sections enrollments
                        students_enrolled = students_enrolled \
                            + section['enrollment']
                data.append(students_enrolled)
            intermediate[key] = {'data': data, 'approach': 0, 'capacity': 0}

    return intermediate 
