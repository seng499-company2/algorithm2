import pytest
import json
from forecaster import determination


def test_approach_determination():
    data = {"CSC110-F": {"data": [0, 0, 500, 200, 400], "approach": 0, "capacity": 500}}
    determination.determine_approach(data)

    assert data["CSC110-F"]["data"] == [0, 0, 500, 200, 400]
    assert data["CSC110-F"]["approach"] == 1
    assert data["CSC110-F"]["capacity"] == 500
