# statistical.py
# Author:
# Date: June 17th, 2022
# This module applies the auto-ARIMA method to predict course capacities

# Helper Functions
# Module API
def apply_auto_arima(internal_series: dict) -> None:
    """ Given an intermediate_object, for each course offering marked for
    the statistical approach, applies auto-arima to determine a capacity,
    or marks the class as unpredicted in the case that the method returns
    no value or a value with an unacceptably large error margin. In the
    case that this method fails to produce an output for a course, mark
    that course as heuristic.

    :param internal_series: Data series collated per course offering
    :return: None, internal_series is modified in place
    """

    pass
