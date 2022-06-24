from forecaster.forecaster import apply_auto_arima

def test_auto_arima():
    
    test_dict = {"CSC110-F": {"data": [0, 0, 500, 200, 400, 300, 150, 200, 220, 175, 124, 221, 175, 200], "approach": 1, "capacity": 500}}
    apply_auto_arima(test_dict)
    
    
