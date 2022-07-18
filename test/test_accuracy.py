import json
from forecaster.forecaster import forecast
from pprint import pprint
import pytest
from mock_data_generator import historic_year_to_mock_schedule, add_cap_first_year
from forecaster.constants import PROGRAM_GROWTH

def measure_accuracy(reference, output):
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
                print()
                print(f"{semester} : {course_code}")
                print("Reference: ", reference_capacity, " Assigned: ", assigned_capacity)
                upper_bound = reference_capacity * 1.2
                lower_bound = reference_capacity / 1.2
                print(f"Upper bound: {upper_bound}")
                print(f"Lower bound: {lower_bound}")
                if assigned_capacity <= upper_bound and assigned_capacity >= lower_bound:
                    correct += 1
                    print("GOOD")
                else:
                    print("BAD")
                    incorrect += 1
            print()
        print(f"Semester {semester} has {correct} correct out of {number_courses}")
        print(f"Percetnage correct: {correct/number_courses}")


# def test_accuracy_heuristic():

#     print("\nTesting heuristic accuracy\n")
#     # Generate reference (correct) schedule
#     reference_schedule = historic_year_to_mock_schedule(2021, includeCapFlag=True)
#     input_schedule = historic_year_to_mock_schedule(2021, includeCapFlag=False)

#     # Run the forecaster on 2021
#     with open("../data/real/accuracy_test_historic_enrollment.json", "r") as f:
#         class_enrollment = json.load(f)
#     with open("../data/real/programEnrollmentData.json", "r") as f:
#         program_enrollment_json = json.load(f)
#         program_enrollment = {int(k): v for k, v in program_enrollment_json.items()}
#     output_schedule = forecast(class_enrollment, program_enrollment, input_schedule, force_flag=0)

#     # Compare the forecasted schedule with the reference schedule
#     measure_accuracy(reference_schedule, output_schedule)

#     assert True


# def test_accuracy_statistical():
#     print("\nTesting statistical accuracy\n")
#     # Generate reference (correct) schedule
#     reference_schedule = historic_year_to_mock_schedule(2021, includeCapFlag=True)
#     input_schedule = historic_year_to_mock_schedule(2021, includeCapFlag=False)

#     # Run the forecaster on 2021
#     with open("../data/real/accuracy_test_historic_enrollment.json", "r") as f:
#         class_enrollment = json.load(f)
#     with open("../data/real/programEnrollmentData.json", "r") as f:
#         program_enrollment_json = json.load(f)
#         program_enrollment = {int(k): v for k, v in program_enrollment_json.items()}
#     output_schedule = forecast(class_enrollment, program_enrollment, input_schedule, force_flag=1)

#     # Compare the forecasted schedule with the reference schedule
#     measure_accuracy(reference_schedule, output_schedule)

#     assert True


def test_accuracy_all():
    print("\nTesting All\n")
    # Generate reference (correct) schedule
    reference_schedule = historic_year_to_mock_schedule(2021, includeCapFlag=True)
    input_schedule = historic_year_to_mock_schedule(2021, includeCapFlag=False)

    # Run the forecaster on 2021
    with open("../data/real/accuracy_test_historic_enrollment.json", "r") as f:
        class_enrollment = json.load(f)
    with open("../data/real/programEnrollmentData.json", "r") as f:
        program_enrollment_json = json.load(f)
        program_enrollment = {int(k): v for k, v in program_enrollment_json.items()}
    output_schedule = forecast(class_enrollment, program_enrollment, input_schedule)

    # Compare the forecasted schedule with the reference schedule
    measure_accuracy(reference_schedule, output_schedule)

    assert True
