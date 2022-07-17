# IF THESE CONFIGS ARE CHANGED PLEASE REVIEW TESTS
MAX_TERMS_SINCE_LAST_OFFERING = 3       # The max number of years since the last offering to perform statistical forecasting
MIN_DATA_POINTS               = 5       # Then minimum number of data points needed to perform statistical forecasting
SCALING_FEATURE_FLAG          = False   # Feature flag for scaling
PROGRAM_GROWTH = 1.0855  # TODO: Calculate this dynamically based on program enrolment
MIN_COURSES = 1
MAX_COURSES = 6
CSC_FACTOR = 4  # To account for the fact that SEng. seats are 1/4 of total capacity
RATIO_ACADEMIC = float(11/15)
FOURTH_YEAR_CAPACITY = 50
THIRD_YEAR_CAPACITY = 60
SECOND_YEAR_CAPACITY = 80
FIRST_YEAR_CAPACITY = 100
UNKNOWN_YEAR_CAPACITY = 80