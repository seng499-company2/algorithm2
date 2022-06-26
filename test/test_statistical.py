import pytest
from forecaster import statistical

def test_auto_arima_all():
    
    internal_series = {"CSC110-F": {"data": [0, 0, 500, 200, 400, 300, 150, 200, 220, 175, 124, 221, 175, 200], "approach": 1, "capacity": 0},
                       "CSC225-F": {"data": [0, 100, 500, 245, 234, 172, 150, 0, 110, 103, 124, 105, 127, 150], "approach": 1, "capacity": 0}}
    internal_series = statistical.apply_auto_arima(internal_series)
    
    capacity_1 = internal_series["CSC110-F"]["capacity"]
    capacity_2 = internal_series["CSC225-F"]["capacity"]
            
    assert isinstance(capacity_1, int)
    assert isinstance(capacity_2, int)
    assert capacity_1 > 0
    assert capacity_2 > 0
    

def test_auto_arima_none():
    
    internal_series = {"CSC110-F": {"data": [0], "approach": 1, "capacity": 0}}
    internal_series = statistical.apply_auto_arima(internal_series)
    
    capacity = internal_series["CSC110-F"]["capacity"]
    
    assert isinstance(capacity, int)
    
    
