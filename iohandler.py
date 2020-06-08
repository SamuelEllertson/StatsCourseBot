
from responder import Responder
from ircbot import IRCBot

'''This class handles all IO interaction with the user, it handles terminal/irc transparently. Use
its get_message, send_message, and ask_question methods for all user interaction

This class is basically already complete'''

class IOHandler():
    
    def __init__(self, args, datastore):
        self.args = args
        self.datastore = datastore
        self.responder = Responder(args, datastore, self)

        if args.use_irc:
            self.ircbot = IRCBot(args)

    def get_message(self) -> str:
        '''Returns the next message from the user'''
        if self.args.use_irc:
            return self.ircbot.get_message()

        return input("> ")

    def send_message(self, message: str) -> None:
        '''Sends a message to the user'''
        if self.args.use_irc:
            return self.ircbot.send_message(message)

        print(f"{self.args.bot_name}: {message}\n")

    def ask_question(self, question: str) -> str:
        '''Prompts the user with question, returns their response'''
        self.send_message(question)
        return self.get_message()

    def listen(self) -> None:
        '''Main loop of the chatbot. Gets messages, prints response. Returns when program is over'''

        while True:
            try:
                message = self.get_message()

                #Exit condition
                if self.responder.is_signaling_exit(message):
                    self.send_message(self.responder.get_exit_phrase())
                    return

                self.send_message(self.responder.get_response(message))

            except KeyboardInterrupt:
                self.send_message(self.responder.get_exit_phrase())
                break
