import json
import sys
from .preprocessor import preProcess, computeBounds
from .determination import determine_approach
from .statistical import apply_auto_arima
from .heuristic import apply_heuristics
from .guarantor import check_intermediate_validity, check_final_validity, Status
from .postprocessor import postProcess


def forecast(course_enrollment: dict, program_enrollment: dict, schedule: dict) -> str:
    lower_bound, upper_bound = computeBounds(program_enrollment)
    intermediate_course_object = preProcess(course_enrollment)

    determine_approach(intermediate_course_object)
    apply_auto_arima(intermediate_course_object)
    apply_heuristics(intermediate_course_object, lower_bound, upper_bound, program_enrollment)

    status = check_intermediate_validity(intermediate_course_object, schedule, lower_bound, upper_bound)
    if status is not Status.GOOD:
        raise Exception("Algorithm 2 failed to produce an output.")

    schedule = postProcess(intermediate_course_object, schedule)

    status = check_final_validity(schedule)
    if status is not Status.GOOD:
        raise Exception("Algorithm 2 failed to produce an output.")

    return json.dumps(schedule)
