
import argparse
from argparse import ArgumentDefaultsHelpFormatter as Formatter
from datastore import DataStore
from dataupdater import scrape_data
from iohandler import IOHandler
from model import Model
import nltk
from pathlib import Path

'''This handles parsing arguments, initializing the DataStore and IOHandler, and starts listening and
responding to messages.
Aside from some error handling and recovery which can be added later, its essentially complete'''

def get_args():
    parser = argparse.ArgumentParser(description='Chatbot that answers questions about CalPoly Stats Courses', formatter_class=Formatter)
    parser.add_argument('-v',            dest="verbose",     action="store_true", help='Toggles verbose output')
    parser.add_argument('--init',        dest="init",        action="store_true", help='initializes project')
    parser.add_argument('--dev',         dest="dev_mode",    action="store_true", help='Turns on development mode')
    parser.add_argument('--new-model',   dest="new_model",   action="store_true", help='Generate a new model instead of loading it')
    parser.add_argument('--scrape',      dest="scrape",      action="store_true", help='Scrape and update database instead of running the chatbot')
    parser.add_argument('--irc',         dest="use_irc",     action="store_true", help='Use irc instead of the terminal')
    parser.add_argument('--irc-host',    dest="irc_host",    metavar= "host",    default='irc.freenode.net', help='Sets irc host')
    parser.add_argument('--irc-channel', dest="irc_channel", metavar= "channel", default='#CSC466',          help='sets irc channel')
    parser.add_argument('--irc-port',    dest="irc_port",    metavar= "port",    default=6667, type=int,     help='sets irc port')
    parser.add_argument('--bot-name',    dest="bot_name",    metavar= "name",    default='StatsCourseBot',   help='Sets bot name')
    return parser.parse_args()

def init(args):

    if args.dev_mode and not Path("db_dev.json").exists():
        print("Create db_dev.json first")
        return
    elif not args.dev_mode and not Path("db.json").exists():
        print("Create db.json first")
        return

    print("Downloading nltk packages")
    nltk.download("stopwords")
    nltk.download("punkt")
    nltk.download("wordnet")
    nltk.download("averaged_perceptron_tagger")

    print("Creating the database tables")
    datastore = DataStore(args)
    datastore.create_tables()
    datastore.close()

    print("Creating the classifier")
    Model(args) 

    print("Scraping the data")
    scrape_data(args)

def main():
    args = get_args()

    if not Path("saved_model.cbm").exists() and not args.init:
        print("First run with --init to initialize the chatbot.")
        return

    if args.init:
        init(args)
        return

    if args.scrape:
        scrape_data(args)
        return

    datastore = DataStore(args)
    iohandler = IOHandler(args, datastore)

    iohandler.listen()


if __name__ == '__main__':
    main()