from enum import Enum, auto

'''This is the canonical source of intents and query patterns'''

class Intent(Enum):
    #When the intent can't be understood
    UNKNOWN                                = auto()

    Intent.PREREQS_OF_COURSE               = auto()
    Intent.UNITS_OF_COURSE                 = auto()
    Intent.LEVEL_OF_COURSE                 = auto()
    Intent.TITLE_OF_COURSE                 = auto()
    Intent.TEACHERS_OF_COURSE              = auto()
    Intent.SECTIONS_OF_COURSE              = auto()
    Intent.ENROLLMENT_CAP_OF_COURSE        = auto()
    Intent.COURSE_ID_OF_COURSE             = auto()
    Intent.DESCRIPTION_OF_COURSE           = auto()

    Intent.TIMES_COURSE_OFFERED            = auto()
    Intent.TERMS_COURSE_OFFERED            = auto()
    Intent.DOES_COURSE_INVOLVE_CODING      = auto()
    Intent.IS_COURSE_ELECTIVE              = auto()

    Intent.FIND_COURSE_ABOUT_TOPIC         = auto() 

    
    
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
        Intent.TEACHERS_OF_COURSE              : QueryPattern.ONE_COURSE,
        Intent.SECTIONS_OF_COURSE              : QueryPattern.ONE_COURSE,
        Intent.ENROLLMENT_CAP_OF_COURSE        : QueryPattern.ONE_COURSE,
        Intent.COURSE_ID_OF_COURSE             : QueryPattern.ONE_COURSE,
        Intent.DESCRIPTION_OF_COURSE           : QueryPattern.ONE_COURSE,

        Intent.TIMES_COURSE_OFFERED            : QueryPattern.ONE_COURSE,
        Intent.TERMS_COURSE_OFFERED            : QueryPattern.ONE_COURSE,
        Intent.DOES_COURSE_INVOLVE_CODING      : QueryPattern.ONE_COURSE,
        Intent.IS_COURSE_ELECTIVE              : QueryPattern.ONE_COURSE,

        Intent.FIND_COURSE_ABOUT_TOPIC         : QueryPattern.TOPIC, 
    }

    return mapping[intent]