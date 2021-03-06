import json
from enum import Enum
import jsonpickle

add_cap_first_year = [
    "math109",
    "math100",
    "math110",
    "engr130",
    "engr110",
    "phys110",
    "csc111",
    "math101",
    "engr120",
    "engr141",
    "phys111",
    "csc115",
    "engr001",
    "chem101",
    "math122",
    "stat260",
    "econ180"
]

def populate_term(courses: list, term: list, min_sections: int, max_sections: int):
    section_count = min_sections
    section_template = {'professor': '',
                        'capacity': '0'}

    for course in courses:
        course_obj = {'code': course,
                      'title': 'This course is awesome'}
        section_obj = [section_template for i in range(section_count)]

        offering_obj = {'course': course_obj,
                        'sections': section_obj}

        term.append(offering_obj)
        section_count = section_count + 1
        if section_count > max_sections:
            section_count = min_sections
    return


def mock_data_generator(fall_courses: list, spring_courses: list, summer_courses: list, min_number_sections: int = 1,
                        max_number_sections: int = 1) -> dict:
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
    fall = []
    spring = []
    summer = []

    populate_term(fall_courses, fall, min_number_sections, max_number_sections)
    populate_term(spring_courses, spring, min_number_sections, max_number_sections)
    populate_term(summer_courses, summer, min_number_sections, max_number_sections)

    mock_schedule = {'fall': fall, 'spring': spring, 'summer': summer}

    json_obj = json.dumps(mock_schedule)
    mock_schedule = json.loads(json_obj)

    return mock_schedule


def generate_historial_offering(course: str, course_term_code: str, enrollment: int) -> dict:
    """ This function takes in a course, course-term code, and enrollment
    value and returns a single historical offering dictionary"""
    return {'term': course_term_code, 'maximumEnrollment': enrollment, 'subjectCourse': course}


def generate_course_enrollment(fall_courses: list, spring_courses: list, summer_courses: list,
                               historical_terms: list) -> dict:
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
                if ((course_list == fall_courses) and (historical_term.endswith('09'))):
                    course_enrollment \
                        .append(generate_historial_offering(course, historical_term, 1))
                elif ((course_list == spring_courses) and (historical_term.endswith('01'))):
                    course_enrollment \
                        .append(generate_historial_offering(course, historical_term, 1))
                elif ((course_list == summer_courses) and (historical_term.endswith('05'))):
                    course_enrollment \
                        .append(generate_historial_offering(course, historical_term, 1))
    return course_enrollment


class FacultyTypeEnum(Enum):
    RESEARCH = 1
    TEACHING = 2


class SemesterEnum(Enum):
    FALL = 1
    SPRING = 2
    SUMMER = 3


