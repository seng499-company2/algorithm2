import pytest
import json
from forecaster import determination

def test_valid():
    internal_obj = {"CSC110-F": {"data": [100, 200, 500, 200, 400, 100, 200, 500, 200, 400], "approach": 0, "capacity": 0}}
    determination.determine_approach(internal_obj)
    assert internal_obj["CSC110-F"]["approach"] == 1


def test_valid_without_most_recent_year():
    internal_obj = {"CSC110-F": {"data": [100, 200, 500, 200, 400, 100, 200, 500, 200, 0], "approach": 0, "capacity": 0}}
    determination.determine_approach(internal_obj)
    assert internal_obj["CSC110-F"]["approach"] == 1


def test_valid_without_most_recent_two_years():
    internal_obj = {"CSC110-F": {"data": [100, 200, 500, 200, 400, 100, 200, 500, 0, 0], "approach": 0, "capacity": 0}}
    determination.determine_approach(internal_obj)
    assert internal_obj["CSC110-F"]["approach"] == 1


def test_invalid_recent_year():
    internal_obj = {"CSC110-F": {"data": [100, 200, 500, 200, 400, 100, 100, 0, 0, 0], "approach": 0, "capacity": 0}}
    determination.determine_approach(internal_obj)
    assert internal_obj["CSC110-F"]["approach"] == 0


def test_invalid_min_data_points_middle_boundary():
    internal_obj = {"CSC110-F": {"data": [0, 0, 0, 0, 0, 0, 0, 100, 100, 100], "approach": 0, "capacity": 0}}
    determination.determine_approach(internal_obj)
    assert internal_obj["CSC110-F"]["approach"] == 0


def test_invalid_min_data_points_upper_boundary():
    internal_obj = {"CSC110-F": {"data": [0, 0, 0, 0, 0, 0, 100, 100, 100, 100], "approach": 0, "capacity": 0}}
    determination.determine_approach(internal_obj)
    assert internal_obj["CSC110-F"]["approach"] == 0


def test_valid_min_data_points_upper_boundary():
    internal_obj = {"CSC110-F": {"data": [0, 0, 0, 0, 0, 100, 100, 100, 100, 100], "approach": 0, "capacity": 0}}
    determination.determine_approach(internal_obj)
    assert internal_obj["CSC110-F"]["approach"] == 1
