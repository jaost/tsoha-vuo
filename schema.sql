DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS feeds CASCADE;
DROP TABLE IF EXISTS items CASCADE;
DROP TABLE IF EXISTS votes CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);
CREATE TABLE feeds (
    id SERIAL PRIMARY KEY,
    secret TEXT UNIQUE,
    title TEXT,
    description TEXT,
    user_id INTEGER REFERENCES users,
    created_at TIMESTAMP
);
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    feed_id INTEGER REFERENCES feeds,
    path TEXT,
    description TEXT,
    user_id INTEGER REFERENCES users,
    created_at TIMESTAMP
);
CREATE TABLE votes (
    id SERIAL PRIMARY KEY,
    feed_id INTEGER REFERENCES feeds,
    item_id INTEGER REFERENCES items,
    user_id INTEGER REFERENCES users
);