class DayOfTheWeekEnum(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5


class CourseDaySpreadEnum(Enum):
    TWF = 1
    MTh = 2
    M = 3
    T = 4
    W = 5
    Th = 6
    F = 7


class CoursePreference:
    def __init__(self, courseCode: str, enthusiasmScore: int):
        self.courseCode = courseCode
        self.enthusiasmScore = enthusiasmScore


class DayTimes:
    def __init__(self, monday: tuple, tuesday: tuple, wednesday: tuple, thursday: tuple, friday: tuple):
        self.monday = monday
        self.tuesday = tuesday
        self.wednesday = wednesday
        self.thursday = thursday
        self.friday = friday


class Professor:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name


class TimeSlot:
    def __init__(self, dayOfWeek: str, timeRange: tuple):
        self.dayOfWeek = dayOfWeek
        self.timeRange = timeRange


class Course:
    def __init__(self, code: str, title: str, pengRequired: dict, yearRequired: int):
        self.code = code
        self.title = title
        self.pengRequired = pengRequired
        self.yearRequired = yearRequired


class CourseSection:
    def __init__(self, professor: Professor, capacity: int, timeSlots: list):
        self.professor = professor
        self.capacity = capacity
        self.timeSlots = timeSlots


class CourseOffering:
    def __init__(self, course: Course, sections: list):
        self.course = course
        self.sections = sections


class Schedule:
    def __init__(self, fall: list, spring: list, summer: list, ):
        self.fall = fall
        self.spring = spring
        self.summer = summer


def generate_deterministic_mock_schedule(num_courses: int):
    return "{}"


def generate_randomized_mock_schedule(num_courses: int):
    return "{}"


CAPFLAG = True


def extract_course_year(historic_data: dict, year: int):
    fall_courses = []
    spring_courses = []
    summer_courses = []
    for course in historic_data:
        # print(f"Course term: {course['term']}")
        # print(f"Year: {year}")
        # print(f"{course['term'].startswith(str(year))}")
        if course['term'].endswith('09') and course['term'].startswith(str(year)):#str(year) in course['term']:
            flag = True
            for courseComapre in fall_courses:
                if courseComapre['subjectCourse'] == course['subjectCourse']:
                    courseComapre['maximumEnrollment'] = courseComapre['maximumEnrollment'] + course[
                        'maximumEnrollment']
                    flag = False
            if flag:
                fall_courses.append(course)

        if course['term'].endswith('01') and course['term'].startswith(str(year+1)):#str(year + 1) in course['term']:
            flag = True
            for courseComapre in spring_courses:
                if courseComapre['subjectCourse'] == course['subjectCourse']:
                    courseComapre['maximumEnrollment'] = courseComapre['maximumEnrollment'] + course[
                        'maximumEnrollment']
                    flag = False
            if flag:
                spring_courses.append(course)

        if course['term'].endswith('05') and course['term'].startswith(str(year+1)):#str(year + 1) in course['term']:
            flag = True
            for courseComapre in summer_courses:
                if courseComapre['subjectCourse'] == course['subjectCourse']:
                    courseComapre['maximumEnrollment'] = courseComapre['maximumEnrollment'] + course[
                        'maximumEnrollment']
                    flag = False
            if flag:
                summer_courses.append(course)

    return fall_courses, spring_courses, summer_courses


def populate_course_offering(courses: list):
    course_sections = []
    test_course = ""

    for course in courses:
        time = ("12:00", "13:20")
        day_times = DayTimes(time, time, time, time, time)

        prof_id = "1"
        prof_name = course["faculty"][0]["displayName"]
        professor = Professor(prof_id, prof_name)

        course_code = course["subjectCourse"]
        course_title = course["courseTitle"]
        course_peng_req = {"fall": True, "spring": True, "Summer": False}
        course_year_req = course["courseNumber"][0]
        test_course = Course(course_code, course_title, course_peng_req, course_year_req)

        course_section_time_slot = []
        lecture_time = (course['meetingsFaculty'][0]['meetingTime']['beginTime'],
                        course['meetingsFaculty'][0]['meetingTime']['endTime'])
        if course["meetingsFaculty"][0]['meetingTime']["monday"]:
            course_section_time_slot.append(TimeSlot(DayOfTheWeekEnum.MONDAY.name, lecture_time))
        if course["meetingsFaculty"][0]['meetingTime']["tuesday"]:
            course_section_time_slot.append(TimeSlot(DayOfTheWeekEnum.TUESDAY.name, lecture_time))
        if course["meetingsFaculty"][0]['meetingTime']["wednesday"]:
            course_section_time_slot.append(TimeSlot(DayOfTheWeekEnum.WEDNESDAY.name, lecture_time))
        if course["meetingsFaculty"][0]['meetingTime']["thursday"]:
            course_section_time_slot.append(TimeSlot(DayOfTheWeekEnum.THURSDAY.name, lecture_time))
        if course["meetingsFaculty"][0]['meetingTime']["friday"]:
            course_section_time_slot.append(TimeSlot(DayOfTheWeekEnum.FRIDAY.name, lecture_time))

        course_section_prof = professor
        course_section_capacity = 0

        if (CAPFLAG):
            course_section_capacity = course["maximumEnrollment"]
        else:
            if str(course["subjectCourse"]).lower() in add_cap_first_year:
                course_section_capacity = course["maximumEnrollment"] + 1

        test_course_section = CourseSection(course_section_prof, course_section_capacity, course_section_time_slot)
        course_sections.append(test_course_section)

    course_offering = CourseOffering(test_course, course_sections)
    return course_offering


def populate_schedule_term(courses: list):
    course_offerings = []
    for course in courses:
        course_sections = []
        for course_section in courses:
            if course_section["subjectCourse"] == course["subjectCourse"]:
                course_sections.append(course_section)
        course_offerings.append(populate_course_offering(course_sections))
    return course_offerings


def historic_year_to_mock_schedule(year: int, includeCapFlag: bool = True):
    global CAPFLAG
    CAPFLAG = includeCapFlag
    with open("../data/real/historicSengProgramCourseData.json", "r") as f:
        json_obj = json.load(f)
    fall_courses, spring_courses, summer_courses = extract_course_year(json_obj, year)
    schedule_fall = populate_schedule_term(fall_courses)
    schedule_spring = populate_schedule_term(spring_courses)
    schedule_summer = populate_schedule_term(summer_courses)

    schedule = Schedule(schedule_fall, schedule_spring, schedule_summer)
    result = jsonpickle.encode(schedule, unpicklable=False)

    json_obj = json.loads(result)

    return json_obj


def create_mock_schedule():
    time = ("12:00", "13:20")
    day_times = DayTimes(time, time, time, time, time)

    prof_id = "1"
    prof_name = "Bill Bird"
    test_professor = Professor(prof_id, prof_name)
    course_code = "CSC225"
    course_title = "Algorithms and Data Structure 1"
    course_peng_req = {"fall": True, "spring": True, "Summer": False}
    course_year_req = 2
    test_course = Course(course_code, course_title, course_peng_req, course_year_req)

    course_section_time_slotM = TimeSlot(DayOfTheWeekEnum.MONDAY.name, time)
    course_section_time_slotT = TimeSlot(DayOfTheWeekEnum.THURSDAY.name, time)
    course_section_prof = test_professor
    course_section_capacity = 500
    course_section_time_slot = [course_section_time_slotM, course_section_time_slotT]
    test_course_section = CourseSection(course_section_prof, course_section_capacity, course_section_time_slot)

    test_course_offering = CourseOffering(test_course, [test_course_section])

    test_schedule = Schedule([test_course_offering], [test_course_offering], [test_course_offering])
    result = jsonpickle.encode(test_schedule, unpicklable=False)

    json_obj = json.loads(result)

    with open("../data/testSchedule.json", "w") as f:
        json.dump(json_obj, f)

    with open("../data/real/historicSengProgramCourseData.json", "r") as f:
        object_json = json.load(f)

    print(object_json[0])


if __name__ == '__main__':
    test_schedule= historic_year_to_mock_schedule(2021, False)
    result = jsonpickle.encode(test_schedule, unpicklable=False)

    json_obj = json.loads(result)

    with open("../data/testSchedule.json", "w") as f:
        json.dump(json_obj, f)
