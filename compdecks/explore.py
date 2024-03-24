import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    render_template_string,
)
from werkzeug.security import check_password_hash, generate_password_hash

from compdecks.db import get_db, close_db

bp = Blueprint("explore", __name__)


class Deck:
    def __init__(self, completed, title, questions, difficulty):
        self.completed = completed
        self.title = title
        self.questions = questions
        self.difficulty = difficulty

    def search(self, word):
        if word is None:
            return False
        return word.lower() in self.title.lower()


decks = [
    Deck("C", "My math deck", "10", "2"),
    Deck("N", "Spanish is good", "3", "2"),
    Deck("C", "Scary science", "105", "2"),
    Deck("N", "Awesome anthropology", "204", "2"),
    Deck("N", "Cool Chemistry", "14", "2"),
    Deck("P", "French", "3", "2"),
    Deck("P", "My latin deck", "49", "2"),
    Deck("N", "Comp sci", "590", "2"),
    Deck("C", "Business", "23", "2"),
    Deck("P", "Bio studying", "43", "2"),
    Deck("C", "Calc III", "87", "2"),
    Deck("N", "Hard economics test", "51", "2"),
]


@bp.route("/explore")
def explore():
    # db = get_db()
    return render_template("explore/explore.html")


@bp.route("/search/", methods=["POST"])
def search():

    searchWord = request.form.get("search", None)
    db = get_db()
    matchDecks = db.execute(
        "SELECT * FROM decks WHERE name LIKE ?", ("%" + searchWord + "%",)
    )

    templ = """
            {% for deck in decks %}
            <tr class="odd:bg-gray-50">
                <td class="whitespace-nowrap px-4 py-2 text-gray-700">{{ deck.completed }}</td>
                <th class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap">{{ deck.title }}</th>
                <td class="whitespace-nowrap px-4 py-2 text-gray-700">{{ deck.questions }}</td>
                <td class="whitespace-nowrap px-4 py-2 text-gray-700">{{ deck.difficulty }}</td>
                <td class="whitespace-nowrap px-4 py-2">
                    <a
                        href="/quiz"
                        class="inline-block rounded bg-indigo-600 px-4 py-2 text-xs font-medium text-white hover:bg-indigo-700"
                    >
                        Play
                    </a>
                </td>
            </tr>
            {% endfor %}
    """

    # matchusers = [deck for deck in decks if deck.search(searchWord)]
    return render_template_string(templ, decks=matchDecks)
