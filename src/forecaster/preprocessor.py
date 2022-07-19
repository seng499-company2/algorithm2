# preprocessor.py
# Author: Tristan Cusi
# Date: June 17th, 2022
# This module preprocesses data for use in the forecaster
import math
from typing import List
from .constants import *


#=============================================================================
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
    capacity = 0
    for course_offering in course_offerings:
        if course_offering['course']['code'] == course_code:
            for section in course_offering['sections']:
                if section['capacity'] is not None:
                    capacity = capacity + int(section['capacity'])
    return capacity


def generate_cutoff_semesters(year: int) -> List:
    """ This function generats a list of semester codes, which
    can be used to exclude historic enrollment data up to the input
    year. """
    cutoff_semesters = []
    for year in range(year, 2024):
        cutoff_semesters.append(str(year) + '09')
        cutoff_semesters.append(str(year) + '01')
        cutoff_semesters.append(str(year) + '05')
    return cutoff_semesters


#=============================================================================
# API Functions
#=============================================================================


def validate_inputs(course_enrolment: list, program_enrolment: dict, schedule: dict) -> tuple:
    """ This function validates the three inputs for forecaster, checking
    structure, if all fields necessary for forecaster are included and the
    types of the fields are correct.

    :param course_enrollment: historical course enrollment data
    :param program_enrolment: historical course enrollment data
    :param schedule: schedule object

    :return: 2-tuple with 
        1) Bool, True if all three inputs are valid, False if any arent
        2) If first value True -> None, else -> String explaining problem 
    """

    #check that historical course enrollment data is correct type
    if not isinstance(course_enrolment, list):
        error = f'Expected historical course enrollment to be a list not \
        {type(course_enrolment)} \n'
        return (False, error)

    for offering in course_enrolment:
        if not isinstance(offering, dict):
            error = f'Expected offering to be a dict not \
            {type(offering)} \n'
            return (False, error)
        #check that fields exists
        if 'term' not in offering:
            error = f'No "term" field in course offering\n'
            return (False, error)
        if 'enrollment' not in offering:
            error = f'No "enrollment" field in course offering\n'
            return (False, error)
        if 'subjectCourse' not in offering:
            error = f'No "subjectCourse" field in course offering\n'
            return (False, error)
        #check fields type is correct
        if not isinstance(offering['term'], str):
            error = f'Expected "term" field to be string not \
            {type(offering["term"])}\n'
            return (False, error)
        if not isinstance(offering['enrollment'], int):
            error = f'Expected "enrollment" field to be int not \
            {type(offering["enrollment"])}\n'
            return (False, error)
        if not isinstance(offering['subjectCourse'], str):
            error = f'Expected "subjectCourse" field to be string not \
            {type(offering["subjectCourse"])}\n'
            return (False, error)

    #check program enrollment is a dict
    if not isinstance(program_enrolment, dict):
        error = f'Expected historical program enrollment to be a dict not \
        {type(program_enrolment)} \n'
        return (False, error)

    #check each dict item 
    for key in program_enrolment:
        if not isinstance(program_enrolment[key], dict):
            error = f'Expected yearly enrollment item to be a dict not \
            {type(program_enrolment[key])} \n'
            return (False, error)
        #check that fields exist
        if '1' not in program_enrolment[key]:
            error = f'No "1" field in {key} program enrolment entry\n'
            return (False, error)
        if '2' not in program_enrolment[key]:
            error = f'No "2" field in {key} program enrolment entry\n'
            return (False, error)
        if '2T' not in program_enrolment[key]:
            error = f'No "2T" field in {key} program enrolment entry\n'
            return (False, error)
        if '3' not in program_enrolment[key]:
            error = f'No "3" field in {key} program enrolment entry\n'
            return (False, error)
        if '4' not in program_enrolment[key]:
            error = f'No "4" field in {key} program enrolment entry\n'
            return (False, error)
        if '5' not in program_enrolment[key]:
            error = f'No "5" field in {key} program enrolment entry\n'
            return (False, error)
        if '6' not in program_enrolment[key]:
            error = f'No "6" field in {key} program enrolment entry\n'
            return (False, error)
        if '7' not in program_enrolment[key]:
            error = f'No "7" field in {key} program enrolment entry\n'
            return (False, error)
        #check that fields type are correct
        if not isinstance(program_enrolment[key]['1'], int):
            error = f'Expected "1" field to be int not \
            {type(program_enrolment[key]["1"])}\n'
            return (False, error)
        if not isinstance(program_enrolment[key]['2'], int):
            error = f'Expected "2" field to be int not \
            {type(program_enrolment[key]["2"])}\n'
            return (False, error)
        if not isinstance(program_enrolment[key]['2T'], int):
            error = f'Expected "2T" field to be int not \
            {type(program_enrolment[key]["2T"])}\n'
            return (False, error)
        if not isinstance(program_enrolment[key]['3'], int):
            error = f'Expected "3" field to be int not \
            {type(program_enrolment[key]["3"])}\n'
            return (False, error)
        if not isinstance(program_enrolment[key]['4'], int):
            error = f'Expected "4" field to be int not \
            {type(program_enrolment[key]["4"])}\n'
            return (False, error)
        if not isinstance(program_enrolment[key]['5'], int):
            error = f'Expected "5" field to be int not \
            {type(program_enrolment[key]["5"])}\n'
            return (False, error)
        if not isinstance(program_enrolment[key]['6'], int):
            error = f'Expected "6" field to be int not \
            {type(program_enrolment[key]["6"])}\n'
            return (False, error)
        if not isinstance(program_enrolment[key]['7'], int):
            error = f'Expected "7" field to be int not \
            {type(program_enrolment[key]["7"])}\n'
            return (False, error)

    #check schedule is a dict
    if not isinstance(schedule, dict):
        error = f'Expected schedule to be a dict not {type(schedule)}\n'
        return (False, error)

    #check each course offering has fields needed and correct type
    for term in schedule:
        if term not in ('fall', 'spring', 'summer'):
            error = f'Expected "fall", "spring", or "summer" field not \
            {schedule[term]}\n'
            return (False, error)
        if not isinstance(schedule[term], list):
            error = f'Expected term to be a list not {type(schedule[term])}\n'
            return (False, error)
        for offering in schedule[term]:
            if not isinstance(offering, dict):
                error = f'Expected offering to be a dict not \
                {type(offering)}\n'
                return (False, error)
            if 'course' not in offering:
                error = f'No "course" field in course offering\n'
                return (False, error)
            if 'sections' not in offering:
                error = f'No "sections" field in course offering\n'
                return (False, error)
            if not isinstance(offering['course'], dict):
                error = f'Expected offerings "course" field to be a dict not \
                {type(offering["course"])}\n'
                return (False, error)
            if not isinstance(offering['sections'], list):
                error = f'Expected offerings "sections" field to be a list \
                not {type(offering["course"])}\n'
                return (False, error)
            if 'code' not in offering['course']:
                error = f'Expected "code" field in course'
                return (False, error)
            if not isinstance(offering['course']['code'], str):
                error = f'Expected "code" field to be a string not \
                {type(offering["course"]["code"])}\n'
                return (False, error)
            for section in offering['sections']:
                if not isinstance(section, dict):
                    error = f'Expected section to be a dict not \
                    {type(section)}\n'
                    return (False, error)
                if 'capacity' not in section:
                    error = f'Expected "capacity" field to be in section'
                    return (False, error)
                # if 'max_capacity' not in section:
                #     error = f'Expected "max_capacity" field to be in section'
                #     return (False, error)
                if not isinstance(section['capacity'], int):
                    error = f'Expected capacity to be a int not \
                    {type(section["capacity"])}\n'
                    return (False, error)
                # if not isinstance(section['max_capacity'], int):
                #     error = f'Expected max_capacity to be a int not \
                #     {type(section['max_capacity'])}\n'
                #     return (False, error)
    return (True, None)


