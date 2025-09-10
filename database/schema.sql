CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL);
CREATE TABLE subjects (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);

CREATE TABLE timetable (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  slot TEXT,
  subject_id INTEGER,
  teacher_id INTEGER
);
CREATE TABLE teachers (
    id  INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
create table subjects(
    id integer primary key AUTOINCREMENT,
    name text not null,
    teacher_id INTEGER,
    FOREIGN KEY(teacher_id)
    REFERENCES teachers(id)
);
CREATE TABLE timetable(
    id INTEGER primary key AUTOINCREMENT,
    slot TEXT NOT NULL,
    subject_id INTEGER,
    teacher_id INTEGER,
    FOREIGN KEY (subject_id)
    REFERENCES subjects(id),
    FOREIGN KEY (teacher_id)
    REFERENCES teachers(id)
);
INSERT INTO teachers (name)
VALUES ('Mr. Sharma'), ('Ms. Gupta');
INSERT INTO subjects (name)
VALUES ('Maths'),('Science');
INSERT INTO timetable (slot, subject_id, teacher_id)
VALUES ('Period 1', 1, 1)'
    ('Period 2', 2, 2);
    
