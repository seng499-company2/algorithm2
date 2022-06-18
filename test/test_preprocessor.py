import pytest
import json
from forecaster import preprocessor


def test_computeBounds():
    lowerBound, upperBound = preprocessor.computeBounds({})
    assert lowerBound == 0
    assert upperBound == 100


def test_preProcessor():
    data = preprocessor.preProcess({})
    assert data["CSC110-F"]["data"]     == [0, 0, 500, 200, 400]
    assert data["CSC110-F"]["approach"] == 0
    assert data["CSC110-F"]["capacity"] == 500
