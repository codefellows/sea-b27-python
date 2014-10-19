CREATE TABLE Room(
    id SERIAL PRIMARY KEY,
    building VARCHAR(20),
    room_number VARCHAR(5)
);

INSERT INTO Room(building, room_number) VALUES
    ('511 Bldg', 'Easy'),
    ('511 Bldg', 'East');

CREATE TABLE Teachers(
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    department VARCHAR(255)
);

INSERT INTO Teachers(name, department) VALUES
    ('Mrs. Krabappel', '4th Grade'),
    ('Mrs. Hoover', '2nd Grade'),
    ('Hans Moleman', 'Ruby'),
    ('Artie Ziff', 'Python'),
    ('Kirk Van Houten', 'JavaScript');

ALTER TABLE Classes ADD COLUMN
    teacher_id INTEGER REFERENCES Teachers(id);

ALTER TABLE Classes ADD COLUMN
    room_id INTEGER REFERENCES Room(id);

