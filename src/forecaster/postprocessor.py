# postprocessor.py
# Author:
# Date: June 17th, 2022
# This module post processes data for use in the forecaster

import copy


# Private Module Variables, Classes
# Private Module Helper Functions
# API Functions
def post_process(internal_obj: dict, schedule: dict) -> dict:
    """ This function combines all intermediate data and formats it into one
     final json for output.

    :param internal_obj: data series organised by course offering
    :param schedule: input schedule object provided by caller
    :return: copy of the input schedule object with capacities
    """

    return_schedule = copy.deepcopy(schedule)  # Don't modify the original schedule
    return return_schedule
