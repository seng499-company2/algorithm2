import pytest
import json
from forecaster import preprocessor


def test_computeBounds():
    low_bound, high_bound = preprocessor.compute_bounds({})
    assert low_bound == 0
    assert high_bound == 100


def test_preprocessor():
    data = preprocessor.pre_process({})
    assert data["CSC110-F"]["data"] == [0, 0, 500, 200, 400]
    assert data["CSC110-F"]["approach"] == 0
    assert data["CSC110-F"]["capacity"] == 500
