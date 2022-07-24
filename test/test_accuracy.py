import json
from forecaster.forecaster import forecast
import pytest
from mock_data_generator import historic_year_to_mock_schedule, add_cap_first_year
from forecaster.constants import RECENT_PROGRAM_GROWTH, OVERALL_PROGRAM_GROWTH
from math import ceil, sqrt
from statistics import mean, median


@pytest.fixture
def open_files():
    standard_deviation = {}
    with open("../data/real/historicCourseData.json", "r") as f:
        class_enrollment = json.load(f)
    with open("../data/real/programEnrollmentData.json", "r") as f:
        program_enrollment_json = json.load(f)
        program_enrollment = {int(k): v for k, v in program_enrollment_json.items()}
    with open("../data/courseMaxCapStaDev.csv", "r") as f:
        lines = f.readlines()
        for line in lines[1:]:
            line = line.split(",")
            standard_deviation[line[0]] = ceil(float(line[1]))
    return class_enrollment, program_enrollment, standard_deviation


def measure_accuracy(year, reference, output, deviation):
    sem = {"fall": "-F", "spring": "-SP", "summer": "-SU"}
    for semester in ["fall", "spring", "summer"]:
        print(f"\n{year} {semester.upper()} % ERROR:")
        number_courses = 0
        total_error = []
        correct = 0
        total_difference = []
        for i, course in enumerate(output[semester]):
            course_code = ''.join(c.lower() for c in course["course"]["code"])
            standard_code = course_code .upper() + sem[semester]
            if course_code not in add_cap_first_year:
                number_courses += 1
                assigned_capacity = course["sections"][0]["capacity"]
                reference_capacity = reference[semester][i]["sections"][0]["capacity"]
                difference = assigned_capacity - reference_capacity
                total_difference.append(difference)
                total_error.append(abs(difference) / reference_capacity)
                error = (difference / reference_capacity)*100
                if standard_code not in deviation.keys():
                    upper_bound = reference_capacity * OVERALL_PROGRAM_GROWTH
                    lower_bound = reference_capacity / OVERALL_PROGRAM_GROWTH
                else:
                    upper_bound = reference_capacity + deviation[standard_code]
                    lower_bound = reference_capacity - deviation[standard_code]
                if assigned_capacity <= upper_bound and assigned_capacity >= lower_bound:
                    correct += 1
                try:
                    print(f"{course_code.upper().ljust(4):9} {error:7.2f}%     assigned: {assigned_capacity:4}     reference: {reference_capacity:4}     std.dev: {deviation[standard_code]:4}")
                except KeyError:
                    print(f"{course_code.upper().ljust(4):9} {error:7.2f}%     assigned: {assigned_capacity:4}     reference: {reference_capacity:4}     std.dev: N/A")
            # except:
            #     print(f"{course_code.upper().ljust(4):9} {error:7.2f}%     assigned: {assigned_capacity:4}     reference: {reference_capacity:4}")
        print(f"\n{year} {semester.upper()} RESULTS:")
        print(f"Average seat difference: {mean([abs(x) for x in total_difference]):.2f}")
        print(f"Total seat difference: {sum(total_difference)}")
        print(f"Within Std. Dev.: {(correct/number_courses)*100:.2f}%")
        print(f"Mean % error: {mean(total_error)*100:.2f}%")
        print(f"Median % error: {median(total_error)*100:.2f}%")


def measure_root_mean_squared_error(year, reference, output):
    # MSE = 1/n * sum(for each n: (Y1-Y2)^2 ) where n=number of courses, Y1=actual value, Y2=predicted value
    print(f"Year:{year}")
    for semester in ["fall", "spring", "summer"]:
        result = 0
        number_courses = 0
        for i, course in enumerate(output[semester]):
            course_code = ''.join(c.lower() for c in course["course"]["code"])
            if course_code not in add_cap_first_year:
                number_courses += 1
                assigned_capacity = course["sections"][0]["capacity"]
                reference_capacity = reference[semester][i]["sections"][0]["capacity"]
                result += (reference_capacity - assigned_capacity)**2
        print(f"{semester} RMSE: {sqrt((1/number_courses) * (result)):.2f}") 
    print("\n") 


