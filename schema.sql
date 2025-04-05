CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE images (
    id INTEGER PRIMARY KEY,
    title TEXT,
    kuvaus TEXT,
    genre TEXT,
    user_id INTEGER REFERENCES users,
    date_added TEXT
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    image_id INTEGER,
    comment TEXT
    user_id INTEGER REFERENCES users
    date_added TEXT
);