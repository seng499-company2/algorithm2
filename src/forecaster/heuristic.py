# heuristic.py
# Author: Sean McAuliffe,
# Date: June 17th, 2022
# This module applies the heuristics to determine course capacities

# Helper Functions

# Module API
def apply_heuristics(internal_series: dict, enrolment: dict, low_bound: int, high_bound: int) -> None:
    """ Given an intermediate_object, for each course offering marked for
    the heuristic approach, guarantee a course capacity to be applied to
    each course.

    :param internal_series: Data series collated by course offering
    :param enrolment: program enrollment loaded from JSON object
    :param low_bound: minimum number of global seats
    :param high_bound: maximum number of global seats
    :return:
    """

    # {"CSC110-F": {"data": [0, 0, 500, 200, 400], "approach": 0, "capacity": 500}}
    """
    Heuristic 1: current_enrollment = (most_recent_enrolment/total_enrollment_that_year)*(1.0855^years_since_last_data)
    Heuristic 2: current_enrollment = (remaining_seats/number_unassigned_courses)
    remaining_seats = high_bound - sum(assigned_capacities)
    Use heuristic 1 if at least 1 data point
    Use heuristic 2 if no data points at all
    Use heuristic 1 to assign as many courses as possible before resorting to heuristic 2
    """

    pass
