import pytest
from forecaster import statistical

def test_auto_arima():
    
    internal_series = {"CSC110-F": {"data": [0, 0, 500, 200, 400, 300, 150, 200, 220, 175, 124, 221, 175, 200], "approach": 1, "capacity": 0}}
    internal_series = statistical.apply_auto_arima(internal_series)
    
    capacity = internal_series["CSC110-F"]["capacity"]
            
    assert capacity > 0
    
    
