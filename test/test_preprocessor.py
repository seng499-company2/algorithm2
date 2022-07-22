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

    assert data == {'CSC225-F': {'data': [250, 250, 250, 750], 'approach': 0, 'capacity': 0},
                    'CSC226-F': {'data': [250, 250, 750, 250], 'approach': 0, 'capacity': 0},
                    'CSC320-SP': {'data': None, 'approach': 0, 'capacity': 40},
                    'CSC360-SU': {'data': [250, 750, 250, 250], 'approach': 0, 'capacity': 0},
                    'CSC370-SU': {'data': None, 'approach': 0, 'capacity': 100},
                    }


def test_validate_input_invalid_course_enrolment():
    schedule_test = mock_data_generator(['CSC225','SENG275'],['CSC226'],['CSC230'], 1, 1)
    program_enrollment_test = json.load(open('../data/real/programEnrollmentData.json', 'r'))
    
    course_enrollment_test = {'key1':'value1'}
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'Expected historical course enrollment to be a list not' in error
 
    course_enrollment_test = ['offering']
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'Expected offering to be a dict not' in error

    offering = {"enrollment": 0, "subjectCourse": "CSC105"}
    course_enrollment_test = [offering]
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'No "term" field in course offering' in error

    offering = {"term": "202301", "subjectCourse": "CSC105"}
    course_enrollment_test = [offering]
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'No "enrollment" field in course offering' in error

    offering = {"term": "202301", "enrollment": 0}
    course_enrollment_test = [offering]
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'No "subjectCourse" field in course offering' in error

    offering = {"term": 202301,
                "enrollment": 0,
                "subjectCourse": "CSC105"
                }
    course_enrollment_test = [offering]
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'Expected "term" field to be string not' in error

    offering = {"term": '202301',
                "enrollment": '0',
                "subjectCourse": "CSC105"
                }
    course_enrollment_test = [offering]
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'Expected "enrollment" field to be int not' in error

    offering = {"term": '202301',
                "enrollment": 0,
                "subjectCourse": 1
                }
    course_enrollment_test = [offering]
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'Expected "subjectCourse" field to be string not' in error


def test_validate_input_invalid_program_enrolment():
    schedule_test = mock_data_generator(['CSC225','SENG275'],['CSC226'],['CSC230'], 1, 1)
    course_enrollment_test = generate_course_enrollment(['CSC225','SENG275'] ,
                                                        ['CSC226'], 
                                                        ['CSC230'], 
                                                        ['202109', '202201', '202205', '202209', '202301'])
    program_enrollment_test = []
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'Expected historical program enrollment to be a dict not' in error

    program_enrollment_test = {"2014":[]}
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'Expected yearly enrollment item to be a dict not' in error

    program_enrollment_test = {"2014" :{ 
                                        "2" : 68,
                                        "2T" : 8,
                                        "3" : 54,
                                        "4" : 21,
                                        "5" : 17,
                                        "6" : 4,
                                        "7" : 1
                                        }
                                }
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'No "1" field in ' in error

    program_enrollment_test = {"2014" :{ "1" : 84,
                                        "2T" : 8,
                                        "3" : 54,
                                        "4" : 21,
                                        "5" : 17,
                                        "6" : 4,
                                        "7" : 1
                                        }
                                }
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'No "2" field in ' in error

    program_enrollment_test = {"2014" :{ "1" : 84,
                                        "2" : 68,
                                        "3" : 54,
                                        "4" : 21,
                                        "5" : 17,
                                        "6" : 4,
                                        "7" : 1
                                        }
                                }
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'No "2T" field in ' in error

    program_enrollment_test = {"2014" :{ "1" : 84,
                                        "2" : 68,
                                        "2T" : 54,
                                        "4" : 21,
                                        "5" : 17,
                                        "6" : 4,
                                        "7" : 1
                                        }
                                }
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'No "3" field in ' in error

    program_enrollment_test = {"2014" :{ "1" : 84,
                                        "2" : 68,
                                        "2T" : 54,
                                        "3" : 21,
                                        "5" : 17,
                                        "6" : 4,
                                        "7" : 1
                                        }
                                }
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'No "4" field in ' in error

    program_enrollment_test = {"2014" :{ "1" : 84,
                                        "2" : 68,
                                        "2T" : 54,
                                        "3" : 21,
                                        "4" : 17,
                                        "6" : 4,
                                        "7" : 1
                                        }
                                }
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'No "5" field in ' in error

    program_enrollment_test = {"2014" :{ "1" : 84,
                                        "2" : 68,
                                        "2T" : 54,
                                        "3" : 21,
                                        "4" : 17,
                                        "5" : 4,
                                        "7" : 1
                                        }
                                }
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'No "6" field in ' in error

    program_enrollment_test = {"2014" :{ "1" : 84,
                                        "2" : 68,
                                        "2T" : 54,
                                        "3" : 21,
                                        "4" : 17,
                                        "5" : 4,
                                        "6" : 1
                                        }
                                }
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'No "7" field in ' in error

    program_enrollment_test = {"2014" :{ "1" : '84',
                                        "2" : 68,
                                        "2T" : 8,
                                        "3" : 54,
                                        "4" : 21,
                                        "5" : 17,
                                        "6" : 4,
                                        "7" : 1
                                        }
                                }
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'Expected "1" field to be int not' in error

    program_enrollment_test = {"2014" :{ "1" : 84,
                                        "2" : '68',
                                        "2T" : 8,
                                        "3" : 54,
                                        "4" : 21,
                                        "5" : 17,
                                        "6" : 4,
                                        "7" : 1
                                        }
                                }
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'Expected "2" field to be int not' in error

    program_enrollment_test = {"2014" :{ "1" : 84,
                                        "2" : 68,
                                        "2T" : '8',
                                        "3" : 54,
                                        "4" : 21,
                                        "5" : 17,
                                        "6" : 4,
                                        "7" : 1
                                        }
                                }
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'Expected "2T" field to be int not' in error

    program_enrollment_test = {"2014" :{ "1" : 84,
                                        "2" : 68,
                                        "2T" : 8,
                                        "3" : '54',
                                        "4" : 21,
                                        "5" : 17,
                                        "6" : 4,
                                        "7" : 1
                                        }
                                }
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'Expected "3" field to be int not' in error

    program_enrollment_test = {"2014" :{ "1" : 84,
                                        "2" : 68,
                                        "2T" : 8,
                                        "3" : 54,
                                        "4" : '21',
                                        "5" : 17,
                                        "6" : 4,
                                        "7" : 1
                                        }
                                }
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'Expected "4" field to be int not' in error

    program_enrollment_test = {"2014" :{ "1" : 84,
                                        "2" : 68,
                                        "2T" : 8,
                                        "3" : 54,
                                        "4" : 21,
                                        "5" : '17',
                                        "6" : 4,
                                        "7" : 1
                                        }
                                }
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'Expected "5" field to be int not' in error

    program_enrollment_test = {"2014" :{ "1" : 84,
                                        "2" : 68,
                                        "2T" : 8,
                                        "3" : 54,
                                        "4" : 21,
                                        "5" : 17,
                                        "6" : '4',
                                        "7" : 1
                                        }
                                }
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'Expected "6" field to be int not' in error

    program_enrollment_test = {"2014" :{ "1" : 84,
                                        "2" : 68,
                                        "2T" : 8,
                                        "3" : 54,
                                        "4" : 21,
                                        "5" : 17,
                                        "6" : 4,
                                        "7" : '1'
                                        }
                                }
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'Expected "7" field to be int not' in error


