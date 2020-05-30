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
    ELECTIVES_OFFERED_CURRENT           = auto()
    ELECTIVES_OFFERED_NEXT              = auto()

    DESCRIPTION_OF_COURSE               = auto()
    FIND_COURSE_ABOUT_TOPIC             = auto()

    TIMES_COURSE_OFFERED_CURRENT        = auto()

    TIMES_COURSE_OFFERED_NEXT           = auto()

    UNITS_OF_COURSE                     = auto()
    HOURS_OF_COURSE                     = auto()

    PREREQS_OF_COURSE                   = auto()

    TITLE_OF_COURSE                     = auto()
    COURSE_ID_OF_COURSE                 = auto()
    LEVEL_OF_COURSE                     = auto()

    ENROLLMENT_CAP_OF_COURSE_CURRENT    = auto()

    ENROLLMENT_CAP_OF_COURSE_NEXT       = auto()

class MissingFieldException(Exception):
    pass

class QueryParameters():

    def __init__(self, class_id: int = None, term: str = None, professor: str = None, topic: str = None):
        """Stores the parameters found in a users queries. All values should be normalized BEFORE being inserted."""
        self.class_id = class_id
        self.term = term
        self.professor = professor
        self.topic = topic

    def __repr__(self):
        return f"{self.__class__.__name__}(class_id={self.class_id}, term='{self.term}', professor='{self.professor}', topic='{self.topic}'')"

    def require_class_id(self):
        if self.class_id is None:
            raise MissingFieldException("Course id")

    def require_term(self):
        if self.term is None:
            raise MissingFieldException("Term")

    def require_professor(self):
        if self.professor is None:
            raise MissingFieldException("Professor")

    def require_topic(self):
        if self.topic is None:
            raise MissingFieldException("Topic")
