import json


def populate_term(courses: list, term: list, min_sections: int, max_sections: int):
    section_count    = min_sections
    section_template = {'professor': '',
                        'capacity': '0'}

    for course in courses:
        course_obj = {'code': course,
                      'title': 'This course is awesome'}
        section_obj  = [section_template for i in range(section_count)]

        offering_obj = {'course'  : course_obj,
                        'sections': section_obj}

        term.append(offering_obj)
        section_count = section_count + 1
        if section_count > max_sections:
            section_count = min_sections
    return


def mock_data_generator(fall_courses: list, spring_courses: list, summer_courses: list, min_number_sections: int = 1, max_number_sections: int = 1) -> dict:
    """
    This function create a mock schedule object that can be used for testing different
    scenarios of input data
    :param fall_courses:   Courses to add to fall term
    :param spring_courses: Courses to add to spring term
    :param summer_courses: Courses to add to summer term
    :param min_number_sections: Min number of sections a course will have
    :param max_number_sections: Max number of sections a course will have
    :return: a schedule object containing the mocked data
    """
    fall   = []
    spring = []
    summer = []

    populate_term(fall_courses,   fall,   min_number_sections, max_number_sections)
    populate_term(spring_courses, spring, min_number_sections, max_number_sections)
    populate_term(summer_courses, summer, min_number_sections, max_number_sections)

    mock_schedule = {'fall': fall, 'spring': spring, 'summer': summer}

    json_obj = json.dumps(mock_schedule)
    mock_schedule = json.loads(json_obj)

    return mock_schedule


def generate_historial_offering(course: str, course_term_code: str, enrollment: int) -> dict:
    """ This function takes in a course, course-term code, and enrollment
    value and returns a single historical offering dictionary"""
    return {'term': course_term_code, 'enrollment': enrollment, 'subjectCourse': course}


def generate_course_enrollment(fall_courses: list, spring_courses: list, summer_courses: list, historical_terms: list) -> dict:
    """ 
    This function creates a moch course enrollment data set that can be used for testing
    :param fall_courses:   Courses to add to fall term
    :param spring_courses: Courses to add to spring term
    :param summer_courses: Courses to add to summer term 
    :param historical_terms: List of course-term codes
    :return: a course enrollment object containing the moch data
    """
    course_enrollment = []
    for course_list in (fall_courses, spring_courses, summer_courses):
        for course in course_list:
            for historical_term in historical_terms:
                if((course_list == fall_courses) and (historical_term.endswith('09'))):
                    course_enrollment\
                    .append(generate_historial_offering(course, historical_term, 1))
                elif((course_list == spring_courses) and (historical_term.endswith('01'))):
                    course_enrollment\
                    .append(generate_historial_offering(course, historical_term, 1))
                elif((course_list == summer_courses) and (historical_term.endswith('05'))):
                    course_enrollment\
                    .append(generate_historial_offering(course, historical_term, 1))
    return course_enrollment