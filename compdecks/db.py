import sqlite3
import csv
import os

import click
from flask import current_app, g


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


@click.command("init-data")
def init_data_command():
    """Insert test data into the decks table."""
    db = get_db()
    users_data = [
        (1, "Bob", 10),
        (1, "Jack", 8),
        (1, "Terry", 9),
        (2, "Steven", 10),
        (2, "Chris", 5),
        (2, "Sandra", 5),
        (3, "Ernie", 5),
        (3, "Jane", 2),
        (2, "Sarah", 1),
        (2, "John", 5),
    ]
    decks_data = [
        ("Sarah", "Math Quiz", "A Math Deck", "compdecks/user_uploads/math.csv", 4),
        (
            "John",
            "History Trivia",
            "A History Deck",
            "compdecks/user_uploads/history.csv",
            4,
        ),
        (
            "Edwin",
            "Science Flashcards",
            "A Science Deck",
            "compdecks/user_uploads/science.csv",
            4,
        ),
    ]
    db.executemany(
        "INSERT INTO decks (owner, name, description, file_path, length) VALUES (?, ?, ?, ?, ?)",
        decks_data,
    )
    db.executemany(
        "INSERT INTO leaderboards (deck_id, username, score) VALUES (?, ?, ?)",
        users_data,
    )
    db.commit()
    click.echo("Inserted test data into the decks table.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(init_data_command)
