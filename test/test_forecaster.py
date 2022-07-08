import json
from re import X

from forecaster.forecaster import forecast
from pprint import pprint


def test_forecast():
    with open("../data/mock/2021Schedule.json", "r") as f:
        schedule = json.load(f)
    with open("../data/real/historicCourseData.json", "r") as f:
        class_enrollment = json.load(f)
    with open("../data/real/programEnrollmentData.json", "r") as f:
        program_enrollment = json.load(f)
    schedule = forecast(class_enrollment, program_enrollment, schedule)
    with open("../data/output_schedule.json", "w") as f:
        f.write(json.dumps(schedule))
    assert schedule is not None
