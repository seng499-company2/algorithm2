# determination.py
# Author:
# Date: June 17th, 2022
# This module determines the approach to use

# Private Module Variables, Classes
# Private Module Helper Functions
# API Functions

def determine_approach(internal_series: dict) -> None:
    """ For each course offering in the internal data series, determine
    whether to apply statical or heuristic methods for capacity assignment:
    by filling in the approach field for each offering in internal series.

    :param internal_series: Data series collated by course offering
    :return: None, internal_series is modified in place
    """

    internal_series["CSC110-F"]["approach"] = 1
