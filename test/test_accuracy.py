import json
from forecaster.forecaster import forecast
from pprint import pprint
import pytest


def test_accuracy():
    with open("../data/mock/2021Schedule.json", "r") as f:
        schedule = json.load(f)
    with open("../data/real/accuracy_test_historic_enrollment.json", "r") as f:
        class_enrollment = json.load(f)
    with open("../data/real/programEnrollmentData.json", "r") as f:
        program_enrollment_json = json.load(f)
        program_enrollment = {int(k): v for k, v in program_enrollment_json.items()}
    schedule = forecast(class_enrollment,program_enrollment,schedule)
    with open("../data/forecaster_test_output.json", "w") as f:
        json.dump(schedule, f)
    pprint(schedule)