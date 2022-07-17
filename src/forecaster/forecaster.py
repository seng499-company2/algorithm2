import json
import sys
import os
import logging
import time

from .preprocessor import pre_process, compute_bounds, validate_inputs
from .determination import determine_approach
from .statistical import apply_auto_arima
from .heuristic import apply_heuristics
from .guarantor import verify_intermediate, verify_final, Status
from .postprocessor import post_process


def forecast(course_enrolment: dict, program_enrolment: dict, schedule: dict, force_flag: int = 2,
             logging_level: int = logging.INFO) -> str:
    """ The forecast method will assign capacities to each course offering
    in the provided schedule object. It will use historical program and course
    enrollment data provided from JSON files to make determination about each
    course capacity.

    :param course_enrolment: python object loaded from course enrollment file
    :param program_enrolment: python objected loaded from program enrollment file
    :param schedule: common object shared with alg-1 representing course offerings
    :param force_flag: Forces the forecaster to use heuristics(0), or auto-arima (1) [0:Heuristics, 1:Arima, 2:auto,]
    :param logging_level: The level to log at, from logging, [Debug, Info, Warning, Errors, Critical]
    :return: JSON encoding of schedule object with capacities assigned
    """
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging_level)
    start_time = time.perf_counter()

    if course_enrolment is None:
        logging.warning('No course enrolment given, using static data')
        course_file = open(os.path.join(os.path.dirname(__file__), 'static_files/historicCourses.json'))
        course_enrolment  = json.load(course_file)
        course_file.close()

    if program_enrolment is None:
        logging.warning('No program enrolment given, using static data')
        enrollment_file = open(os.path.join(os.path.dirname(__file__), 'static_files/programEnrollmentData.json'))
        program_enrolment_json  = json.load(enrollment_file)
        program_enrolment = {int(k): v for k, v in program_enrolment_json.items()}
        enrollment_file.close()      
    else:
        program_enrolment = {int(k): v for k, v in program_enrolment.items()}

    if schedule is None:
        logging.warning('No schedule given, using static data')
        schedule_file = open(os.path.join(os.path.dirname(__file__), 'static_files/testSchedule.json'))
        schedule  = json.load(schedule_file)
        schedule_file.close()        

    # Validate inputs
    valid, error = validate_inputs(course_enrolment, program_enrolment, schedule)
    if not valid:
        raise ValueError(error)
    logging.info('Input Valid')

    # Preprocessing steps, generate internal data series
    logging.info('Preprocessing')
    low_bound, high_bound = compute_bounds(program_enrolment)
    internal_series = pre_process(course_enrolment, schedule)

    # Determine approach and assign course capacities
    logging.info('Determing Approach')
    determine_approach(internal_series, force_flag)

    logging.info('Statistical Forecasting')
    apply_auto_arima(internal_series)

    logging.info('Heuristic Forecasting')
    apply_heuristics(internal_series, program_enrolment, low_bound, high_bound)

    # Verify that internal_series assignment was valid
    logging.info('Verifying Intermediate Output')
    status = verify_intermediate(internal_series, schedule, low_bound, high_bound)
    if status is not Status.GOOD:
        raise Exception(f"Algorithm 2 failed to produce an output: {status}")

    # Translate internal_series into schedule object
    logging.info('Postprocessing')
    output_schedule = post_process(internal_series, schedule)

    # Verify final schedule object
    logging.info('Verifying Final Output')
    status = verify_final(output_schedule, schedule)
    if status is not Status.GOOD:
        raise Exception(f"Algorithm 2 failed to produce an output: {status}")

    # Return schedule to caller
    logging.info("Algorithm 2 Took: " + str(round(time.perf_counter() - start_time, 2)) + " Seconds")
    return output_schedule
