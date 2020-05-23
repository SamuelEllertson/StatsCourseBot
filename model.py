from queryspec import Intent

'''This is for parsing the intent from a message, as well as extracting the relevant information
from a message based on the intent'''

class Model():

    def __init__(self, args, datastore):
        self.args = args
        self.datastore = datastore

    #Primary method
    def get_intent(self, message: str) -> Intent:
        pass
