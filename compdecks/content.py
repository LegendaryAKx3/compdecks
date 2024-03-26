from flask import Blueprint, render_template, request

from compdecks.auth import login_required
from compdecks.db import get_db
import csv
import random

# content does not have a url_prefix
bp = Blueprint("content", __name__)


class Deck:
    def __init__(self, deck_file):
        self.deck = self.load(deck_file)
        self.idx = 0
        self.score = 0

    def load(self, deck_file):
        deck = []
        with open(deck_file, "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                question, answer = row
                deck.append((question, answer))

        return self.shuffle(deck)

    def get_current_question(self):
        return self.deck[self.idx]

    def check_answer(self, user_answer):
        _, correct_answer = self.get_current_question()
        # This may bite me later for subjects like chemistry...
        return user_answer.strip().lower() == correct_answer.lower()

    def update_score(self, is_correct: bool) -> None:
        if is_correct:
            self.score += 1

    def deck_length(self):
        return len(self.deck)

    def next_question(self):
        # TODO: how to fix index error?
        if self.idx + 1 >= len(self.deck):
            return None
        self.idx += 1
        return self.get_current_question

    # TODO: call this at some point
    def shuffle(self, deck):
        random.shuffle(deck)
        return deck


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
    if request.method == "GET":
        return render_template(
            "content/quiz.html", question=deck.get_current_question(), id=deck_id
        )
    elif request.method == "POST":
        user_answer = request.form["answer"]
        is_correct = deck.check_answer(user_answer)
        deck.update_score(is_correct)
        next_question = deck.next_question()
        if next_question:
            return render_template(
                "content/quiz.html", question=next_question(), deck=deck, id=deck_id
            )
        else:
            # TODO: fix, this is to stop the form resubmitting when reloading on the result screen
            score = deck.score
            total = deck.deck_length()
            return render_template(
                "content/result.html",
                score=score,
                total=total,
            )


@bp.route("/settings", methods=["GET", "POST"])
def settings():
    return render_template("content/settings.html")
