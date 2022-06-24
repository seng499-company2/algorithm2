from pmdarima.arima import auto_arima
import pandas as pd
import numpy as np

# statistical.py
# Author:
# Date: June 17th, 2022
# This module applies the auto-ARIMA method to predict course capacities
# Helper Functions
# Module API

def main():
    apply_auto_arima(None)

def apply_auto_arima(internal_series: dict) -> None:
    
    # Given an intermediate_object, for each course offering marked for
    # the statistical approach, applies auto-arima to determine a capacity,
    # or marks the class as unpredicted in the case that the method returns
    # no value or a value with an unacceptably large error margin. In the
    # case that this method fails to produce an output for a course, mark
    # that course as heuristic.

    # :param internal_series: Data series collated per course offering
    # :return: None, internal_series is modified in place
    
    time_index = [i for i in range(1, 15)]
    
    test_dict = {"CSC110-F": {"data": [0, 0, 500, 200, 400, 300, 150, 200, 220, 175, 124, 221, 175, 200], "approach": 1, "capacity": 500}}
    
    for key in test_dict:
        course_sem = key
        if test_dict[key]["approach"] == 1:
            past_data = test_dict[key]["data"]
            data_dict = {'time': time_index, 'hist_capacities': past_data}
            df = pd.DataFrame.from_dict(data_dict)
            df = df.set_index('time')
            capacity = predict_capacity(df)
            test_dict[key]["capacity"] = capacity
    
def predict_capacity(time_series):
    model = auto_arima(time_series, start_p = 1, start_1 = 2,
                       test = 'adf',
                       max_p = 5, max_a = 5,
                       m = 1,
                       d = 1,
                       seasonal = False,
                       start_P = 0,
                       D = None,
                       trace = True,
                       error_action = 'ignore',
                       suppress_warnings= True,
                       stepwise = True)
    
    print(model.summary())
    
    capacity = model.predict(1)
    return capacity[0]
        
if __name__ == '__main__':
    main()
        
