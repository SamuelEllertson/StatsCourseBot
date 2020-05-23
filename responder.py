
"""This class is responsible for dealing with the content of a users message and generating responses."""

from model import Model
from queryspec import Intent

'''Takes in a message from the user, and uses its model to create a response message'''

class Responder():

    def __init__(self, args, datastore, iohandler):
        self.args = args
        self.datastore = datastore
        self.iohandler = iohandler
        self.model = Model(args, datastore, iohandler)

    def get_response(self, message: str) -> str:
        '''The primary function of the Responder. Takes in a raw message from the user
        and returns a final response message'''

        return message #currently just echoing the message

    #Could be made better
    def is_signaling_exit(self, message):
        '''returns true if message intends to end the program'''
        message = message.strip().lower()

        if message in ('quit', 'bye', 'exit', 'q'):
            return True

        return False

    def get_exit_phrase(self):
        return "Bye"

    # Helper methods down here