from flask import Blueprint, render_template, request, session, redirect, url_for

from compdecks.auth import login_required
from compdecks.db import get_db
import csv
import random

# content does not have a url_prefix
bp = Blueprint("content", __name__)

# better way? :FIXME:
loaded_decks = {}


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
    leaderboard = db.execute(
        "select * from leaderboards where deck_id is ? order by score desc limit 3",
        (str(deck_id),),
    )
    return render_template(
        "content/deck_details.html", deck=deck, leaderboard=leaderboard
    )


# does this need a seperate route getting the same info or can we somehow chain off the deck details?
@bp.route("/deck/play/<int:deck_id>", methods=["GET", "POST"])
def deck_play(deck_id: int):

    # load the deck and save into the in memory loaded decks
    if session["user_id"] not in loaded_decks:
        loaded_decks[session["user_id"]] = load_deck(session["user_id"])

    questions: list[tuple] = loaded_decks[session["user_id"]]

    if "question" not in session:
        session["question"] = 0

    if "score" not in session:
        session["score"] = 0

    if request.method == "GET":
        if "question" in session:
            session.pop("question")
        if "score" in session:
            session.pop("score")

        return render_template(
            "content/question.html",
            id=deck_id,
            question=questions[0][0],
        )

    if request.method == "POST":
        db = get_db()
        user_answer = request.form["answer"]
        correct_answer = questions[session["question"]][1]

        # TODO: remove check later
        if user_answer.lower() == correct_answer.lower():
            session["score"] += 1

        if session["question"] >= len(questions) - 1:
            # RESULT
            # Record play and save score to leaderboard
            username = db.execute("SELECT username FROM users WHERE id IS ?;", session["user_id"]).fetchone()
            db.execute("insert into leaderboard (deck_id, username, score) (?, ?, ?);", deck_id, username, session["score"])
            db.execute("update decks plays = plays + 1 where id = ?;", deck_id)
            db.commit()
            return redirect(url_for("content.results"))
        else:
            session["question"] += 1

        return render_template(
            "content/question.html",
            id=deck_id,
            question=questions[session["question"]][0],
        )


@bp.route("/result", methods=["GET"])
def results():
    score = None
    if "score" in session:
        score = session["score"]
        session.pop("score", None)

    if "question" in session:
        session.pop("question", None)

    if session["user_id"] in loaded_decks:
        total = len(loaded_decks[session["user_id"]])
        del loaded_decks[session["user_id"]]
    else:
        # still form bug with back button from home page.
        return redirect("/")
    # TODO: save score to leaderboard

    return render_template("content/result.html", score=score, total=total)


@bp.route("/settings", methods=["GET", "POST"])
def settings():
    return render_template("content/settings.html")


def load_deck(deck_id: int) -> dict:
    """create an instance of Deck and return the questions"""
    db = get_db()
    path = db.execute(
        "SELECT file_path FROM decks WHERE id IS ?", (str(deck_id),)
    ).fetchone()

    (path,) = path
    deck = Deck(path)
    questions: list[tuple] = deck.questions
    return questions


def usertoid(user: str) -> int:
    """retrieve id from username"""
    db = get_db()
    id = db.execute("SELECT id FROM users WHERE username IS ?", (user,)).fetchone()
    return id