def measure_mean_squared_error(year, reference, output):
    # MSE = 1/n * sum(for each n: (Y1-Y2)^2 ) where n=number of courses, Y1=actual value, Y2=predicted value
    print(f"\nYEAR: {year}")
    for semester in ["fall", "spring", "summer"]:
        result = 0
        number_courses = 0
        total_seats = 0
        for i, course in enumerate(output[semester]):
            course_code = ''.join(c.lower() for c in course["course"]["code"])
            if course_code not in add_cap_first_year:
                number_courses += 1
                assigned_capacity = course["sections"][0]["capacity"]
                reference_capacity = reference[semester][i]["sections"][0]["capacity"]
                total_seats += assigned_capacity
                result += (reference_capacity - assigned_capacity)**2
        print(f"{semester.upper():7} MSE: {(1/number_courses) * (result):.2f}") 


def test_accuracy_normal(open_files):

    print("\n\n-----------------------")
    print("Testing Normal Accuracy")
    print("-----------------------\n")

    for year in range(2017, 2022):
        # Generate reference (correct) schedule
        reference_schedule = historic_year_to_mock_schedule(year, includeCapFlag=True)
        input_schedule = historic_year_to_mock_schedule(year, includeCapFlag=False)

        # Run the forecaster on 2021
        class_enrollment, program_enrollment, standard_deviation = open_files
        output_schedule = forecast(class_enrollment, program_enrollment, input_schedule, cutoff_year=year, force_flag=2)

        # Compare the forecasted schedule with the reference schedule
        measure_accuracy(year, reference_schedule, output_schedule, standard_deviation)

    assert True


def test_accuracy_heuristic(open_files):

    print("\n\n--------------------------")
    print("Testing Heuristic Accuracy")
    print("--------------------------\n")

    for year in range(2017, 2022):
        # Generate reference (correct) schedule
        reference_schedule = historic_year_to_mock_schedule(year, includeCapFlag=True)
        input_schedule = historic_year_to_mock_schedule(year, includeCapFlag=False)

        # Run the forecaster on 2021
        class_enrollment, program_enrollment, standard_deviation = open_files
        output_schedule = forecast(class_enrollment, program_enrollment, input_schedule, cutoff_year=year, force_flag=0)

        # Compare the forecasted schedule with the reference schedule
        measure_accuracy(year, reference_schedule, output_schedule, standard_deviation)

    assert True


def test_root_mean_squared_error(open_files):

    print("\n\n-----------------------")
    print("Testing RMSE")
    print("-----------------------\n")

    for year in range(2017, 2022):
        # Generate reference (correct) schedule
        reference_schedule = historic_year_to_mock_schedule(year, includeCapFlag=True)
        input_schedule = historic_year_to_mock_schedule(year, includeCapFlag=False)

        # Run the forecaster on 2021
        class_enrollment, program_enrollment, standard_deviation = open_files
        output_schedule = forecast(class_enrollment, program_enrollment, input_schedule, cutoff_year=year, force_flag=2)

        measure_root_mean_squared_error(year, reference_schedule, output_schedule)
    assert True


def test_mean_squared_error(open_files):

    print("\n\n--------------------")
    print("Testing MSE Accuracy")
    print("--------------------\n")

    for year in range(2017, 2022):
        # Generate reference (correct) schedule
        reference_schedule = historic_year_to_mock_schedule(year, includeCapFlag=True)
        input_schedule = historic_year_to_mock_schedule(year, includeCapFlag=False)

        # Run the forecaster on 2021
        class_enrollment, program_enrollment, standarad_deviation = open_files
        output_schedule = forecast(class_enrollment, program_enrollment, input_schedule, cutoff_year=year, force_flag=2)

        measure_mean_squared_error(year, reference_schedule, output_schedule)
    assert True