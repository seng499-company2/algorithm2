import json

from forecaster.heuristic import apply_heuristics
from forecaster.preprocessor import compute_bounds


def test_apply_heuristics_all_data():
    internal_series = {"CSC110-F": {"data": [68, 81, 122, 115, 153], "approach": 0, "capacity": 0},
                       "CSC116-F": {"data": [0, 0, 91, 112, 130], "approach": 1, "capacity": 0},
                       "SENG265-F": {"data": [0, 91, 0, 129, 142], "approach": 0, "capacity": 0}}

    with open("../data/real/programEnrollmentData.json", "r") as fb:
        en = json.load(fb)

    low, high = compute_bounds(en)
    apply_heuristics(internal_series, en, low, high)
    assert internal_series["CSC110-F"]["capacity"] == 166
    assert internal_series["CSC116-F"]["capacity"] == 141
    assert internal_series["SENG265-F"]["capacity"] == 154


def test_apply_heuristics_no_data():
    internal_series = {"CSC110-F": {"data": [0], "approach": 0, "capacity": 0},
                       "CSC116-F": {"data": [0], "approach": 1, "capacity": 0},
                       "SENG265-F": {"data": [0], "approach": 0, "capacity": 0}}

    with open("../data/real/programEnrollmentData.json", "r") as fb:
        en = json.load(fb)

    low, high = compute_bounds(en)
    apply_heuristics(internal_series, en, low, high)
    assert internal_series["CSC110-F"]["capacity"] == 2816
    assert internal_series["CSC116-F"]["capacity"] == 2816
    assert internal_series["SENG265-F"]["capacity"] == 2816


def test_apply_heuristics_some_data():
    internal_series = {"CSC110-F": {"data": [0], "approach": 0, "capacity": 0},
                       "CSC116-F": {"data": [124], "approach": 1, "capacity": 0},
                       "SENG265-F": {"data": [0], "approach": 0, "capacity": 0}}

    with open("../data/real/programEnrollmentData.json", "r") as fb:
        en = json.load(fb)

    low, high = compute_bounds(en)
    apply_heuristics(internal_series, en, low, high)
    assert internal_series["CSC110-F"]["capacity"] == 4157
    assert internal_series["CSC116-F"]["capacity"] == 134
    assert internal_series["SENG265-F"]["capacity"] == 4157
