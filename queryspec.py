from enum import Enum, auto

'''This is the canonical source of intents and query patterns'''

class Intent(Enum):
    #When the intent can't be understood
    UNKNOWN                         = auto()

    PREREQS_OF_COURSE               = auto()
    UNITS_OF_COURSE                 = auto()
    LEVEL_OF_COURSE                 = auto()
    TITLE_OF_COURSE                 = auto()
    TEACHERS_OF_COURSE              = auto()
    SECTIONS_OF_COURSE              = auto()
    ENROLLMENT_CAP_OF_COURSE        = auto()
    COURSE_ID_OF_COURSE             = auto()
    DESCRIPTION_OF_COURSE           = auto()

    TIMES_COURSE_OFFERED            = auto()
    TERMS_COURSE_OFFERED            = auto()
    DOES_COURSE_INVOLVE_CODING      = auto()
    IS_COURSE_ELECTIVE              = auto()

    FIND_COURSE_ABOUT_TOPIC         = auto() 
