
"""This class is responsible for dealing with the content of a users message and generating responses."""

from model import Model
from datastore import Course, Section
from typing import List, Set
from queryspec import Intent, QueryParameters, MissingFieldException

'''Takes in a message from the user, and uses its model to create a response message'''

class InvalidCourseException(Exception):
    pass

class Responder():

    def __init__(self, args, datastore, iohandler):
        self.args = args
        self.datastore = datastore
        self.iohandler = iohandler
        self.model = Model(args, datastore, iohandler)

        self.intent_to_handler = {
            Intent.UNKNOWN                          : self.handler_unknown,

            Intent.PREREQS_OF_COURSE                : self.handler_prereqs_of_course,
            Intent.UNITS_OF_COURSE                  : self.handler_units_of_course,
            Intent.COURSE_OFFERED_IN_TERM           : self.handler_course_offered_in_term,
            Intent.TERMS_COURSE_OFFERED             : self.handler_terms_course_offered,
            Intent.NUMBER_OF_TERMS_COURSE_OFFERED   : self.handler_number_of_terms_course_offered,
            Intent.DOES_COURSE_INVOLVE_CODING       : self.handler_does_course_involve_coding,
            Intent.WHAT_COURSES_INVOLVE_CODING      : self.handler_what_courses_involve_coding,
            Intent.TEACHERS_OF_COURSE_CURRENT       : self.handler_teachers_of_course_current,
            Intent.PROFESSOR_COURSES_CURRENT        : self.handler_professor_courses_current,
            Intent.TEACHERS_OF_COURSE_NEXT          : self.handler_teachers_of_course_next,
            Intent.PROFESSOR_COURSES_NEXT           : self.handler_professor_courses_next,
            Intent.IS_COURSE_ELECTIVE               : self.handler_is_course_elective,
            Intent.ELECTIVES_OFFERED_CURRENT        : self.handler_electives_offered_current,
            Intent.ELECTIVES_OFFERED_NEXT           : self.handler_electives_offered_next,
            Intent.DESCRIPTION_OF_COURSE            : self.handler_description_of_course,
            Intent.FIND_COURSE_ABOUT_TOPIC          : self.handler_find_course_about_topic,
            Intent.TIMES_COURSE_OFFERED_CURRENT     : self.handler_times_course_offered_current,
            Intent.TIMES_COURSE_OFFERED_NEXT        : self.handler_times_course_offered_next,
            Intent.HOURS_OF_COURSE                  : self.handler_hours_of_course,
            Intent.TITLE_OF_COURSE                  : self.handler_title_of_course,
            Intent.COURSE_ID_OF_COURSE              : self.handler_course_id_of_course,
            Intent.LEVEL_OF_COURSE                  : self.handler_level_of_course,
            Intent.ENROLLMENT_CAP_OF_COURSE_CURRENT : self.handler_enrollment_cap_of_course_current,
            Intent.ENROLLMENT_CAP_OF_COURSE_NEXT    : self.handler_enrollment_cap_of_course_next,
           
        }

    def get_response(self, message: str) -> str:
        '''The primary function of the Responder. Takes in a raw message from the user
        and returns a final response message'''

        intent, params = self.model.get_intent_and_params(message)

        if self.args.verbose:
            print(f"intent={intent.name}, params={params}")

        try:
            return self.intent_to_handler[intent](params)

        except MissingFieldException as e:
            return self.missing_information_response(intent, params, str(e))

        except InvalidCourseException as e:
            return self.invalid_course_message(str(e))

        except KeyboardInterrupt as e:
            raise e

        except Exception as e:
            if self.args.dev_mode:
                raise e
            else:
                return self.get_error_message()

    # Query handlers 

    def handler_unknown(self, params: QueryParameters) -> str:
        '''This one is special, it should use any params available to craft the best reponse it can'''
        return "unknown intent" #placeholder

    #Use this as a model for implementing the rest
    def handler_prereqs_of_course(self, params: QueryParameters) -> str:

        # Require the presence of variable for a given intent, this corresponds to the [variable] in the query
        params.require_class_id() 

        # Retrieve the course object via self.get_course() this handles the case of an invalid course automatically
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

    def handler_course_offered_in_term(self, params: QueryParameters) -> str:

        params.require_class_id()

        params.require_term()

        course = self.get_course(params.class_id)

        if params.term in course.terms:
            return f"Yes, STAT {params.class_id} is offered in the {params.term.title()}."
        else:
            return f"Sorry, STAT {params.class_id} is not offered in the {params.term.title()}."

    def handler_terms_course_offered(self, params: QueryParameters) -> str:

        params.require_class_id()

        course = self.get_course(params.class_id)

        if len(course.terms) == 0:
            return f"Sorry, {course.full_name()} is not a regularly offered class."
        if len(course.terms) == 1:
            return f"{course.full_name()} is typically offered in the {', '.join([t.title() for t in course.terms])}."
        else:
            return f"{course.full_name()} is typically offered in the following quarters: {', '.join([t.title() for t in course.terms])}."

    def handler_number_of_terms_course_offered(self, params: QueryParameters) -> str: 

        params.require_class_id()

        course = self.get_course(params.class_id)

        numberOfTerms = len(course.terms)

        if numberOfTerms == 1:
             return f"{course.full_name()} is usually offered in {numberOfTerms} quarter."
        else:
            return f"{course.full_name()} is usually offered in {numberOfTerms} quarters."

    def handler_does_course_involve_coding(self, params: QueryParameters) -> str:

        params.require_class_id()

        course = self.get_course(params.class_id)

        if course.coding_involved:
            return f"Yes, {course.full_name()} involves coding."
        else:
           return f"No, {course.full_name()} does not involve coding."

    def handler_what_courses_involve_coding(self, params: QueryParameters) -> str: 

        classes = self.datastore.get_classes_with_coding()

        classes = ["STAT " + str(c) for c in classes]

        if len(classes) > 1:
            classes[-1] = "and " + str(classes[-1])

        return f"{', '.join(classes)} require coding."

    def handler_teachers_of_course_current(self, params: QueryParameters) -> str:

        params.require_class_id()

        sections = self.datastore.get_sections_from_id_and_quarter(params.class_id, True)

        if len(sections) == 0:
            return f"Sorry, there are no sections of STAT {params.class_id} this quarter."

        professors = set()

        # Correct formatting and no duplicates
        for section in sections:
            name = section.teacher.split(", ")[0].title()
            professors.add(name)

        professors = list(professors)

        if len(professors) > 1:
            professors[-1] = "and " + professors[-1]

        # Can have 0, 1, or multiple professors teaching a class
        if len(professors) == 1:
            return f"Professor {', '.join(professors)} is teaching {sections[0].full_name()} this quarter."
        elif len(professors) == 0:
            return f"Sorry, no one is teaching STAT {params.class_id} this quarter."
        else:
            return f"Professors {', '.join(professors)} are teaching {sections[0].full_name()} this quarter."

    def handler_professor_courses_current(self, params: QueryParameters) -> str:

        params.require_professor()

        sections = self.datastore.get_sections_from_professor(params.professor, True)

        if len(sections) == 0:
            return f"Sorry, {params.professor} is not teaching any courses this quarter."

        classes = set()

        # Correct formatting and no duplicates
        for section in sections:
            name = section.full_name()
            classes.add(name)

        classes = list(classes)

        if len(classes) > 2:
            classes[-1] = "and " + str(classes[-1])

        if len(classes) == 0:
            return f"Sorry, Professor {params.professor.title()} is not teaching any classes this quarter."
        elif len(classes) == 2:
            return f"Professor {params.professor.title()} is teaching {classes[0] + ' and ' + classes[1]} this quarter."   
        else:
            return f"Professor {params.professor.title()} is teaching {', '.join(classes)} this quarter."            

    def handler_teachers_of_course_next(self, params: QueryParameters) -> str: 

        params.require_class_id()

        sections = self.datastore.get_sections_from_id_and_quarter(params.class_id, False)

        if len(sections) == 0:
            return f"Sorry, there are no sections of STAT {params.class_id} next quarter."              

        professors = set()

        # Correct formatting and no duplicates
        for section in sections:
            name = section.teacher.split(", ")[0].title()
            professors.add(name)

        professors = list(professors)

        if len(professors) > 1:
            professors[-1] = "and " + professors[-1]

        # Can have 0, 1, or multiple professors teaching a class
        if len(professors) == 1:
            return f"Professor {', '.join(professors)} is teaching {sections[0].full_name()} next quarter."
        elif len(professors) == 0:
            return f"Sorry, no one is teaching STAT {params.class_id} next quarter."
        else:
            return f"Professors {', '.join(professors)} are teaching {sections[0].full_name()} next quarter."

    def handler_professor_courses_next(self, params: QueryParameters) -> str: 
        params.require_professor()

        sections = self.datastore.get_sections_from_professor(params.professor, False)

        if len(sections) == 0:
            return f"Sorry, {params.professor} is not teaching any courses next quarter."

        classes = set()

        # Correct formatting and no duplicates
        for section in sections:
            name = section.full_name()
            classes.add(name)

        classes = list(classes)

        if len(classes) > 2:
            classes[-1] = "and " + str(classes[-1])

        if len(classes) == 0:
            return f"Sorry, Professor {params.professor.title()} is not teaching any classes next quarter."
        elif len(classes) == 2:
            return f"Professor {params.professor.title()} is teaching {classes[0] + ' and ' + classes[1]} next quarter." 
        else:
            return f"Professor {params.professor.title()} is teaching {', '.join(classes)} next quarter."            

    def handler_is_course_elective(self, params: QueryParameters) -> str:

        params.require_class_id()

        course = self.get_course(params.class_id)

        if course.elective:
            return f"Yes, {course.full_name()} is an elective."
        else:
             return f"No, {course.full_name()} is not an elective."

    def handler_electives_offered_current(self, params: QueryParameters) -> str:
        
        results = self.datastore.get_electives_by_quarter(True)

        classes = []

        for result in results:
            classes.append("STAT " + str(result))

        if len(classes) > 1:
            classes[-1] = "and " + str(classes[-1])

        if len(classes) == 0:
            return f"Sorry, there are no electives offered this quarter."
        else:
            return f"{', '.join(classes)} are all the electives this quarter."

    def handler_electives_offered_next(self, params: QueryParameters) -> str: 

        results = self.datastore.get_electives_by_quarter(False)

        classes = []

        for result in results:
            classes.append("STAT " + str(result))

        if len(classes) > 1:
            classes[-1] = "and " + str(classes[-1])

        if len(classes) == 0:
            return f"Sorry, there are no electives offered next quarter."
        else:
            return f"{', '.join(classes)} are all the electives offered next quarter."

    def handler_description_of_course(self, params: QueryParameters) -> str: #TODO: Make sure response sounds natural

        params.require_class_id()

        course = self.get_course(params.class_id)

        return f"{course.full_name()} is about {course.about}."

    def handler_find_course_about_topic(self, params: QueryParameters) -> str: #TODO: Improve response message

        params.require_topic()

        courses = self.datastore.get_courses_about_topic(params.topic)

        classes = [] 

        for course in courses:
            classes.append(course.full_name())

        if len(classes) > 2:
            classes[-1] = "and " + str(classes[-1])


        if len(classes) == 0:
            return f"Sorry, there aren't any courses about {params.topic}"
        elif len(classes) == 1:
            return f"{', '.join(classes)} is about {params.topic}."
        elif len(classes) == 2:
            return f"{classes[0] + ' and ' + classes[1]} are about {params.topic}."
        else:
            return f"{', '.join(classes)} are about {params.topic}."

    def handler_times_course_offered_current(self, params: QueryParameters) -> str: 

        params.require_class_id()

        sections = self.datastore.get_sections_from_id_and_quarter(params.class_id, True)

        if len(sections) == 0:
            return f"Sorry, there are no sections of STAT {params.class_id} this quarter."
                                                                             
        times = []

        for section in sections:
            if len(section.times_offered) > 0:
                times.append(section.times_offered)

        if len(times) > 2:
            times[-1] = "and " + str(times[-1])

        if len(times) == 0:
            return f"Sorry, {sections[0].full_name()} isn't offered synchronously this quarter. "
        elif len(times) == 2:
            return f"{sections[0].full_name()} is offered at {times[0] + ' and ' + times[1]} each week this quarter."
        else:
             return f"{sections[0].full_name()} is offered at {', '.join(times)} each week this quarter."

    def handler_times_course_offered_next(self, params: QueryParameters) -> str:

        params.require_class_id()
 
        sections = self.datastore.get_sections_from_id_and_quarter(params.class_id, False)

        if len(sections) == 0:
            return f"Sorry, there are no sections of STAT {params.class_id} next quarter."

        times = []

        for section in sections:
            if len(section.times_offered) > 0:
                times.append(section.times_offered)

        if len(times) > 2:
            times[-1] = "and " + str(times[-1])

        if len(times) == 0:
            return f"Sorry, {sections[0].full_name()} isn't offered synchronously next quarter. "
        elif len(times) == 2:
            return f"{sections[0].full_name()} is offered at {times[0] + ' and ' + times[1]} each week next quarter."
        else:
             return f"{sections[0].full_name()} is offered at {', '.join(times)} each week next quarter."

    def handler_hours_of_course(self, params: QueryParameters) -> str:

        params.require_class_id()

        course = self.get_course(params.class_id)

        return f"{course.full_name()} meets for {course.units} hours a week."

    def handler_title_of_course(self, params: QueryParameters) -> str:

        params.require_class_id()

        course = self.get_course(params.class_id)

        return f"The title of {course.full_name()} is {course.title}."

    def handler_course_id_of_course(self, params: QueryParameters) -> str:

        params.require_class_id()

        course = self.get_course(params.class_id)

        return f"The class number of {course.full_name()} is {course.id}."

    def handler_level_of_course(self, params: QueryParameters) -> str: #TODO: Verify works correctly

        params.require_class_id()

        course = self.get_course(params.class_id)

        return f"The level of {course.full_name()} is {str(course.id)[0]}00"

    def handler_enrollment_cap_of_course_current(self, params: QueryParameters) -> str: 

        params.require_class_id()

        sections = self.datastore.get_sections_from_id_and_quarter(params.class_id, True)

        cap = 0
        for section in sections:
            cap += section.enrollment_cap

        return f"The enrollment cap for {sections[0].full_name()} this quarter is {cap}."

    def handler_enrollment_cap_of_course_next(self, params: QueryParameters) -> str: 

        params.require_class_id()

        sections = self.datastore.get_sections_from_id_and_quarter(params.class_id, False)

        cap = 0
        for section in sections:
            cap += section.enrollment_cap                                                                                                                    
        return f"The enrollment cap for {sections[0].full_name()} next quarter is {cap}."


    def missing_information_response(self, intent: Intent, params: QueryParameters, missing_value: str):
        '''special handler for when an intent was determined, but the required parameters were missing'''
        return "Sorry, Looks like I'm confused, or your query is missing information. Try Rephrasing."


    #Extraneous methods

    def get_course(self, class_id: int) -> Course:
        '''This is the prefered method to get a course object. It handles the case of
        an invalid course id'''

        course = self.datastore.get_course_from_id(class_id)

        if course is None:
            raise InvalidCourseException(str(class_id))

        return course

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

    def get_error_message(self):
        return "Sorry, something went wrong."
