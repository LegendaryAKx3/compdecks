from flask import Blueprint, render_template, request, session, redirect, url_for, flash

from compdecks.auth import login_required
from compdecks.db import get_db
from compdecks.deck import Deck

from werkzeug.utils import secure_filename

import os
import csv

# content does not have a url_prefix
bp = Blueprint("content", __name__)

# better way? :FIXME:
loaded_decks = {}


@bp.route("/")
@login_required
def index():
    db = get_db()
    featDecks = db.execute(
        "SELECT * FROM DECKS order by plays desc limit 6;"
    ).fetchall()
    return render_template("content/index.html", decks=featDecks)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'csv'}

@bp.route("/create", methods=["GET", "POST"])
@login_required
def create_deck():
    if request.method == "GET":
        ...
        # Figure out how csv file editing system will work
    elif request.method == "POST":
        db = get_db()
        title = request.form["title"]
        description = request.form["description"]
        user = db.execute("select * from users where id is ?", (str(session["user_id"]))).fetchone()

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect("/create")
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return redirect("/create")

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join("/user_uploads/", filename)
            for filename in db.execute("select file_path from decks;").fetchall():
                if filename == file_path:
                    flash("File is already in database")
                    return redirect("/create")
            file.save(file_path)
        
        with open(filename) as f:
            length = sum(1 for line in f)

        #TODO how will the csv come through from the frontend?
        db.execute(
                "insert into decks (owner, name, description, file_path, length) values (?, ?, ?, ?, ?);",
                (user["username"], title, description, file_path, length),
            )
        redirect("/")
    return render_template("content/create.html")


@bp.route("/deck/<int:deck_id>", methods=["GET"])
@login_required
def deck_details(deck_id: int):
    db = get_db()
    deck = db.execute("SELECT * FROM decks WHERE id IS ?", (str(deck_id),)).fetchone()
    leaderboard = db.execute(
        "select * from leaderboards where deck_id is ? order by score desc limit 6",
        (str(deck_id),),
    )
    return render_template(
        "content/deck_details.html", deck=deck, leaderboard=leaderboard
    )


# does this need a seperate route getting the same info or can we somehow chain off the deck details?
@bp.route("/deck/play/<int:deck_id>", methods=["GET", "POST"])
@login_required
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
            username = db.execute(
                "SELECT username FROM users WHERE id IS ?;", str(session["user_id"])
            ).fetchall()
            username = username[0]["username"]
            db.execute(
                "insert into leaderboards (deck_id, username, score) values (?, ?, ?);",
                (deck_id, username, session["score"]),
            )
            db.execute("update decks set plays = plays + 1 where id = ?;", str(deck_id))
            db.commit()
            session["id"] = deck_id
            return redirect(url_for("content.results"))
        else:
            session["question"] += 1

        return render_template(
            "content/question.html",
            id=deck_id,
            question=questions[session["question"]][0],
        )


@bp.route("/result", methods=["GET"])
@login_required
def results():
    score = None
    if "score" in session:
        score = session["score"]
        session.pop("score", None)

    if "question" in session:
        session.pop("question", None)

    if "id" in session:
        id = session["id"]
        session.pop("id", None)

    if session["user_id"] in loaded_decks:
        total = len(loaded_decks[session["user_id"]])
        del loaded_decks[session["user_id"]]
    else:
        # still form bug with back button from home page.
        return redirect("/")

    return render_template("content/result.html", score=score, total=total, id=id)



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
