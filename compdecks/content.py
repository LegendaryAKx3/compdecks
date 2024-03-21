from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from compdecks.auth import login_required
from compdecks.db import get_db

# content does not have a url_prefix
bp = Blueprint("content", __name__)


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


class Deck:
    def __init__(self):
        self.id = 1
        self.name = "Good Deck"
        self.owner = "Me 1"
        self.questions = "10"
        self.file_path = "/d//d/"


@bp.route("/deck/<int:deck_id>", methods=["GET"])
def deck_details(deck_id):
    # get deck details from the database
    ...

    # get questions from the deck
    ...

    # TODO: REMOVE, THIS IS FOR TESTING PURPOSES
    deck = Deck()
    return render_template("content/deck_details.html", deck=deck)
