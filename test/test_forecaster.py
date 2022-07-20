import json
from forecaster.forecaster import forecast
import pytest


def test_forecast():
    with open("../data/mock/2021Schedule.json", "r") as f:
        schedule = json.load(f)
    with open("../data/real/historicCourseData.json", "r") as f:
        class_enrollment = json.load(f)
    with open("../data/real/programEnrollmentData.json", "r") as f:
        program_enrollment_json = json.load(f)
        program_enrollment = {int(k): v for k, v in program_enrollment_json.items()}
    schedule = forecast(class_enrollment,program_enrollment,schedule)


def test_forecast_with_none_class_enrollment():
    with open("../data/mock/2021Schedule.json", "r") as f:
        schedule = json.load(f)
    with open("../data/real/historicCourseData.json", "r") as f:
        class_enrollment = json.load(f)
    with open("../data/real/programEnrollmentData.json", "r") as f:
        program_enrollment_json = json.load(f)
        program_enrollment = {int(k): v for k, v in program_enrollment_json.items()}
    schedule = forecast(None,program_enrollment,schedule)


def test_forecast_with_none_program_enrollment():
    with open("../data/mock/2021Schedule.json", "r") as f:
        schedule = json.load(f)
    with open("../data/real/historicCourseData.json", "r") as f:
        class_enrollment = json.load(f)
    with open("../data/real/programEnrollmentData.json", "r") as f:
        program_enrollment_json = json.load(f)
        program_enrollment = {int(k): v for k, v in program_enrollment_json.items()}
    schedule = forecast(class_enrollment,None,schedule)


def test_forecast_with_none_schedule():
    with open("../data/mock/2021Schedule.json", "r") as f:
        schedule = json.load(f)
    with open("../data/real/historicCourseData.json", "r") as f:
        class_enrollment = json.load(f)
    with open("../data/real/programEnrollmentData.json", "r") as f:
        program_enrollment_json = json.load(f)
        program_enrollment = {int(k): v for k, v in program_enrollment_json.items()}
    schedule = forecast(class_enrollment,program_enrollment,None)


def test_forecast_with_all_none():
    with open("../data/mock/2021Schedule.json", "r") as f:
        schedule = json.load(f)
    with open("../data/real/historicCourseData.json", "r") as f:
        class_enrollment = json.load(f)
    with open("../data/real/programEnrollmentData.json", "r") as f:
        program_enrollment_json = json.load(f)
        program_enrollment = {int(k): v for k, v in program_enrollment_json.items()}
    schedule = forecast(None,None,None)


def test_forcaster_with_invalid_input():
    with open("../data/real/historicCourseData.json", "r") as f:
        class_enrollment = json.load(f)
    with open("../data/real/programEnrollmentData.json", "r") as f:
        program_enrollment_json = json.load(f)
        program_enrollment = {int(k): v for k, v in program_enrollment_json.items()}
    schedule = []

    with pytest.raises(ValueError) as exc_info:
        schedule = forecast(class_enrollment, program_enrollment, schedule)

    exception_raised = str(exc_info)
    assert 'Expected schedule to be a dict not' in exception_raised
    