def test_validate_input_invalid_schedule():
    course_enrollment_test = generate_course_enrollment(['CSC225','SENG275'] ,
                                                        ['CSC226'], 
                                                        ['CSC230'], 
                                                        ['202109', '202201', '202205', '202209', '202301'])
    program_enrollment_test = json.load(open('../data/real/programEnrollmentData.json', 'r'))

    schedule_test = [] 
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'Expected schedule to be a dict not' in error

    schedule_test = {'mid_summer':[]} 
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'Expected "fall", "spring", or "summer" field not' in error

    schedule_test = {'fall':{}} 
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'Expected term to be a list not' in error


    schedule_test = {'fall':['offering']} 
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'Expected offering to be a dict not' in error

    # offering = {sections':[{'capacity':1015, 'max_capacity':1015}]}
    offering = {'sections':[{'capacity':1015}]}
    schedule_test = {'fall':[offering]} 
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'No "course" field in course offering' in error

    offering = {'course':{'code':'CHEM101'}}
    schedule_test = {'fall':[offering]} 
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'No "sections" field in course offering' in error

    # offering = {'course':[]
    #             'sections':[{'capacity':1015, 'max_capacity':1015}]
    #             }
    offering = {'course':[],
                'sections':[{'capacity':1015}]
                }
    schedule_test = {'fall':[offering]} 
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'Expected offerings "course" field to be a dict not' in error

    offering = {'course':{'code':'CHEM101'},
                'sections':{}
                }
    schedule_test = {'fall':[offering]} 
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'Expected offerings "sections" field to be a list' in error

    offering = {'course':{},
                'sections':[]
                }
    schedule_test = {'fall':[offering]} 
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'Expected "code" field in course' in error

    offering = {'course':{'code':100},
                'sections':[]}
    schedule_test = {'fall':[offering]} 
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'Expected "code" field to be a string not' in error

    offering = {'course':{'code':'CHEM101'},
                'sections':['section']
                }
    schedule_test = {'fall':[offering]} 
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'Expected section to be a dict not' in error

    offering = {'course':{'code':'CHEM101'},
                'sections':[{}]
                }
    schedule_test = {'fall':[offering]} 
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'Expected "capacity" field to be in section' in error

    # offering = {'course':{'code':'CHEM101'}
    #             'sections':[{'capacity':1015}]
    #             }
    # schedule_test = {'fall':[offering]} 
    # valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    # assert not valid
    # assert 'Expected "max_capacity" field to be in section' in error

    offering = {'course':{'code':'CHEM101'},
                'sections':[{'capacity':'1015'}]
                }
    schedule_test = {'fall':[offering]} 
    valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    assert not valid
    assert 'Expected capacity to be a int not' in error

    # offering = {'course':{'code':'CHEM101'}
    #             'sections':[{'capacity':'1015', 'max_capacity':'1015'}]
    #             }
    # schedule_test = {'fall':[offering]} 
    # valid, error = preprocessor.validate_inputs(course_enrollment_test, program_enrollment_test, schedule_test)

    # assert not valid
    # assert 'Expected max_capacity to be a int not' in error



