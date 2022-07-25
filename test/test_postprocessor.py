import pytest
import json
import math
from forecaster import postprocessor
from mock_data_generator import mock_data_generator

# Valid test cases shouldn't cause any errors
def test_one_section():
    schedule_test   = mock_data_generator(["CSC225"], [], [], 1, 1)
    internal_object = {"CSC225-F": {"data": [], "approach": 0, "capacity": 500}}
    schedule        = postprocessor.post_process(internal_object, schedule_test)

    expected = internal_object["CSC225-F"]["capacity"]
    actual   = schedule['fall'][0]['sections'][0]['capacity']

    assert expected == actual, f"Expected {expected} Got {actual}"


def test_two_sections():
    schedule_test   = mock_data_generator(["CSC225"], [], [], 2, 2)
    internal_object = {"CSC225-F": {"data": [], "approach": 0, "capacity": 500}}
    schedule        = postprocessor.post_process(internal_object, schedule_test)

    expected_one = math.ceil(internal_object["CSC225-F"]["capacity"] * 0.75)
    expected_two = math.ceil(internal_object["CSC225-F"]["capacity"] * 0.25)

    actual_one = schedule['fall'][0]['sections'][0]['capacity']
    actual_two = schedule['fall'][0]['sections'][1]['capacity']

    assert expected_one == actual_one, f"Expected {expected_one} Got {actual_one}"
    assert expected_two == actual_two, f"Expected {expected_two} Got {actual_two}"


def test_three_sections():
    schedule_test   = mock_data_generator(["CSC225"], [], [], 3, 3)
    internal_object = {"CSC225-F": {"data": [], "approach": 0, "capacity": 500}}
    schedule        = postprocessor.post_process(internal_object, schedule_test)

    expected = math.ceil(internal_object["CSC225-F"]["capacity"] / 3)

    actual_one   = math.ceil(schedule['fall'][0]['sections'][0]['capacity'])
    actual_two   = math.ceil(schedule['fall'][0]['sections'][1]['capacity'])
    actual_three = math.ceil(schedule['fall'][0]['sections'][2]['capacity'])

    assert expected == actual_one,   f"Expected {expected} Got {actual_one}"
    assert expected == actual_two,   f"Expected {expected} Got {actual_two}"
    assert expected == actual_three, f"Expected {expected} Got {actual_three}"


def test_four_sections():
    schedule_test   = mock_data_generator(["CSC225"], [], [], 4, 4)
    internal_object = {"CSC225-F": {"data": [], "approach": 0, "capacity": 500}}
    schedule        = postprocessor.post_process(internal_object, schedule_test)

    expected = math.ceil(internal_object["CSC225-F"]["capacity"] / 4)

    actual_one   = math.ceil(schedule['fall'][0]['sections'][0]['capacity'])
    actual_two   = math.ceil(schedule['fall'][0]['sections'][1]['capacity'])
    actual_three = math.ceil(schedule['fall'][0]['sections'][2]['capacity'])
    actual_four  = math.ceil(schedule['fall'][0]['sections'][3]['capacity'])

    assert expected == actual_one,   f"Expected {expected} Got {actual_one}"
    assert expected == actual_two,   f"Expected {expected} Got {actual_two}"
    assert expected == actual_three, f"Expected {expected} Got {actual_three}"
    assert expected == actual_four,  f"Expected {expected} Got {actual_four}"


def test_multiple_terms():
    schedule_test   = mock_data_generator(["CSC225"], ["CSC225"], ["CSC225"], 1, 1)
    internal_object = {"CSC225-F":  {"data": [], "approach": 0, "capacity": 500},
                       "CSC225-SP": {"data": [], "approach": 0, "capacity": 200},
                       "CSC225-SU": {"data": [], "approach": 0, "capacity": 100}}
    schedule        = postprocessor.post_process(internal_object, schedule_test)

    expected_fall   = internal_object["CSC225-F"]["capacity"]
    actual_fall     = schedule['fall'][0]['sections'][0]['capacity']

    expected_spring = internal_object["CSC225-SP"]["capacity"]
    actual_spring   = schedule['spring'][0]['sections'][0]['capacity']

    expected_summer = internal_object["CSC225-SU"]["capacity"]
    actual_summer   = schedule['summer'][0]['sections'][0]['capacity']

    assert expected_fall   == actual_fall,   f"Expected {expected_fall}   Got {actual_fall}"
    assert expected_spring == actual_spring, f"Expected {expected_spring} Got {actual_spring}"
    assert expected_summer == actual_summer, f"Expected {expected_summer} Got {actual_summer}"

