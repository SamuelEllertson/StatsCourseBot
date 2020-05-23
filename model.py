from queryspec import Intent

'''This is for parsing the intent from a message, as well as extracting the relevant information
from a message based on the intent'''

class Model():

    def __init__(self, args, datastore, iohandler):
        self.args = args
        self.datastore = datastore
        self.iohandler = iohandler

    def get_intent(self, message: str) -> Intent:
        '''Takes in a raw message, and determines its intent, returning Intent.UNKNOWN
        if it can not determine within some tolerance. It is permitted, and encouraged, to ask 
        additional questions to determine a users intent'''
        return Intent.UNKNOWN

    def get_course_id(self, message: str) -> int:
        '''This method is very important, being called on all but one intents. 
        It takes in a raw message, and determines which single course it is refering to.
        It could be in the form of some or parts of its title, or its course id.
        It should aggressively try its options to come up with its best guess, or None if it has no idea'''
        return 312