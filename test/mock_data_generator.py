import json
from enum import Enum
import jsonpickle


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


def generate_deterministic_mock_schedule(num_courses: int):

    return "{}"


def generate_randomized_mock_schedule(num_courses: int):

    return "{}"


def extract_course_year(historic_data: dict, year: int):
    fall_courses   = []
    spring_courses = []
    summer_courses = []
    for course in historic_data:
        if '09' in course['term'] and str(year) in course['term']:
            fall_courses.append(course)
        if '01' in course['term'] and str(year+1) in course['term']:
            spring_courses.append(course)
        if '05' in course['term'] and str(year+1) in course['term']:
            summer_courses.append(course)
    return fall_courses, spring_courses, summer_courses


def populate_course_offering(courses: list):
    course_sections = []
    test_course     = ""

    for course in courses:
        time          = ("12:00", "13:20")
        day_times     = DayTimes(time, time, time, time, time)

        prof_id            = "1"
        prof_name          = course["faculty"][0]["displayName"]
        prof_is_peng       = False
        prof_faculty_type  = FacultyTypeEnum.TEACHING.name
        prof_course_pref   = [CoursePreference("CSC225", 195)]
        prof_obligations   = 5
        prof_pref_times    = {"fall": day_times, "spring": day_times, "summer": day_times}
        prof_pref_num      = {"fall": 1, "spring": 2, "summer": 3}
        prof_pref_no_teach = SemesterEnum.FALL.name
        prof_day_spread    = [CourseDaySpreadEnum.TWF.name, CourseDaySpreadEnum.MTh.name]
        professor          = Professor(prof_id, prof_name, prof_is_peng, prof_faculty_type, prof_course_pref, prof_obligations,
                                   prof_pref_times, prof_pref_num, prof_pref_no_teach, prof_day_spread)

        course_code     = course["subjectCourse"]
        course_title    = course["courseTitle"]
        course_peng_req = {"fall": True, "spring": True, "Summer": False}
        course_year_req = course["courseNumber"][0]
        test_course          = Course(course_code, course_title, course_peng_req, course_year_req)

        course_section_time_slot  = []
        lecture_time = (course['meetingsFaculty'][0]['meetingTime']['beginTime'], course['meetingsFaculty'][0]['meetingTime']['endTime'])
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

        course_section_prof       = professor
        course_section_capacity   = course["maximumEnrollment"]
        test_course_section       = CourseSection(course_section_prof, course_section_capacity, course_section_time_slot)
        course_sections.append(test_course_section)

    course_offering = CourseOffering(test_course, course_sections)
    return course_offering


def populate_term(courses: list):
    course_offerings = []
    for course in courses:
        course_sections = []
        for course_section in courses:
            if course_section["subjectCourse"] == course["subjectCourse"]:
                course_sections.append(course_section)
        course_offerings.append(populate_course_offering(course_sections))
    return course_offerings


def historic_year_to_mock_schedule(year: int):
    with open("../data/real/historicSengProgramCourseData.json", "r") as f:
        json_obj = json.load(f)
    fall_courses, spring_courses, summer_courses = extract_course_year(json_obj, year)
    schedule_fall   = populate_term(fall_courses)
    schedule_spring = populate_term(spring_courses)
    schedule_summer = populate_term(summer_courses)

    schedule = Schedule(schedule_fall, schedule_spring, schedule_summer)
    return schedule


class FacultyTypeEnum(Enum):
    RESEARCH = 1
    TEACHING = 2


class SemesterEnum(Enum):
    FALL   = 1
    SPRING = 2
    SUMMER = 3


class DayOfTheWeekEnum(Enum):
    MONDAY    = 1
    TUESDAY   = 2
    WEDNESDAY = 3
    THURSDAY  = 4
    FRIDAY    = 5


class CourseDaySpreadEnum(Enum):
    TWF = 1
    MTh = 2
    M   = 3
    T   = 4
    W   = 5
    Th  = 6
    F   = 7


class CoursePreference:
    def __init__(self, courseCode: str, enthusiasmScore: int):
        self.courseCode        = courseCode
        self.enthusiasmScore   = enthusiasmScore


class DayTimes:
    def __init__(self, monday: tuple, tuesday: tuple, wednesday: tuple, thursday: tuple, friday: tuple):
        self.monday    = monday
        self.tuesday   = tuesday
        self.wednesday = wednesday
        self.thursday  = thursday
        self.friday    = friday


