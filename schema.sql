DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS images;
DROP TABLE IF EXISTS classes;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT,
    kuvaus TEXT,
    image BLOB
);

CREATE TABLE images (
    id INTEGER PRIMARY KEY,
    title TEXT,
    kuvaus TEXT,
    genre TEXT,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    date_added TEXT
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