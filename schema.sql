DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS images;
DROP TABLE IF EXISTS classes;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT,
    user_description TEXT,
    profile_pic BLOB
);

CREATE TABLE images (
    id INTEGER PRIMARY KEY,
    title TEXT,
    image_description TEXT,
    genre TEXT,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    date_added TEXT,
    image MEDIUMBLOB
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    image_id INTEGER REFERENCES images(id) ON DELETE CASCADE,
    comment TEXT,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    date_added TEXT,
    image_title TEXT
);

CREATE TABLE grades (
    id INTEGER PRIMARY KEY,
    image_id INTEGER REFERENCES images(id) ON DELETE CASCADE,
    grade INTEGER,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE chatbox (
    id INTEGER PRIMARY KEY,
    user TEXT,
    messages TEXT
);