
import argparse
from argparse import ArgumentDefaultsHelpFormatter as Formatter
from datastore import DataStore
from iohandler import IOHandler

def get_args():
    parser = argparse.ArgumentParser(description='Chatbot that answers questions about CalPoly Stats Courses', formatter_class=Formatter)
    parser.add_argument('-v',            dest="verbose",     action="store_true", help='Toggles verbose output')
    parser.add_argument('--irc',         dest="use_irc",     action="store_true", help='Use irc instead of the terminal')
    parser.add_argument('--irc-host',    dest="irc_host",    metavar= "host",    default='irc.freenode.net', help='Sets irc host')
    parser.add_argument('--irc-channel', dest="irc_channel", metavar= "channel", default='#CSC466',          help='sets irc channel')
    parser.add_argument('--irc-port',    dest="irc_port",    metavar= "port",    default=6667, type=int,     help='sets irc port')
    parser.add_argument('--bot-name',    dest="bot_name",    metavar= "name",    default='StatsCourseBot',   help='Sets bot name')
    return parser.parse_args()

def main():
    args = get_args()

    datastore = DataStore(args)
    iohandler = IOHandler(args, datastore)

    iohandler.listen()

if __name__ == '__main__':
    main()