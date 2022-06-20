import pytest
import json
from forecaster import preprocessor


def test_compute_bounds():
    with open("../data/programEnrollmentData.json", "r") as fb:
        x = json.load(fb)
    low_bound, high_bound = preprocessor.compute_bounds(x[0])
    assert low_bound == 352
    assert high_bound == 2112


def test_preprocessor():
    data = preprocessor.pre_process({})
    assert data["CSC110-F"]["data"] == [0, 0, 500, 200, 400]
    assert data["CSC110-F"]["approach"] == 0
    assert data["CSC110-F"]["capacity"] == 500
