
"""This class is responsible for dealing with the content of a users message and generating responses."""

from model import Model
from queryspec import Intent, QueryParameters

'''Takes in a message from the user, and uses its model to create a response message'''

class Responder():

    def __init__(self, args, datastore, iohandler):
        self.args = args
        self.datastore = datastore
        self.iohandler = iohandler
        self.model = Model(args, datastore, iohandler)
        self.model.train_model()

        self.intent_to_handler = {
            Intent.UNKNOWN           : self.handler_unknown,

            Intent.PREREQS_OF_COURSE : self.handler_prereqs_of_course,
            Intent.UNITS_OF_COURSE   : self.handler_units_of_course
            #etc
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

        course = self.datastore.get_course_from_id(params.class_id) #Retrieve the course object

        #Special case response since prereqs could be None
        if course.prereqs is None:
            return f"{course.full_name()} has no prerequisite courses."

        #prefer to use course.full_name() as opposed to course.title
        return f"The prerequisites for {course.full_name()} are: {course.prereqs}"

    def handler_units_of_course(self, params: QueryParameters) -> str:
        return "units are ___" #placeholder



    #Make one for each intent, same function definition for each

    def missing_information_response(self, intent: Intent, params: QueryParameters, missing_value: str):
        '''special handler for when an intent was determined, but the required parameters were missing'''

        return f"intent: {intent.name}, missing value: {missing_value}" #TODO: make this better


    #Extraneous methods

    def is_signaling_exit(self, message):
        '''returns true if message intends to end the program'''
        message = message.strip().lower()

        if message in ('quit', 'bye', 'exit', 'q'):
            return True

        return False

    def get_exit_phrase(self):
        return "Bye"