def test_max_capacity_one_section_true():
    schedule_test   = json.load(open('../data/mock/mockSchedule3.json', 'r'))
    internal_object = {'CSC225-F': {'data': [10, 10, 10, 30], 'approach': 0, 'capacity': 500},
                       'CSC226-F': {'data': [10, 10, 30, 10], 'approach': 0, 'capacity': 0},
                       'CSC391-F': {'data': None, 'approach': 0, 'capacity': 60},
                       'CSC320-SP': {'data': None, 'approach': 0, 'capacity': 40},
                       'CSC360-SU': {'data': [10, 30,10, 10], 'approach': 0, 'capacity': 0},
                       'CSC370-SU': {'data': None, 'approach': 0, 'capacity': 100},
                       'CSC381-SU': {'data': [0,0,0,0], 'approach': 0, 'capacity': 50}
                       }
    schedule        = postprocessor.post_process(internal_object, schedule_test)

    expected_one = '300' #assigned max cap
    expected_two = '60'
    actual_one = schedule['fall'][0]['sections'][0]['capacity']
    actual_two = schedule['fall'][2]['sections'][0]['capacity']

    assert expected_one == actual_one, f"Expected {expected_one} Got {actual_one}"
    assert expected_two == actual_two, f"Expected {expected_two} Got {actual_two}"
    
def test_max_capacity_one_section_false():
    schedule_test   = json.load(open('../data/mock/mockSchedule3.json', 'r'))
    internal_object = {'CSC225-F': {'data': [10, 10, 10, 30], 'approach': 0, 'capacity': 295},
                       'CSC226-F': {'data': [10, 10, 30, 10], 'approach': 0, 'capacity': 0},
                       'CSC391-F': {'data': None, 'approach': 0, 'capacity': 60},
                       'CSC320-SP': {'data': None, 'approach': 0, 'capacity': 40},
                       'CSC360-SU': {'data': [10, 30,10, 10], 'approach': 0, 'capacity': 0},
                       'CSC370-SU': {'data': None, 'approach': 0, 'capacity': 100},
                       'CSC381-SU': {'data': [0,0,0,0], 'approach': 0, 'capacity': 50}
                       }
    schedule        = postprocessor.post_process(internal_object, schedule_test)
   # print(schedule)
    expected = internal_object['CSC225-F']['capacity']
    actual   = schedule['fall'][0]['sections'][0]['capacity']

    assert expected == actual, f"Expected {expected} Got {actual}"
    
def test_max_capacity_two_sections_false():
    schedule_test   = json.load(open('../data/mock/mockSchedule3.json', 'r'))
    internal_object = {'CSC225-F': {'data': [10, 10, 10, 30], 'approach': 0, 'capacity': 500},
                       'CSC226-F': {'data': [10, 10, 30, 10], 'approach': 0, 'capacity': 40},
                       'CSC320-SP': {'data': None, 'approach': 0, 'capacity': 40},
                       'CSC360-SU': {'data': [10, 30,10, 10], 'approach': 0, 'capacity': 0},
                       'CSC370-SU': {'data': None, 'approach': 0, 'capacity': 100},
                       'CSC381-SU': {'data': [0,0,0,0], 'approach': 0, 'capacity': 50}
                       }
    schedule        = postprocessor.post_process(internal_object, schedule_test)

    expected_one = math.ceil(internal_object["CSC226-F"]["capacity"] * 0.75)
    expected_two = math.ceil(internal_object["CSC226-F"]["capacity"] * 0.25)
    
    actual_one = schedule['fall'][1]['sections'][0]['capacity']
    actual_two = schedule['fall'][1]['sections'][1]['capacity']
    
    assert expected_one == actual_one, f"Expected {expected_one} Got {actual_one}"
    assert expected_two == actual_two, f"Expected {expected_two} Got {actual_two}"
    
def test_max_capacity_two_sections_true():
    schedule_test   = json.load(open('../data/mock/mockSchedule3.json', 'r'))
    internal_object = {'CSC225-F': {'data': [10, 10, 10, 30], 'approach': 0, 'capacity': 500},
                       'CSC226-F': {'data': [10, 10, 30, 10], 'approach': 0, 'capacity': 40},
                       'CSC391-F': {'data': None, 'approach': 0, 'capacity': 60},
                       'CSC320-SP': {'data': [10, 10, 10, 20], 'approach': 0, 'capacity': 60},
                       'CSC360-SU': {'data': [10, 30,10, 10], 'approach': 0, 'capacity': 0},
                       'CSC370-SU': {'data': None, 'approach': 0, 'capacity': 100},
                       'CSC381-SU': {'data': [0,0,0,0], 'approach': 0, 'capacity': 50}
                       }
    schedule        = postprocessor.post_process(internal_object, schedule_test)

    expected_one = '10' #assigned max cap
    expected_two = math.ceil(internal_object["CSC320-SP"]["capacity"] * 0.25)
    
    expected_three = '30'
    expected_four = '20'
    
    actual_one = schedule['spring'][0]['sections'][0]['capacity']
    actual_two = schedule['spring'][0]['sections'][1]['capacity']
    
    actual_three = schedule['summer'][2]['sections'][0]['capacity']
    actual_four = schedule['summer'][2]['sections'][1]['capacity']
    
    assert expected_one == actual_one, f"Expected {expected_one} Got {actual_one}"
    assert expected_two == actual_two, f"Expected {expected_two} Got {actual_two}"
    
    assert expected_three == actual_three, f"Expected {expected_three} Got {actual_three}"
    assert expected_four == actual_four, f"Expected {expected_four} Got {actual_four}"