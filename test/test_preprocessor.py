import pytest
import json
from forecaster import preprocessor
from mock_data_generator import mock_data_generator
from mock_data_generator import generate_course_enrollment


def test_compute_bounds():
    with open("../data/real/programEnrollmentData.json", "r") as fb:
        x_json = json.load(fb)
        x = {int(k): v for k, v in x_json.items()}
    low_bound, high_bound = preprocessor.compute_bounds(x)
    assert low_bound == 1408
    assert high_bound == 8448


def test_get_historical_term_codes():
    course_enrollment_test = generate_course_enrollment(['CSC225','SENG275'],['CSC226'],['CSC230'],['202109', '202201', '202205', '202209', '202301'])

    historical_term_codes = preprocessor.get_historical_term_codes(course_enrollment_test)
    assert historical_term_codes == {'fall': ['202109', '202209'], 
                                    'spring': ['202201','202301'], 
                                    'summer': ['202205']}


def test_remove_dups():
    list1 = [1,1,2,2,3,4]
    list2 = preprocessor.remove_dups(list1)
    list3 = ['a','a','b','b','c','d']
    list4 = preprocessor.remove_dups(list3)

    assert list2 == [1,2,3,4]
    assert list4 == ['a','b','c','d']


def test_get_set_of_course_codes():
    schedule_test = mock_data_generator(['CSC225','SENG275'],['CSC226'],['CSC230'], 1, 1)
    set_of_courses = preprocessor.get_set_of_course_codes(schedule_test)

    assert set_of_courses == {'CSC225','SENG275','CSC226','CSC230'}


def test_is_course_in_term():
    schedule_test = mock_data_generator(['CSC225','SENG275'],['CSC226'],['CSC230'], 1, 1)

    assert preprocessor.is_course_in_term('CSC225', schedule_test['fall'])
    assert preprocessor.is_course_in_term('SENG275', schedule_test['fall'])
    assert not preprocessor.is_course_in_term('CSC226', schedule_test['fall'])
    assert preprocessor.is_course_in_term('CSC226', schedule_test['spring'])
    assert preprocessor.is_course_in_term('CSC230', schedule_test['summer'])

def test_get_capacity():
    schedule_test = mock_data_generator(['CSC225','SENG275'],['CSC226'],['CSC230'], 1, 1)
    section_template = {'professor': '', 'capacity': '10'}
    schedule_test['fall'][0]['sections'].append(section_template)
    schedule_test['fall'][0]['sections'].append(section_template)

    capacity = preprocessor.get_capacity('CSC225', schedule_test['fall'])

    assert capacity == 20


def test_preprocessor():
    schedule_test = mock_data_generator(['CSC225','SENG275'],['CSC226'],['CSC230'], 1, 1)
    course_enrollment_test = generate_course_enrollment(['CSC225','SENG275'] ,
                                                        ['CSC226'], 
                                                        ['CSC230'], 
                                                        ['202109', '202201', '202205', '202209', '202301'])
    data = preprocessor.pre_process(course_enrollment_test, schedule_test)

    assert data == {'CSC225-F': {'data': [1, 1], 'approach': 0, 'capacity': 0},
                    'SENG275-F': {'data': [1, 1], 'approach': 0, 'capacity': 0},
                    'CSC226-SP': {'data': [1, 1], 'approach': 0, 'capacity': 0},
                    'CSC230-SU': {'data': [1], 'approach': 0, 'capacity': 0},
                    }

def test_preprocessor_advanced():
    schedule_test = json.load(open('../data/mock/mockSchedule2.json', 'r'))
    course_enrollment_test = json.load(open('../data/mock/mockHistoricCourseData.json', 'r'))

    data = preprocessor.pre_process(course_enrollment_test, schedule_test)

    assert data == {'CSC225-F': {'data': [10, 10, 10, 30], 'approach': 0, 'capacity': 0},
                    'CSC226-F': {'data': [10, 10, 30, 10], 'approach': 0, 'capacity': 0},
                    'CSC320-SP': {'data': None, 'approach': 0, 'capacity': 40},
                    'CSC360-SU': {'data': [10, 30,10, 10], 'approach': 0, 'capacity': 0},
                    'CSC370-SU': {'data': None, 'approach': 0, 'capacity': 100},
                    }

