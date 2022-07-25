# postprocessor.py
# Author:
# Date: June 17th, 2022
# This module post processes data for use in the forecaster

import copy
import json
import math
import logging

# Private Module Variables, Classes
internal_object = {}


# Private Module Helper Functions
def assign_capacities(term: dict, term_code: str):
    for course in term:
        course_name = course['course']['code'] + "-" + term_code
        course_sections = course['sections']
        num_sections = len(course_sections)
        try:
            logging.debug('%s Post-processing' % (str(course_name)).ljust(15, ' '))
            total_capacity = internal_object[course_name]['capacity']
            if num_sections == 1:
                
                #Checks if course has a maxCapacity field
                if 'maxCapacity' in course['sections'][0]:
                    maxCapacity = course['sections'][0]['maxCapacity']
                             
                    #Assign maxCapacity if forecasted capacity more
                    if int(total_capacity) >= int(maxCapacity):
                        course['sections'][0]['capacity'] = maxCapacity
                    
                    else:
                        course['sections'][0]['capacity'] = total_capacity
                else:
                    course['sections'][0]['capacity'] = total_capacity
                logging.debug('%s One section with %d' % (str(course_name).ljust(15, ' '), total_capacity))
            elif num_sections == 2:
                
                #Checks if section has a maxCapacity field
                if 'maxCapacity' in course['sections'][0]:
                    maxCapacity = course['sections'][0]['maxCapacity']
                    
                    #Checks if course has no data, then assign the maxCapacity as the capacity for the section
                    if internal_object[course_name]['data'] is None or all(v == 0 for v in internal_object[course_name]['data']):
                        course['sections'][0]['capacity'] = maxCapacity
                        
                    #Checks if forecasted capacity is more than maxCapacity, then assign the maxCapacity as the capacity for the section
                    elif int(math.ceil(total_capacity * 0.75)) > int(maxCapacity):
                        course['sections'][0]['capacity'] = maxCapacity
                    
                    else:
                        course['sections'][0]['capacity'] = math.ceil(total_capacity * 0.75)
                else:
                    course['sections'][0]['capacity'] = math.ceil(total_capacity * 0.75)
                
                #Checks if section has a maxCapacity field
                if 'maxCapacity' in course['sections'][1]:
                    maxCapacity = course['sections'][1]['maxCapacity']
                    
                    #Checks if course has no data, then assign the maxCapacity as the capacity for the section
                    if internal_object[course_name]['data'] is None or all(v == 0 for v in internal_object[course_name]['data']):
                        course['sections'][1]['capacity'] = maxCapacity
                        
                    #Checks if forecasted capacity is more than maxCapacity, then assign the maxCapacity as the capacity for the section
                    elif int(math.ceil(total_capacity * 0.25)) > int(maxCapacity):
                        course['sections'][1]['capacity'] = maxCapacity
                    
                    else:
                        course['sections'][1]['capacity'] = math.ceil(total_capacity * 0.25)
                else:
                    course['sections'][1]['capacity'] = math.ceil(total_capacity * 0.25)
                    
                logging.debug('%s Two sections with %d, and %d' % (str(course_name).ljust(15, ' '),
                                                                  math.ceil(total_capacity * 0.75),
                                                                  math.ceil(total_capacity * 0.25)))
            else:
                capacity_per_section = math.ceil(total_capacity / num_sections)
                logging.debug('%s %d sections with %d' % (str(course_name).ljust(15, ' '),num_sections, capacity_per_section))
                for section in course_sections:
                    section['capacity'] = capacity_per_section
        finally:
            continue

    return


# API Functions
def post_process(internal_obj: dict, schedule: dict) -> dict:
    """ This function combines all intermediate data and formats it into one
     final json for output.

    :param internal_obj: data series organised by course offering
    :param schedule: input schedule object provided by caller
    :return: copy of the input schedule object with capacities
    """

    global internal_object
    internal_object = internal_obj

    return_schedule = copy.deepcopy(schedule)  # Don't modify the original schedule

    fall_term = return_schedule['fall']
    spring_term = return_schedule['spring']
    summer_term = return_schedule['summer']

    assign_capacities(fall_term,   'F')
    assign_capacities(spring_term, 'SP')
    assign_capacities(summer_term, 'SU')

    return return_schedule
