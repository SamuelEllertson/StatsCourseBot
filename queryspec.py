from enum import Enum, auto

'''This is the canonical source of intents and query patterns'''

class Intent(Enum):
    #When the intent can't be understood
    UNKNOWN                             = auto()

    COURSE_OFFERED_IN_TERM              = auto()
    TERMS_COURSE_OFFERED                = auto()
    NUMBER_OF_TERMS_COURSE_OFFERED      = auto()

    DOES_COURSE_INVOLVE_CODING          = auto()
    WHAT_COURSES_INVOLVE_CODING         = auto()

    TEACHERS_OF_COURSE_CURRENT          = auto()
    PROFESSOR_COURSES_CURRENT           = auto()

    TEACHERS_OF_COURSE_NEXT             = auto()
    PROFESSOR_COURSES_NEXT              = auto()

    IS_COURSE_ELECTIVE                  = auto()
    TYPE_OF_COURSE                      = auto()
    APPROVED_ELECTIVES                  = auto()
    ELECTIVES_OFFERED_CURRENT           = auto()
    ELECTIVES_OFFERED_NEXT              = auto()

    DESCRIPTION_OF_COURSE               = auto()
    FIND_COURSE_ABOUT_TOPIC             = auto()

    TIMES_COURSE_OFFERED_CURRENT        = auto()

    TIMES_COURSE_OFFERED_NEXT           = auto()

    UNITS_OF_COURSE                     = auto()
    HOURS_FOR_COURSE                    = auto()

    PREREQS_OF_COURSE                   = auto()
    DOES_COURSE_HAVE_PREREQS            = auto()

    TITLE_OF_COURSE                     = auto()
    COURSE_ID_OF_COURSE                 = auto()
    LEVEL_OF_COURSE                     = auto()

    ENROLLMENT_CAP_OF_COURSE_CURRENT    = auto()

    ENROLLMENT_CAP_OF_COURSE_NEXT       = auto()
