
"""This class is responsible for dealing with the content of a users message and generating responses."""

from model import Model
from queryspec import Intent, QueryParameters
from datastore import Course, Section
from typing import List, Set

'''Takes in a message from the user, and uses its model to create a response message'''

class Responder():

    def __init__(self, args, datastore, iohandler):
        self.args = args
        self.datastore = datastore
        self.iohandler = iohandler
        self.model = Model(args, datastore, iohandler)
        self.model.train_model()

        self.intent_to_handler = {
            Intent.UNKNOWN                          :   self.handler_unknown,

            Intent.PREREQS_OF_COURSE                :   self.handler_prereqs_of_course,
            Intent.UNITS_OF_COURSE                  :   self.handler_units_of_course,
            Intent.COURSE_OFFERED_IN_TERM           :   self.handler_course_offered_in_term,
            Intent.TERMS_COURSE_OFFERED             :   self.handler_terms_course_offered,
            Intent.NUMBER_OF_TERMS_COURSE_OFFERED   :   self.handler_number_of_terms_course_offered,
            Intent.DOES_COURSE_INVOLVE_CODING       :   self.handler_does_course_involve_coding,
            Intent.WHAT_COURSES_INVOLVE_CODING      :   self.handler_what_courses_involve_coding,
            Intent.TEACHERS_OF_COURSE_CURRENT       :   self.handler_teachers_of_course_current,
            Intent.PROFESSOR_COURSES_CURRENT        :   self.handler_professor_courses_current,
            Intent.TEACHERS_OF_COURSE_NEXT          :   self.handler_teachers_of_course_next,
            Intent.PROFESSOR_COURSES_NEXT           :   self.handler_professor_courses_next,
            Intent.IS_COURSE_ELECTIVE               :   self.handler_is_course_elective,
            Intent.ELECTIVES_OFFERED_CURRENT        :   self.handler_electives_offered_current,
            Intent.ELECTIVES_OFFERED_NEXT           :   self.handler_electives_offered_next,
            Intent.DESCRIPTION_OF_COURSE            :   self.handler_description_of_course,
            Intent.FIND_COURSE_ABOUT_TOPIC          :   self.handler_find_course_about_topic,
            Intent.TIMES_COURSE_OFFERED_CURRENT     :   self.handler_times_course_offered_current,
            Intent.TIMES_COURSE_OFFERED_NEXT        :   self.handler_times_course_offered_next,
            Intent.HOURS_OF_COURSE                  :   self.handler_hourse_of_course,
            Intent.TITLE_OF_COURSE                  :   self.handler_title_of_course,
            Intent.COURSE_ID_OF_COURSE              :   self.handler_course_id_of_course,
            Intent.LEVEL_OF_COURSE                  :   self.handler_level_of_course,
            Intent.ENROLLMENT_CAP_OF_COURSE_CURRENT :   self.enrollment_cap_of_course_current,
            Intent.ENROLLMENT_CAP_OF_COURSE_NEXT    :   self.enrollment_cap_of_course_next,
           
        }

    def get_response(self, message: str) -> str:
        '''The primary function of the Responder. Takes in a raw message from the user
        and returns a final response message'''

        intent, params = self.model.get_intent_and_params(message)

        try:
            return self.intent_to_handler[intent](params)
        except AttributeError as e:
            return self.missing_information_response(intent, params, str(e))

    # Query handlers 

    def handler_unknown(self, params: QueryParameters) -> str:
        '''This one is special, it should use any params available to craft the best reponse it can'''
        return "unknown intent" #placeholder

    #Use this as a model for implementing the rest
    def handler_prereqs_of_course(self, params: QueryParameters) -> str:

        params.require_class_id() #require the presence of variable for a given intent, this corresponds to the [variable] in the query

        #Retrieve the course object via self.get_course() this handles the case of an invalid course automatically
        course = self.get_course(params.class_id)

        #Special case response since prereqs could be None
        if course.prereqs is None:
            return f"{course.full_name()} has no prerequisite courses."

        #prefer to use course.full_name() as opposed to course.title
        return f"The prerequisites for {course.full_name()} are: {course.prereqs}"

    def handler_units_of_course(self, params: QueryParameters) -> str:
    
        params.require_class_id()

        course = self.get_course(params.class_id)
    
        return f"{course.full_name()} counts for {course.units} units."

    def handler_course_offered_in_term(self, params: QueryParameters) -> str: #TODO: Imporve response message

        params.require_class_id()

        params.require_term()

        course = self.get_course(params.class_id)

        if params.term in course.terms:
            return "Yes."
        else:
            return "No."

    def handler_terms_course_offered(self, params: QueryParameters) -> str: #TODO: Clean up course.terms formatting

        params.require_class_id()

        course = self.get_course(params.class_id)

        return f"{course.full_name()} is typically offered {course.terms}."

    def handler_number_of_terms_course_offered(self, params: QueryParameters) -> str: #TODO: Check if quarters should be plural or not

        params.require_class_id()

        course = self.get_course(params.class_id)

        numberOfTerms = len(course.terms.split(","))

        return f"{course.full_name()} is usually offered in {numberOfTerms} quarters."

    def handler_does_course_involve_coding(self, params: QueryParameters) -> str: #TODO: Improve response message

        params.require_class_id()

        course = self.get_course(params.class_id)

        if course.coding_involved:
            return "Yes."
        else:
            return "No."

    def handler_what_courses_involve_coding(self, params: QueryParameters) -> str: #TODO: Add STAT in front of all classes in response message

        classes = self.datastore.get_classes_with_coding()

        return f"{classes} require coding."

    def handler_teachers_of_course_current(self, params: QueryParameters) -> str: #TODO: Add and after second to last professor in professor list

        params.require_class_id()

        sections = self.get_sections_from_id_and_quarter(params.class_id, True)

        professors = []

        for section in sections:
            professors.append(section.teacher)

        return f"{professors} are teaching {sections[0].full_name()} this quarter."

    def handler_professor_courses_current(self, params: QueryParameters) -> str: #TODO: Add STAT in front of all classes in response message

        params.require_professor()

        sections = self.get_sections_from_professor(params.professor, True)

        classes = []

        for section in sections:
            classes.append(section.course_id)

        return f"{params.professor} is teaching {classes} this quarter."

    def handler_teachers_of_course_next(self, params: QueryParameters) -> str: #TODO: Add and after second to last professor in professor list

        params.require_class_id()

        sections = self.get_sections_from_id_and_quarter(params.class_id, False)                                                                              
        professors = []

        for section in sections:
            professors.append(section.teacher)

        return f"{professors} are teaching {sections[0].full_name()} next quarter."

    def handler_professor_courses_next(self, params: QueryParameters) -> str: #TODO: Add STAT in front of all classes in response message

        params.require_professor()

        sections = self.get_sections_from_professor(params.professor, False)

        classes = []

        for section in sections:
            classes.append(section.course_id)

        return f"{params.professor} is teaching {classes} this quarter."

    def handler_is_course_elective(self, params: QueryParameters) -> str: #TODO: Improve response message

        params.require_class_id()

        course = self.get_course()

        if course.elective:
            return "Yes."
        else:
            return "No."

    def handler_electives_offered_current(self, params: QueryParameters) -> str: #TODO: Add STAT in front of all classes in response message
        
        results = self.get_electives_by_quarter(True)

        classes = []

        for result in results:
            classes.append(result)

        return f"{classes} are offered this quarter."

    def handler_electives_offered_next(self, params: QueryParameters) -> str: #TODO: Add STAT in front of all classes in response message

        results = self.get_electives_by_quarter(False)

        classes = []

        for result in results:
            classes.append(result)

        return f"{classes} are offered next quarter."

    def handler_description_of_course(self, params: QueryParameters) -> str: #TODO: Make sure response sounds natural

        params.require_class_id()

        course = self.get_course(params.class_id)

        return f"{course.full_name()} is about {course.description}."

    def handler_find_course_about_topic(self, params: QueryParameters) -> str: #TODO: Improve response message

        params.require_topic()

        courses = self.datastore.get_course_about_topic(params.topic)

        if len(courses) != 0:
            return "Yes."
        else:
            return "No."

    def handler_times_course_offered_current(self, params: QueryParameters) -> str: #TODO: Add STAT in front of course id

        params.require_class_id()

        sections = self.get_sections_from_id_and_quarter(params.class_id, True)
                                                                             
        times = []

        for section in sections:
            times.append(section.times_offered)

        return f"{params.id} is offered at {times} each week this quarter."

    def handler_times_course_offered_next(self, params: QueryParameters) -> str: #TODO: Add STAT in front of course id

        params.require_class_id()

        sections = self.get_sections_from_id_and_quarter(params.class_id, False)

        times = []                                                                                                                                           
        for section in sections:
            times.append(section.times_offered)                            
                                                                                  
        return f"{params.id} is offered at {times} each week this quarter."

    def handler_hours_of_course(self, params: QueryParameters) -> str:

        params.require_class_id()

        course = self.get_course(params.class_id)

        return f"{course.full_name()} meets for {course.units} hours a week."

    def handler_title_of_course(self, params: QueryParameters) -> str:

        params.require_class_id()

        course = self.get_course(params.class_id)

        return f"The title of {course.full_name()} is {course.title}."

    def handler_course_id_of_course(self, params: QueryParameters) -> str: #TODO: See if this question is really needed

        params.require_class_id()

        return f"The class number of STAT {params.class_id} is {params.class_id}."

    def handler_level_of_course(self, params: QueryParameters) -> str: #TODO: Verify works correctly

        params.require_class_id()

        return f"The level of STAT {params.class_id} is {str(params.class_id)[0]}00."

    def handler_enrollment_cap_of_course_current(self, params: QueryParameters) -> str: #TODO: Add STAT in front of class_id

        params.require_class_id()

        sections = self.get_sections_from_id_and_quarter(params.class_id, True)

        cap = 0
        for section in sections:
            cap += section.enrollment_cap

        return f"The enrollment cap for {params.class_id} this quarter is {cap}."

    def handler_enrollment_cap_of_course_next(self, params: QueryParameters) -> str: #TODO: Add STAT in front of class_id

        params.require_class_id()

        sections = self.get_sections_from_id_and_quarter(params.class_id, False)

        cap = 0
        for section in sections:
            cap += section.enrollment_cap                                                                                                                    
        return f"The enrollment cap for {params.class_id} next quarter is {cap}."


    def missing_information_response(self, intent: Intent, params: QueryParameters, missing_value: str):
        '''special handler for when an intent was determined, but the required parameters were missing'''

        return f"intent: {intent.name}, missing value: {missing_value}" #TODO: make this better


    #Extraneous methods

    def get_course(self, class_id: int) -> Course:
        '''This is the prefered method to get a course object. It handles the case of
        an invalid course id'''

        course = self.datastore.get_course_from_id(class_id)

        if course is None:
            raise InvalidCourseException(str(class_id))

        return course

    def get_sections_from_id_and_quarter(self, class_id: int, current_quarter: bool) -> List[Section]:

        sections = self.datastore.get_sections_from_id_and_quarter(class_id, current_quarter)

        if sections is None:
            raise InvalidSectionFromIdAndQuarterException(str(class_id), bool(current_quarter))

        return sections

    def get_sections_from_professor(self, professor: str, current_quarter: bool) -> List[Section]:

        sections = self.datastore.get_sections_from_professor(professor, current_quarter)

        if sections is None:
            raise InvalidSectionFromProfessorException(str(professor), bool(current_quarter))

        return sections

    def get_electives_by_quarter(self, current_quarter: bool) -> Set[str]:

        results = self.datastore.get_electives_by_quarter(current_quarter)

        if results is None:
            raise InvalidElectivesByQuarter(bool(current_quarter))

        return results

    def invalid_course_message(self, class_id):
        return f"I'm sorry, It appears that STAT {class_id} is not a valid class."

    def is_signaling_exit(self, message):
        '''returns true if message intends to end the program'''
        message = message.strip().lower()

        if message in ('quit', 'bye', 'exit', 'q'):
            return True

        return False

    def get_exit_phrase(self):
        return "Bye"
