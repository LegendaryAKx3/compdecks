from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

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
        self.idx += 1
        if self.idx >= len(self.deck):
            return None
        return self.get_current_question

    # TODO: call this at some point
    def shuffle(self, deck):
        random.shuffle(deck)
        return deck


@bp.route("/")
def index():
    # db = get_db()
    return render_template("content/index.html", title="Hello")


@bp.route("/create", methods=["GET", "POST"])
def create_deck():
    if request.method == "POST":
        ...
        # Figure out how csv file editing system will work
    return render_template("create.html")


@bp.route("/deck/<int:deck_id>", methods=["GET"])
def deck_details(deck_id):
    # get deck details from the database
    ...

    # get questions from the deck
    ...

    # TODO: REMOVE, THIS IS FOR TESTING PURPOSES
    deck = Deck()
    return render_template("content/deck_details.html", deck=deck)


# THIS URL IS FOR TESTING. REMOVE LATER TODO:
test_quiz = Deck("test_quiz.csv")


@bp.route("/quiz", methods=["GET", "POST"])
def quiz():
    print(test_quiz.get_current_question())
    if request.method == "GET":
        return render_template(
            "content/quiz.html", question=test_quiz.get_current_question()
        )
    elif request.method == "POST":
        user_answer = request.form["answer"]
        is_correct = test_quiz.check_answer(user_answer)
        test_quiz.update_score(is_correct)
        next_question = test_quiz.next_question()
        if next_question:
            return render_template("content/quiz.html", question=next_question())
        else:
            return render_template(
                "content/result.html",
                score=test_quiz.score,
                total=test_quiz.deck_length(),
            )
