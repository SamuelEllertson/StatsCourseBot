drop table if exists sections;
drop table if exists course;

create table course (
    id int primary key,
    prereqs varchar(200),
    units varchar(10) not null,
    title varchar(100) not null,
    about varchar(500) not null,
    coding_involved boolean not null,
    elective boolean not null,
    terms SET("fall", "winter", "spring", "summer")
);

create table sections (
    course_id int not null,
    section_id int not null,
    times_offered varchar(50) not null,
    enrollment_cap int not null,
    teacher varchar(100) not null,
    current_quarter boolean not null,
    PRIMARY KEY (course_id, section_id, current_quarter),
    constraint FK_COURSE foreign key (course_id) references course(id) on delete cascade
);
