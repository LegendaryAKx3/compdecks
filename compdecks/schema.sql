-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS decks;
DROP TABLE IF EXISTS leaderboards;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE decks (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    owner TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    file_path TEXT NOT NULL,
    length INTEGER NOT NULL,
    plays INTEGER DEFAULT 0
);


-- Keep track of all user leaderboard positions
CREATE TABLE leaderboards (
    deck_id INTEGER NOT NULL,
    username TEXT NOT NULL,
    score DEFAULT 0
);