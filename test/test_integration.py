import pytest
import json
from forecaster import constants
from forecaster import determination
from forecaster import guarantor
from forecaster import heuristic
from forecaster import postprocessor
from forecaster import preprocessor
from forecaster import statistical
from mock_data_generator import mock_data_generator
from mock_data_generator import generate_course_enrollment


def test_module_integration():
    schedule_test = json.load(open('../data/mock/mockSchedule2.json', 'r'))
    course_enrollment_test = json.load(open('../data/mock/mockHistoricCourseData2.json', 'r'))
    program_enrolment = json.load(open('../data/real/programEnrollmentData.json', 'r'))

    low_bound, high_bound = preprocessor.compute_bounds(program_enrolment)

    assert low_bound == 352*4
    assert high_bound == 2112*4

    internal_obj = preprocessor.pre_process(course_enrollment_test, schedule_test)

    assert internal_obj == {'CSC225-F': {'data': [10, 10, 10, 10, 30], 'approach': 0, 'capacity': 0},
                            'CSC226-F': {'data': [0, 10, 10, 30, 10], 'approach': 0, 'capacity': 0},
                            'CSC320-SP': {'data': None, 'approach': 0, 'capacity': 40},
                            'CSC360-SU': {'data': [10, 30 ,10, 10], 'approach': 0, 'capacity': 0},
                            'CSC370-SU': {'data': None, 'approach': 0, 'capacity': 100},
                            }

    determination.determine_approach(internal_obj)
    
    assert internal_obj['CSC225-F']['approach'] == 1
    assert internal_obj['CSC226-F']['approach'] == 0
    assert internal_obj['CSC320-SP']['approach'] == 0
    assert internal_obj['CSC360-SU']['approach'] == 0
    assert internal_obj['CSC370-SU']['approach'] == 0

    statistical.apply_auto_arima(internal_obj)

    arima_capacity = internal_obj['CSC225-F']['capacity']
    assert  arima_capacity > 0

    heuristic.apply_heuristics(internal_obj, program_enrolment, low_bound, high_bound)

    assert internal_obj['CSC225-F']['capacity'] == arima_capacity
    assert internal_obj['CSC226-F']['capacity'] > 0
    assert internal_obj['CSC320-SP']['capacity'] == 40
    assert internal_obj['CSC360-SU']['capacity'] > 0
    assert internal_obj['CSC370-SU']['capacity'] == 100

    status = guarantor.verify_intermediate(internal_obj, schedule_test, low_bound, high_bound)

    assert status == guarantor.Status.GOOD

    output_schedule = postprocessor.post_process(internal_obj, schedule_test)
    actual_capacity_sec1 = output_schedule['fall'][1]['sections'][0]['capacity']
    actual_capacity_sec2 = output_schedule['fall'][1]['sections'][1]['capacity']

    assert actual_capacity_sec1 > 0
    assert actual_capacity_sec2 > 0

    status = guarantor.verify_final(output_schedule, schedule_test)

    assert status == guarantor.Status.GOOD

