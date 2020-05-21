
# Adapted from bot by Joel Rosdahl <joel@rosdahl.net> and Foaad Khosmood

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad
from queue import Queue
from threading import Thread

class IRCBot(irc.bot.SingleServerIRCBot):

    def __init__(self, args):
        self.args = args
        irc.bot.SingleServerIRCBot.__init__(self, [(args.irc_host, args.irc_port)], args.bot_name, args.bot_name)
        self.channel = args.irc_channel

        #This is the queue that stores messages. The bot is run in a seperate thread, and pushes messages into the queue.
        self.messages = Queue()

        self.run_threaded()

    def send_message(self, message):
        self.connection.privmsg(self.channel, message)

    def get_message(self):
        return self.messages.get()

    def run_threaded(self):
        Thread(target=self.start, daemon=True).start()
    
    #modified to push messages to the message queue
    def on_pubmsg(self, c, e):
        a = e.arguments[0].split(":", 1)
        if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(self.connection.get_nickname()):
            message = a[1].strip()
            
            if self.args.verbose:
                print(f"[ircbot] received message: {message}")
            
            self.messages.put(message)
    
    # Everything else left as-is

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        self.do_command(e, e.arguments[0])


    def on_dccmsg(self, c, e):
        # non-chat DCC messages are raw bytes; decode as text
        text = e.arguments[0].decode('utf-8')
        c.privmsg("You said: " + text)

    def on_dccchat(self, c, e):
        if len(e.arguments) != 2:
            return
        args = e.arguments[1].split()
        if len(args) == 4:
            try:
                address = ip_numstr_to_quad(args[2])
                port = int(args[3])
            except ValueError:
                return
            self.dcc_connect(address, port)
