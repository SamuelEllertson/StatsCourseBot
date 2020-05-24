
import argparse
from argparse import ArgumentDefaultsHelpFormatter as Formatter
from datastore import DataStore
from datastore import Course
from datastore import Section
# from iohandler import IOHandler

'''This handles parsing arguments, initializing the DataStore and IOHandler, and starts listening and
responding to messages.

Aside from some error handling and recovery which can be added later, its essentially complete'''

def get_args():
    parser = argparse.ArgumentParser(description='Chatbot that answers questions about CalPoly Stats Courses', formatter_class=Formatter)
    parser.add_argument('-v',            dest="verbose",     action="store_true", help='Toggles verbose output')
    parser.add_argument('--dev',         dest="dev_mode",    action="store_true", help='Turns on development mode')
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



def test():
    args = get_args()
    datastore = DataStore(args)
    #datastore.test_db()
    course = Course(1, "fun", "class", "good", "stuff", 0, 1, "winter")
    datastore.insert_course(course)
    course = Course(12, "fun", "class", "good", "stuff", 0, 1, "winter")
    datastore.insert_course(course)
    course = Course(112, "fun", "class", "good", "stuff", 0, 1, "winter")
    datastore.insert_course(course)
    course = Course(11231, "fun", "class", "good", "stuff", 0, 1, "winter")
    datastore.insert_course(course)
    course = Course(1231, "fun", "class", "good", "stuff", 0, 1, "winter")
    datastore.insert_course(course)
    course = Course(1231122, "fun", "class", "good", "stuff", 0, 1, "winter")
    section = Section(1,2, "hi", 3, "classfun")

    
    datastore.insert_section(section)
    print(datastore.get_course_ids())
    print(datastore.get_course_from_id(1))
    
if __name__ == '__main__':
    #main()
    test()

    