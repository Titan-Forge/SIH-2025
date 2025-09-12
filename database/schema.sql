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
INSERT INTO timetable (slot, subject, teacher ) VALUES ('Period1' , 'Maths', 'Mr. Sharma' );
VALUES ('Period 1', 1, 1)'
    ('Period 2', 2, 2);
 CREATE TABLE IF NOT EXISTS teachers ( id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL );
 CREATE TABLE IF NOT EXISTS subjects ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL );
 CREATE TABLE IF NOT EXISTS rooms ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL );
 CREATE TABLE IF NOT EXISTS timetable ( id INTEGER PRIMARY KEY AUTOINCREMENT, run_id TEXT,
 slot TEXT,
 subject TEXT,
 ROOM text,
 created_at TIMESTAMP DEFAULT
 CURRENT_TIMESTAMP
 );
 INSERT INTO teachers (name) VALUES
 ('Mr. Sharma'), ('Ms. Gupta');
 INSERT INTO subjects (name) VALUES
 ('Maths'), ('Physics');
 INSERT INTO rooms (name) VALUES
 ('Lab1'), ('Room101');

