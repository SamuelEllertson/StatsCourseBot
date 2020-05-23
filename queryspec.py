from enum import Enum, auto

'''This is the canonical source of intents and query patterns'''

class Intent(Enum):
    #When the intent can't be understood
    UNKNOWN                         = auto()

    PREREQS_OF_COURSE               = auto()
    UNITS_OF_COURSE                 = auto()
    LEVEL_OF_COURSE                 = auto()
    TITLE_OF_COURSE                 = auto()
    TIMES_COURSE_OFFERED            = auto()
    TERMS_COURSE_OFFERED            = auto()
    WHAT_COURSE_ABOUT               = auto()
    DOES_COURSE_INVOLVE_CODING      = auto()
    IS_COURSE_ELECTIVE              = auto()
    
    COURSE_ID_OF_TITLE              = auto()

    IS_COURSE_OFFERED_IN_TERM       = auto()
    IS_COURSE_OFFERED_NEXT_TERM     = auto()

    IS_COURSE_PREREQ_OF_COURSE      = auto()
    COURSES_AFTER_COURSE            = auto()

    FIND_COURSE_ABOUT_TOPIC         = auto()

    TEACHERS_THIS_QUARTER           = auto()
    TEACHERS_NEXT_QUARTER           = auto()
    
    NUMBER_OF_SECTIONS_THIS_QUARTER = auto()
    NUMBER_OF_SECTIONS_NEXT_QUARTER = auto()
    
    ENROLLMENT_CAP_NEXT_QUARTER     = auto()
    
class QueryPattern(Enum):
    ONE_COURSE      = auto()
    TWO_COURSES     = auto()
    TOPIC           = auto()
    COURSE_AND_TERM = auto()
    TITLE           = auto()

def intent_to_query_pattern(intent):
    #Unknown intent should be handled before this is ever called
    assert intent != Intent.UNKNOWN

    mapping = {
        Intent.PREREQS_OF_COURSE               : QueryPattern.ONE_COURSE,
        Intent.UNITS_OF_COURSE                 : QueryPattern.ONE_COURSE,
        Intent.LEVEL_OF_COURSE                 : QueryPattern.ONE_COURSE,
        Intent.TITLE_OF_COURSE                 : QueryPattern.ONE_COURSE,
        Intent.TIMES_COURSE_OFFERED            : QueryPattern.ONE_COURSE,
        Intent.TERMS_COURSE_OFFERED            : QueryPattern.ONE_COURSE,
        Intent.WHAT_COURSE_ABOUT               : QueryPattern.ONE_COURSE,
        Intent.DOES_COURSE_INVOLVE_CODING      : QueryPattern.ONE_COURSE,
        Intent.IS_COURSE_ELECTIVE              : QueryPattern.ONE_COURSE,
        Intent.COURSES_AFTER_COURSE            : QueryPattern.ONE_COURSE,
        Intent.TEACHERS_THIS_QUARTER           : QueryPattern.ONE_COURSE,
        Intent.TEACHERS_NEXT_QUARTER           : QueryPattern.ONE_COURSE,
        Intent.NUMBER_OF_SECTIONS_THIS_QUARTER : QueryPattern.ONE_COURSE,
        Intent.NUMBER_OF_SECTIONS_NEXT_QUARTER : QueryPattern.ONE_COURSE,
        Intent.ENROLLMENT_CAP_NEXT_QUARTER     : QueryPattern.ONE_COURSE
        Intent.IS_COURSE_OFFERED_NEXT_TERM     : QueryPattern.ONE_COURSE,

        Intent.IS_COURSE_PREREQ_OF_COURSE      : QueryPattern.TWO_COURSES,

        Intent.FIND_COURSE_ABOUT_TOPIC         : QueryPattern.TOPIC,

        Intent.IS_COURSE_OFFERED_IN_TERM       : QueryPattern.COURSE_AND_TERM,

        Intent.COURSE_ID_OF_TITLE              : QueryPattern.TITLE,
    }

    return mapping[intent]