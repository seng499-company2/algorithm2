import json
import sys
from .preprocessor import pre_process, compute_bounds
from .determination import determine_approach
from .statistical import apply_auto_arima
from .heuristic import apply_heuristics
from .guarantor import verify_intermediate, verify_final, Status
from .postprocessor import post_process


def forecast(course_enrolment: dict, program_enrolment: dict, schedule: dict) -> str:
    """ The forecast method will assign capacities to each course offering
    in the provided schedule object. It will use historical program and course
    enrollment data provided from JSON files to make determination about each
    course capacity.

    :param course_enrolment: python object loaded from course enrollment file
    :param program_enrolment: python objected loaded from program enrollment file
    :param schedule: common object shared with alg-1 representing course offerings
    :return: JSON encoding of schedule object with capacities assigned
    """
    if course_enrolment is None and program_enrolment is None and schedule is None:
        return 'OK'

    # Preprocessing steps, generate internal data series
    low_bound, high_bound = compute_bounds(program_enrolment)
    internal_series = pre_process(course_enrolment, schedule)

    # Determine approach and assign course capacities
    determine_approach(internal_series)
    apply_auto_arima(internal_series)
    apply_heuristics(internal_series, program_enrolment, low_bound, high_bound)

    # Verify that internal_series assignment was valid
    status = verify_intermediate(internal_series, schedule, low_bound, high_bound)
    if status is not Status.GOOD:
        raise Exception("Algorithm 2 failed to produce an output.")

    # Translate internal_series into schedule object
    output_schedule = post_process(internal_series, schedule)

    # Verify final schedule object
    status = verify_final(output_schedule, schedule)
    if status is not Status.GOOD:
        raise Exception("Algorithm 2 failed to produce an output.")

    # Return schedule to caller
    return json.dumps(output_schedule)