class Professor:
    def __init__(self, id: str, name: str, isPeng: bool, facultyType: str, coursePreferences: list,
                 teachingObligations: int, preferredTimes: dict, preferredCoursesPerSemester: dict,
                 preferredNonTeachingSemester : str, preferredCourseDaySpreads: []):
        self.id                           = id
        self.name                         = name
        self.isPeng                       = isPeng
        self.facultyType                  = facultyType
        self.coursePreferences            = coursePreferences
        self.teachingObligations          = teachingObligations
        self.preferredTimes               = preferredTimes
        self.preferredCoursesPerSemester  = preferredCoursesPerSemester
        self.preferredNonTeachingSemester = preferredNonTeachingSemester
        self.preferredCourseDaySpreads    = preferredCourseDaySpreads


class TimeSlot:
    def __init__(self, dayOfWeek: str, timeRange: tuple):
        self.dayOfWeek = dayOfWeek
        self.timeRange = timeRange


class Course:
    def __init__(self, code: str, title: str, pengRequired: dict, yearRequired: int):
        self.code         = code
        self.title        = title
        self.pengRequired = pengRequired
        self.yearRequired = yearRequired


class CourseSection:
    def __init__(self, professor: Professor, capacity: int, timeSlots: list):
        self.professor = professor
        self.capacity  = capacity
        self.timeSlots = timeSlots


class CourseOffering:
    def __init__(self, course: Course, sections: list):
        self.course   = course
        self.sections = sections


class Schedule:
    def __init__(self, fall: list, spring: list, summer: list,):
        self.fall   = fall
        self.spring = spring
        self.summer = summer


if __name__ == '__main__':
    historicTestSchedule = historic_year_to_mock_schedule(2021)
    pickledHistoric = jsonpickle.encode(historicTestSchedule, unpicklable=False)
    json_obj = json.loads(pickledHistoric)
    with open("../data/testHistoricSchedule.json", "w") as f:
        json.dump(json_obj, f)


    time          = ("12:00", "13:20")
    day_times     = DayTimes(time, time, time, time, time)

    prof_id            = "1"
    prof_name          = "Bill Bird"
    prof_is_peng       = False
    prof_faculty_type  = FacultyTypeEnum.TEACHING.name
    prof_course_pref   = [CoursePreference("CSC225", 195)]
    prof_obligations   = 5
    prof_pref_times    = {"fall": day_times, "spring": day_times, "summer": day_times}
    prof_pref_num      = {"fall": 1, "spring": 2, "summer": 3}
    prof_pref_no_teach = SemesterEnum.FALL.name
    prof_day_spread    = [CourseDaySpreadEnum.TWF.name, CourseDaySpreadEnum.MTh.name]
    test_professor = Professor(prof_id, prof_name, prof_is_peng, prof_faculty_type, prof_course_pref, prof_obligations,
                               prof_pref_times, prof_pref_num, prof_pref_no_teach, prof_day_spread)
    course_code     = "CSC225"
    course_title    = "Algorithms and Data Structure 1"
    course_peng_req = {"fall": True, "spring": True, "Summer": False}
    course_year_req = 2
    test_course          = Course(course_code, course_title, course_peng_req, course_year_req)

    course_section_time_slotM = TimeSlot(DayOfTheWeekEnum.MONDAY.name, time )
    course_section_time_slotT = TimeSlot(DayOfTheWeekEnum.THURSDAY.name, time )
    course_section_prof       = test_professor
    course_section_capacity   = 500
    course_section_time_slot  = [course_section_time_slotM, course_section_time_slotT ]
    test_course_section       = CourseSection(course_section_prof, course_section_capacity, course_section_time_slot)

    test_course_offering = CourseOffering(test_course, [test_course_section])

    test_schedule = Schedule([test_course_offering], [test_course_offering], [test_course_offering])
    result = jsonpickle.encode(test_schedule, unpicklable=False)

    json_obj = json.loads(result)

    with open("../data/testSchedule.json", "w") as f:
        json.dump(json_obj, f)

    with open("../data/real/historicSengProgramCourseData.json", "r") as f:
        object_json = json.load(f)

    print(object_json[0])
