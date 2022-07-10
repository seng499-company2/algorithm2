import json
import sys
import os

from .preprocessor import pre_process, compute_bounds
from .determination import determine_approach
from .statistical import apply_auto_arima
from .heuristic import apply_heuristics
from .guarantor import verify_intermediate, verify_final, Status
from .postprocessor import post_process


def forecast(course_enrolment: dict, program_enrolment: dict, schedule: dict, force_flag: int = 2) -> str:
    """ The forecast method will assign capacities to each course offering
    in the provided schedule object. It will use historical program and course
    enrollment data provided from JSON files to make determination about each
    course capacity.

    :param course_enrolment: python object loaded from course enrollment file
    :param program_enrolment: python objected loaded from program enrollment file
    :param schedule: common object shared with alg-1 representing course offerings
    :param force_flag: Forces the forecaster to use heuristics(0), or auto-arima (1) [0:Heuristics, 1:Arima, 2:auto,]
    :return: JSON encoding of schedule object with capacities assigned
    """
    if course_enrolment is None:
        course_file = open(os.path.join(os.path.dirname(__file__), 'static_files/historicCourses.json'))
        course_enrolment  = json.load(course_file)
        course_file.close()

    if program_enrolment is None:
        enrollment_file = open(os.path.join(os.path.dirname(__file__), 'static_files/programEnrollmentData.json'))
        program_enrolment_json  = json.load(enrollment_file)
        program_enrolment = {int(k): v for k, v in program_enrolment_json.items()}
        enrollment_file.close()

    if schedule is None:
        schedule_file = open(os.path.join(os.path.dirname(__file__), 'static_files/testSchedule.json'))
        schedule  = json.load(schedule_file)
        schedule_file.close()



    # Preprocessing steps, generate internal data series
    low_bound, high_bound = compute_bounds(program_enrolment)
    internal_series = pre_process(course_enrolment, schedule)

    # Determine approach and assign course capacities
    determine_approach(internal_series, force_flag)
    apply_auto_arima(internal_series)
    apply_heuristics(internal_series, program_enrolment, low_bound, high_bound)

    # Verify that internal_series assignment was valid
    status = verify_intermediate(internal_series, schedule, low_bound, high_bound)
    if status is not Status.GOOD:
        raise Exception(f"Algorithm 2 failed to produce an output: {status}")

    # Translate internal_series into schedule object
    output_schedule = post_process(internal_series, schedule)

    # Verify final schedule object
    status = verify_final(output_schedule, schedule)
    if status is not Status.GOOD:
        raise Exception(f"Algorithm 2 failed to produce an output: {status}")

    # Return schedule to caller
    return output_schedule
