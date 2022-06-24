import pytest
import json
from forecaster import preprocessor
from mock_data_generator import mock_data_generator


def generate_historial_offering(course: str, term: str, enrollment: int) -> dict:
    return {'term': term, 'enrollment': enrollment, 'subjectCourse': course}


def generate_course_enrollment(fall_courses: list, spring_courses: list, summer_courses: list, historical_terms: list) -> dict:
    course_enrollment = []
    for course_list in (fall_courses, spring_courses, summer_courses):
        for course in course_list:
            for historical_term in historical_terms:
                if((course_list == fall_courses) and (historical_term.endswith('09'))):
                    course_enrollment\
                    .append(generate_historial_offering(course, historical_term, 1))
                elif((course_list == spring_courses) and (historical_term.endswith('01'))):
                    course_enrollment\
                    .append(generate_historial_offering(course, historical_term, 1))
                elif((course_list == summer_courses) and (historical_term.endswith('05'))):
                    course_enrollment\
                    .append(generate_historial_offering(course, historical_term, 1))
    return course_enrollment


def test_computeBounds():
    low_bound, high_bound = preprocessor.compute_bounds({})
    assert low_bound == 0
    assert high_bound == 100


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

