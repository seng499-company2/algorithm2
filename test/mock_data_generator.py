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