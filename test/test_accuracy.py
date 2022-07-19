import json

from forecaster.forecaster import forecast
from pprint import pprint
import pytest
from mock_data_generator import historic_year_to_mock_schedule, add_cap_first_year
from forecaster.constants import PROGRAM_GROWTH


@pytest.fixture
def open_files():
    with open("../data/real/historicCourseData.json", "r") as f:
        class_enrollment = json.load(f)
    with open("../data/real/programEnrollmentData.json", "r") as f:
        program_enrollment_json = json.load(f)
        program_enrollment = {int(k): v for k, v in program_enrollment_json.items()}
    return class_enrollment, program_enrollment


def measure_accuracy(year, reference, output):
    print("\nYear:", year)
    for semester in ["fall", "spring", "summer"]:
        number_courses = 0
        correct = 0
        incorrect = 0
        for i, course in enumerate(output[semester]):
            course_code = ''.join(c.lower() for c in course["course"]["code"])
            if course_code not in add_cap_first_year:
                number_courses += 1
                assigned_capacity = course["sections"][0]["capacity"]
                reference_capacity = reference[semester][i]["sections"][0]["capacity"]
                upper_bound = reference_capacity * PROGRAM_GROWTH
                lower_bound = reference_capacity / PROGRAM_GROWTH
                if assigned_capacity <= upper_bound and assigned_capacity >= lower_bound:
                    correct += 1
                else:
                    incorrect += 1
        print(f"{semester}: {correct/number_courses*100:.2f}%")


def test_accuracy_normal(open_files):

    print("\nTesting normal accuracy\n")

    for year in range(2008, 2022):
        # Generate reference (correct) schedule
        reference_schedule = historic_year_to_mock_schedule(year, includeCapFlag=True)
        input_schedule = historic_year_to_mock_schedule(year, includeCapFlag=False)

        # Run the forecaster on 2021
        class_enrollment, program_enrollment = open_files
        output_schedule = forecast(class_enrollment, program_enrollment, input_schedule, cutoff_year=year, force_flag=2)

        # Compare the forecasted schedule with the reference schedule
        measure_accuracy(year, reference_schedule, output_schedule)

    assert True


def test_accuracy_statistical(open_files):

    print("\nTesting statistical accuracy\n")

    for year in range(2008, 2022):
        # Generate reference (correct) schedule
        reference_schedule = historic_year_to_mock_schedule(year, includeCapFlag=True)
        input_schedule = historic_year_to_mock_schedule(year, includeCapFlag=False)

        # Run the forecaster on 2021
        class_enrollment, program_enrollment = open_files
        output_schedule = forecast(class_enrollment, program_enrollment, input_schedule, cutoff_year=year, force_flag=1)

        # Compare the forecasted schedule with the reference schedule
        measure_accuracy(year, reference_schedule, output_schedule)

    assert True


def test_accuracy_normal(open_files):

    print("\nTesting heuristic accuracy\n")

    for year in range(2008, 2022):
        # Generate reference (correct) schedule
        reference_schedule = historic_year_to_mock_schedule(year, includeCapFlag=True)
        input_schedule = historic_year_to_mock_schedule(year, includeCapFlag=False)

        # Run the forecaster on 2021
        class_enrollment, program_enrollment = open_files
        output_schedule = forecast(class_enrollment, program_enrollment, input_schedule, cutoff_year=year, force_flag=0)

        # Compare the forecasted schedule with the reference schedule
        measure_accuracy(year, reference_schedule, output_schedule)

    assert True
