CREATE TABLE Students(
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(60) NOT NULL,
    last_name VARCHAR(60) NOT NULL,
    email VARCHAR(255) NOT NULL
);

INSERT INTO Students(first_name, last_name, email) VALUES 
    ('Homer', 'Simpson', 'hsimpson@springfieldnuclear.com'),
    ('Carl', 'Carlson', 'ccarlson@springfieldnuclear.com'),
    ('Lenny', 'Lenord', 'llenord@springfieldnuclear.com'),
    ('Bart', 'Simpson', 'skateordie@yahoo.com'),
    ('Lisa', 'Simpson', 'jazzqueen12@hotmail.com'),
    ('Otto', 'Mann', 'otto@otto.de'),
    ('Waylon', 'Smithers', 'wsmithers@springfieldnuclear.com');

CREATE TABLE Classes(
    id  SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    language SMALLINT NOT NULL DEFAULT 1, /* 1 = python, 2 = ruby, 3 = javascript */
    start_on DATE,
    end_on DATE    
);

INSERT INTO Classes(name, language, start_on, end_on) VALUES 
    ('Ruby for Nuclear Automation', 2, '11/3/2014', '12/5/2014'),
    ('Python Dev Accelerator', 1, '10/6/2014', '11/28/2014'),
    ('Build Your First Website', 3, NULL, NULL);

CREATE TABLE Enrollments(
    student_id INTEGER REFERENCES Students(id),
    class_id INTEGER REFERENCES Classes(id)
);

INSERT INTO Enrollments VALUES
    (1, 1),
    (2, 1),
    (3, 1),
    (6, 1),
    (4, 3),
    (5, 2);
