-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS decks;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

-- TODO store questions and answers for the deck in database
CREATE TABLE decks (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    owner_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    file_path TEXT NOT NULL
);

-- Keep track of all user leaderboard positions
CREATE TABLE leaderboards (
    deck_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    username TEXT NOT NULL,
    position INTEGER NOT NULL
)