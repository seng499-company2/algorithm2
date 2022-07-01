import json

from forecaster.forecaster import forecast


# def test_forecast():
#     with open("../data/mockSchedule2.json", "r") as f:
#         schedule = json.load(f)
#     with open("../data/historicCourseData.json", "r") as f:
#         class_enrollment = json.load(f)
#     with open("../data/programEnrollmentData.json", "r") as f:
#         program_enrollment = json.load(f)
#     schedule = forecast(class_enrollment, program_enrollment, schedule)
#     assert schedule is not None
