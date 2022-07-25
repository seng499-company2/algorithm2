import json

from forecaster.heuristic import apply_heuristics
from forecaster.preprocessor import compute_bounds


def test_apply_heuristics_all_data():
    internal_series = {"CSC110-F": {"data": [68, 81, 122, 115, 153], "approach": 0, "capacity": 0},
                       "CSC116-F": {"data": [0, 0, 91, 112, 130], "approach": 1, "capacity": 0},
                       "SENG265-F": {"data": [0, 91, 0, 129, 142], "approach": 0, "capacity": 0}}

    with open("../data/real/programEnrollmentData.json", "r") as fb:
        en_json = json.load(fb)
        en = {int(k): v for k, v in en_json.items()}

    apply_heuristics(internal_series, en)
    assert internal_series["CSC110-F"]["capacity"] == 159
    assert internal_series["CSC116-F"]["capacity"] == 135
    assert internal_series["SENG265-F"]["capacity"] == 148


def test_apply_heuristics_no_data():
    internal_series = {"CSC110-F": {"data": None, "approach": 0, "capacity": 0},
                       "CSC116-F": {"data": None, "approach": 1, "capacity": 0},
                       "SENG265-F": {"data": None, "approach": 0, "capacity": 0}}

    with open("../data/real/programEnrollmentData.json", "r") as fb:
        en_json = json.load(fb)
        en = {int(k): v for k, v in en_json.items()}

    apply_heuristics(internal_series, en)
    assert internal_series["CSC110-F"]["capacity"] == 100
    assert internal_series["CSC116-F"]["capacity"] == 100
    assert internal_series["SENG265-F"]["capacity"] == 80


def test_apply_heuristics_some_data():
    internal_series = {"CSC110-F": {"data": None, "approach": 0, "capacity": 0},
                       "CSC116-F": {"data": [124], "approach": 1, "capacity": 0},
                       "SENG265-F": {"data": None, "approach": 0, "capacity": 0}}

    with open("../data/real/programEnrollmentData.json", "r") as fb:
        en_json = json.load(fb)
        en = {int(k): v for k, v in en_json.items()}

    apply_heuristics(internal_series, en)
    assert internal_series["CSC110-F"]["capacity"] == 77
    assert internal_series["CSC116-F"]["capacity"] == 129
    assert internal_series["SENG265-F"]["capacity"] == 80