def compute_bounds(program_enrolment: dict):
    """ This function computes the upper and lower bound on the global
    seat allocation.

    :param program_enrolment: historical course enrollment data
    
    :return: lower and upper bound for global seat assignment
    """

    prev_enrollment = 0
    for year in program_enrolment[2021].keys():
        prev_enrollment += program_enrolment[2021][year]

    # TODO: It might be worthwhile to actually recompute the trend line
    #  in this function, rather than hard coding 8.55%
    current_enrolment = math.ceil(prev_enrollment * PROGRAM_GROWTH)

    lower_bound = CSC_FACTOR * (MIN_COURSES * math.ceil(current_enrolment * RATIO_ACADEMIC))
    upper_bound = CSC_FACTOR * (MAX_COURSES * math.ceil(current_enrolment * RATIO_ACADEMIC))

    return lower_bound, upper_bound  # Adjust the bounds to account for CSc. students


def pre_process(course_enrollment: list, schedule: dict, year_cutoff=None) -> dict:
    """ Takes class enrollment JSON and schedule JSON and generates an 
    intermediate object with data-series organized by class-term

    :param course_enrollment: historical course enrollment data
    :param schedule: JSON schedule object

    :return: internal intermediate course data series object
    """
    
    # create a list of course-term codes for each term 
    historical_term_codes = get_historical_term_codes(course_enrollment)

    # create a set of all course codes
    set_of_courses = get_set_of_course_codes(schedule)

    intermediate = {}
    remove_semesters = []
    if year_cutoff is not None:
        remove_semesters = generate_cutoff_semesters(year_cutoff)
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
                if offering in remove_semesters:
                    continue
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
