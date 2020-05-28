from queryspec import Intent

def get_training_data():
    querys = open('query.txt')
    output = {}

    for line in querys:
        line_split = line.rstrip().split('|')
        if line_split[0] == 'B4':
            if line_split[3] == 'COURSE_OFFERED_IN_TERM':
                output[line_split[1]] = Intent.COURSE_OFFERED_IN_TERM
            elif line_split[3] == 'TERMS_COURSE_OFFERED':
                output[line_split[1]] = Intent.TERMS_COURSE_OFFERED
            elif line_split[3] == 'NUMBER_OF_TERMS_COURSE_OFFERED':
                output[line_split[1]] = Intent.NUMBER_OF_TERMS_COURSE_OFFERED
            elif line_split[3] == 'DOES_COURSE_INVOLVE_CODING':
                output[line_split[1]] = Intent.DOES_COURSE_INVOLVE_CODING
            elif line_split[3] == 'WHAT_COURSES_INVOLVE_CODING':
                output[line_split[1]] = Intent.WHAT_COURSES_INVOLVE_CODING
            elif line_split[3] == 'TEACHERS_OF_COURSE_CURRENT':
                output[line_split[1]] = Intent.TEACHERS_OF_COURSE_CURRENT
            elif line_split[3] == 'PROFESSOR_COURSES_CURRENT':
                output[line_split[1]] = Intent.PROFESSOR_COURSES_CURRENT
            elif line_split[3] == 'TEACHERS_OF_COURSE_NEXT':
                output[line_split[1]] = Intent.TEACHERS_OF_COURSE_NEXT
            elif line_split[3] == 'PROFESSOR_COURSES_NEXT':
                output[line_split[1]] = Intent.PROFESSOR_COURSES_NEXT
            elif line_split[3] == 'IS_COURSE_ELECTIVE':
                output[line_split[1]] = Intent.IS_COURSE_ELECTIVE
            elif line_split[3] == 'TYPE_OF_COURSE':
                output[line_split[1]] = Intent.TYPE_OF_COURSE
            elif line_split[3] == 'APPROVED_ELECTIVES':
                output[line_split[1]] = Intent.APPROVED_ELECTIVES
            elif line_split[3] == 'ELECTIVES_OFFERED_CURRENT':
                output[line_split[1]] = Intent.ELECTIVES_OFFERED_CURRENT
            elif line_split[3] == 'ELECTIVES_OFFERED_NEXT':
                output[line_split[1]] = Intent.ELECTIVES_OFFERED_NEXT
            elif line_split[3] == 'DESCRIPTION_OF_COURSE':
                output[line_split[1]] = Intent.DESCRIPTION_OF_COURSE
            elif line_split[3] == 'FIND_COURSE_ABOUT_TOPIC':
                output[line_split[1]] = Intent.FIND_COURSE_ABOUT_TOPIC
            elif line_split[3] == 'TIMES_COURSE_OFFERED_CURRENT':
                output[line_split[1]] = Intent.TIMES_COURSE_OFFERED_CURRENT
            elif line_split[3] == 'TIMES_COURSE_OFFERED_NEXT':
                output[line_split[1]] = Intent.TIMES_COURSE_OFFERED_NEXT
            elif line_split[3] == 'UNITS_OF_COURSE':
                output[line_split[1]] = Intent.UNITS_OF_COURSE
            elif line_split[3] == 'HOURS_OF_COURSE':
                output[line_split[1]] = Intent.HOURS_OF_COURSE
            elif line_split[3] == 'PREREQS_OF_COURSE':
                output[line_split[1]] = Intent.PREREQS_OF_COURSE
            elif line_split[3] == 'DOES_COURSE_HAVE_PREREQS':
                output[line_split[1]] = Intent.DOES_COURSE_HAVE_PREREQS
            elif line_split[3] == 'TITLE_OF_COURSE':
                output[line_split[1]] = Intent.TITLE_OF_COURSE
            elif line_split[3] == 'COURSE_ID_OF_COURSE':
                output[line_split[1]] = Intent.COURSE_ID_OF_COURSE
            elif line_split[3] == 'LEVEL_OF_COURSE':
                output[line_split[1]] = Intent.LEVEL_OF_COURSE
            elif line_split[3] == 'ENROLLMENT_CAP_OF_COURSE_CURRENT':
                output[line_split[1]] = Intent.ENROLLMENT_CAP_OF_COURSE_CURRENT
            elif line_split[3] == 'ENROLLMENT_CAP_OF_COURSE_NEXT':
                output[line_split[1]] = Intent.ENROLLMENT_CAP_OF_COURSE_NEXT
            else:
                output[line_split[1]] = Intent.UNKNOWN
    
    return output

print(get_training_data())
