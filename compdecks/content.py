from flask import Blueprint, render_template, request, session

from compdecks.auth import login_required
from compdecks.db import get_db
import csv
import random

# content does not have a url_prefix
bp = Blueprint("content", __name__)


class Deck:
    def __init__(self, path: str):
        self.questions: list[tuple] = []
        self.load(path)

    def load(self, path: str) -> None:
        with open(path, "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:
                    question, answer = row
                    self.questions.append((question, answer))
            # TODO: make sure it only shuffles one layer down
            random.shuffle(self.questions)


@bp.route("/")
@login_required
def index():
    # db = get_db()
    return render_template("content/index.html", title="Hello")


@bp.route("/create", methods=["GET", "POST"])
def create_deck():
    if request.method == "GET":
        ...
        # Figure out how csv file editing system will work
    elif request.method == "POST":
        ...
    return render_template("content/create.html")


@bp.route("/deck/<int:deck_id>", methods=["GET"])
def deck_details(deck_id: int):
    db = get_db()
    deck = db.execute("SELECT * FROM decks WHERE id IS ?", (str(deck_id),)).fetchone()
    return render_template("content/deck_details.html", deck=deck)


# does this need a seperate route getting the same info or can we somehow chain off the deck details?
@bp.route("/deck/play/<int:deck_id>", methods=["GET", "POST"])
def deck_play(deck_id: int):
    # TODO: VERY NOT DONE
    db = get_db()
    path = db.execute(
        "SELECT file_path FROM decks WHERE id IS ?", (str(deck_id),)
    ).fetchone()

    (path,) = path
    deck = Deck(path)
    questions: list[tuple] = deck.questions


@bp.route("/settings", methods=["GET", "POST"])
def settings():
    return render_template("content/settings.html")
