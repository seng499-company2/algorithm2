# statistical.py
# Author: Siddhant Kumar
# Date: June 17th, 2022
# This module applies the auto-ARIMA method to predict course capacities

from pmdarima.arima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
import logging
import numpy as np


# Helper Functions
def predict_capacity(time_series):
    model = auto_arima(time_series, start_p=1, start_q=1,
                       max_p=10, max_q=10,
                       test='adf',
                       m=1,
                       d=None,
                       seasonal=False,
                       start_P=0,
                       D=None,
                       trace=True,
                       error_action='warn',
                       suppress_warnings=True,
                       stepwise=True)

    capacity = model.predict(1)
    return int(capacity[0])


# Module API

def apply_auto_arima(internal_series: dict) -> dict:
    # Given an intermediate_object, for each course offering marked for
    # the statistical approach, applies auto-arima to determine a capacity,
    # or marks the class as unpredicted in the case that the method returns
    # no value or a value with an unacceptably large error margin. In the
    # case that this method fails to produce an output for a course, mark
    # that course as heuristic.

    # :param internal_series: Data series collated per course offering
    # :return: None, internal_series is modified in place

    for key in internal_series:
        course_sem = key
        if internal_series[key]["approach"] == 1 and internal_series[key]["capacity"] <= 0:
            logging.debug('%s Trying Auto-Arima' % (str(key)).ljust(15, ' '))
            try:
                past_data = internal_series[key]["data"]
                past_data = [num for num in past_data if num > 0]
                time_index = [i for i in range(1, len(past_data) + 1)]
                data_dict = {'time': time_index, 'hist_capacities': past_data}
                df = pd.DataFrame.from_dict(data_dict)
                df = df.set_index('time')
                capacity = predict_capacity(df)
                internal_series[key]["capacity"] = capacity
                logging.debug('%s Success Auto-Arima forecasted %d' % (str(key).ljust(15, ' '), capacity))
            except:
                internal_series[key]["capacity"] = 0
                internal_series[key]["approach"] = 0
                logging.debug('%s Failure Auto-Arima' % (str(key).ljust(15, ' ')))
    return internal_series
