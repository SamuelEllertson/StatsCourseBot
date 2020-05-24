
import json
from dataclasses import dataclass, field

import pymysql.cursors
import pymysql.connections
import warnings

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
    id              : int
    prereqs         : str
    units           : str
    title           : str
    about           : str
    coding_involved : bool = False
    elective        : bool = False
    terms           : set  = field(default_factory=set)

    def as_list(self):
        return [
            self.id, 
            self.prereqs, 
            self.units, 
            self.title, 
            self.about, 
            self.coding_involved,
            self.elective, 
            ','.join(self.terms)
        ]

    def from_db(db_result):
        '''Constructs a new course from a database result object, doing the necessary transformations'''
        args = list(db_result)

        #convert 0,1 to actual boolean
        args[5] = bool(args[5])
        args[6] = bool(args[6])

        #convert comma seperated string to real set
        args[7] = set(args[7].split(","))

        return Course(*args)

@dataclass
class Section:
    course_id      : int
    section_id     : int
    times_offered  : str
    enrollment_cap : int
    teacher        : str

    def as_list(self):
        return [
            self.course_id,
            self.section_id,
            self.times_offered,
            self.enrollment_cap,
            self.teacher
        ]

    def from_db(db_result):
        return Section(*db_result)

class DataStore():

    def __init__(self, args):
        self.args = args

        with open("db_dev.json" if args.dev_mode else "db.json") as config_file:
            config = json.load(config_file)

        self.connection = pymysql.connect(config["host"], config["username"], config["password"], config["database"]) 

    def clear(self) -> None:
        '''Clears the database of all entries'''

        self.execute_query("DELETE FROM sections;")
        self.execute_query("DELETE FROM course;")

    def insert_course(self, course: Course) -> None:
        '''inserts course information into the database'''

        query = "INSERT IGNORE INTO course VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"

        self.execute_query(query, course.as_list())

    def insert_section(self, section: Section) -> None:
        '''inserts section into database'''
        query = "INSERT IGNORE INTO sections VALUES (%s, %s, %s, %s, %s);"

        self.execute_query(query, section.as_list())

    def get_course_ids(self) -> set:
        '''returns a set of all course ids'''
        query = "SELECT id FROM course"

        results = self.execute_query(query)

        return set(result[0] for result in results)
    
    def get_course_from_id(self, id: int) -> Course:
        '''Returns a course object from its course_id, or None if that id doesnt exist'''
        query = "SELECT * FROM course WHERE id = %s"

        result = self.execute_query(query, id, one_result=True)

        if result is None:
            return None

        return Course.from_db(result)

    ### Helper methods down here

    def execute_query(self, query: str, arguments: list = None, one_result : bool = False):
        with self.connection.cursor() as cursor:

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")

                if arguments is None:
                    cursor.execute(query)
                else:
                    cursor.execute(query, arguments)

                if one_result:
                    result = cursor.fetchone()
                else:
                    result = cursor.fetchall() 

        self.connection.commit()

        return result
