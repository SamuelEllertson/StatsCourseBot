
import json
from dataclasses import dataclass, field

# import mysql.connector
# from mysql.connector import Error
import pymysql.cursors
import pymysql.connections

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
    title           : str
    prereqs         : str
    units           : str
    about           : str
    coding_involved : bool = False
    elective        : bool = False
    terms           : set  = field(default_factory=set)

@dataclass
class Section:
    course_id      : int
    section_id     : int
    times_offered  : str
    enrollment_cap : int
    teacher        : str

class DataStore():

    def __init__(self, args):
        self.args = args

        with open("db_dev.json" if args.dev_mode else "db.json") as config_file:
            config = json.load(config_file)
            print(config)

        self.connection = pymysql.connect(config["host"], config["username"], config["password"], config["database"]) 
        #create connection to db based on config. Here are the docs https://pynative.com/python-mysql-database-connection/

    ### 'public' methods up here

    def clear(self) -> None:
        '''Clears the database of all entries'''
        # cursor = self.connection.cursor()
        pass


    def insert_course(self, course: Course) -> None:
        '''inserts course information into the database'''
        with self.connection.cursor() as cursor:
        # cursor = self.connection.cursor()
            sql = """
            INSERT INTO course (id, prereqs, units, title, about, coding_involved, elective, terms)
                VALUES (course.id, course.prereqs, course.units, course.title, course.about, course.coding_involved
                course.elective, course.terms);
            """
            cursor.execute(sql)
        self.connection.commit()

    def insert_section(self, section: Section) -> None:
        '''inserts section into database'''
        #cursor = self.connection.cursor()
        with self.connection.cursor() as cursor:
            sql = """
            INSERT INTO sections (course_id, section_id, times_offered, enrollment_cap, teacher)
                VALUES (section.course_id, section.section_id, section.times_offered, section.enrollment_cap,
                 section.teacher);
            """
            cursor.execute(sql)
        self.connection.commit()


    def get_course_ids(self) -> set:
        '''returns a set of all course ids'''

        return set([302, 312, 315]) #dummy return value
    
    def get_course_from_id(self, id: int) -> Course:
        '''Returns a course object from its course_id, or None if that id doesnt exist'''

        return Course(1, "fake course", "no prereqs", "1-2", "this is a fake course description", False, True, set('fall'))

    ### Helper methods down here


    def test_db(self) -> None:
        cursor = self.connection.cursor()
        sql = "SELECT `*` FROM `Cities`"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
