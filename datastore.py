
import json
from dataclasses import dataclass

import mysql.connector
from mysql.connector import Error

'''Provides high level access methods to data stored in the database

All SQL queries should be aggregated here, abstracting that logic away from other parts of the code.
creates a connection to the database based on the db.json config file

as a baseline, create methods for:
    looking up a course based on various attributes,
    getting a set of all courses
    getting a set of course_id's, course_title's

unless it makes sense to otherwise, nearly everything here should return either a set, a Course, or None

Document your methods with a docstring, describing what it takes and what it returns, 
in both a successful and unsuccessful case

add a type hint to params, as shown below 

prefer returning None or an empty set instead of raising an error, unless it makes sense to otherwise

keep the 'public' methods up at the top, with internal methods at the bottom, so that its clear what is 
intended for use elsewhere in the code
'''

@dataclass
class Course:
    course_id:      int 
    course_title:   str
    course_prereqs: str
    course_units:   int
    course_desc:    str

class DataStore():

    def __init__(self, args):
        self.args = args

        with open("db.json") as config_file:
            config = json.load(config_file)

        self.connection = None #create connection to db based on config. Here are the docs https://pynative.com/python-mysql-database-connection/


    ### 'public' methods up here

    def get_course_ids(self) -> set:
        '''returns a set of all course ids'''

        return set([302, 312, 315]) #dummy return value
    
    def get_course_from_id(self, id: int) -> Course:
        '''Returns a course object from its course_id, or None if that id doesnt exist'''

        return Course(1, "fake course", "no prereqs", "0 units", "this is a fake course description")

    ### Helper methods down here