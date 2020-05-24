
import os, sys, random, requests, re
from bs4 import BeautifulSoup
from datastore import Course, Section
from main import get_args
from datastore import DataStore


"""This file will be run entirely independantly of the rest of the code. Its job is to scrape the catalog
and any other relevant website, collection all the stats course data, and populate the database"""


def main():
    courses = scrape_courses()
    args = get_args()
    datastore = DataStore(args)
    datastore.clear()
    for i in range(len(courses)):
        print(courses[i].as_list())
        datastore.insert_course(courses[i])
        
        print(courses[i])

    print(courses)
    sections = scrape_sections()
    for section in sections:
        print(section)

def scrape_courses():
    """Scrapes http://catalog.calpoly.edu/coursesaz/stat/ and https://registrar.calpoly.edu/term-typically-offered for course data."""

    courses = []

    # obtain the content of the URL in HTML
    url = "http://catalog.calpoly.edu/coursesaz/stat/"
    myRequest = requests.get(url)

    # Create a soup object that parses the HTML
    soup = BeautifulSoup(myRequest.text, "html.parser")

    # step through the tag hierarchy
    raw_courses = soup.find_all("div", attrs={"class": "courseblock"})
    for course in raw_courses:
        coding_involved = False
        id_and_title = (
            course.find("p", {"class": "courseblocktitle"}).get_text().strip()
        )
        units = (
            course.find("span", {"class": "courseblockhours"})
            .get_text()
            .strip()
            .split(" ")[0]
        )
        id_and_title = id_and_title.split(".")
        id = id_and_title[0].split("\xa0")[1]
        title = id_and_title[1].strip()
        paragraphs = course.findAll("p")
        prereqs = ""
        reccomended = ""
        if len(paragraphs) == 5:
            ge_areas = re.findall(r"Area (\w+)", paragraphs[1].text)
        prereqs_raw = (
            course.find("div", {"class": "noindent courseextendedwrap"})
            .get_text()
            .split()
        )
        desc = (
            course.find("div", {"class": "courseblockdesc"})
            .get_text()
            .replace("\n", "")
        )
        coding_involved = False
        if "software" in desc:
            coding_involved = True
        for i in range(len(prereqs_raw)):
            if prereqs_raw[i].endswith("Prerequisite:") or prereqs_raw[i].endswith("Corequisite:"):
                prereqs = " ".join(prereqs_raw[i + 1:])
            if prereqs_raw[i].endswith("Reccomended:"):
                reccomended = " ".join(prereqs_raw[i:])

        courses.append(
            Course(int(id), prereqs, units, title, desc, coding_involved, False, {})
        )

    url = "https://tto.calpoly.edu/csv-to-html-table-master/tto/Course_Term_Typically_Offered.csv"

    terms = requests.get(url).text.split("\n")
    course_terms = {}
    for row in terms:
        data = row.split(",")
        if data[0].split("-")[0] == "STAT":
            course_terms[int(data[0].split("-")[1])] = (
                data[4],
                data[5],
                data[6],
                data[7],
            )

    for course in courses:
        course.terms = set([t for t in course_terms[course.id] if len(t) > 1])

    # obtain the content of the URL in HTML
    url = "http://catalog.calpoly.edu/collegesandprograms/collegeofsciencemathematics/statistics/bsstatistics/"
    myRequest = requests.get(url)

    # Create a soup object that parses the HTML
    soup = BeautifulSoup(myRequest.text, "html.parser")
    start = soup.find("td", text="Select from List A below:").parent
    electives = []
    for row in start.find_next_siblings("tr"):
        if row.find("td", text="SUPPORT COURSES") or row.find(
            "td", text="Select from List B below:"
        ):
            break
        else:
            id = row.find("td", {"class": "codecol"}).text.split()[1]
            #print(id)
            electives.append(int(id))
    for course in courses:
        if course.id in electives:
            course.elective = True

    return courses

def scrape_sections():
    """Scrapes https://schedules.calpoly.edu/subject_STAT_next.htm for next section data."""

    sections = []

    # obtain the content of the URL in HTML
    url = "https://schedules.calpoly.edu/subject_STAT_next.htm"
    myRequest = requests.get(url)

    # Create a soup object that parses the HTML
    soup = BeautifulSoup(myRequest.text, "html.parser")

    # step through the tag hierarchy
    table = soup.find_all("tr", attrs={"class": "entry1 active"})

    for row in table:
        id = int(row.find("td", attrs={"class": "courseName active"}).find("a")["title"].split(" ")[1])
        section = int(row.find("td", attrs={"class": "courseSection"}).text)
        days = row.find("td", attrs={"class": "courseDays"}).text.strip()
        start_time = row.find("td", attrs={"class": "startTime"}).text.strip()
        end_time = row.find("td", attrs={"class": "endTime"}).text.strip()
        teacher = row.find("td", attrs={"class": "personName"}).find("a").text
        cap = int(row.find_all("td", attrs={"class": "count"})[1].text)
        times_offered = ""
        if len(days) > 0 and len(start_time) > 0 and len(end_time) > 0:
            times_offered = days + " " + start_time + "-" + end_time
        sections.append(Section(id, section, times_offered, cap, teacher))


    return sections



if __name__ == "__main__":
    main()

