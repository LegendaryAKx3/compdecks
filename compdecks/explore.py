from flask import (
    Blueprint,
    render_template,
    request,
    render_template_string,
)

from compdecks.db import get_db

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


@bp.route("/explore")
def explore():
    # db = get_db()
    return render_template("explore/explore.html")


@bp.route("/search/", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        templ = """
                {% for deck in decks %}
                <tr>
                    <td>{{ deck.completed }}</td>
                    <th>{{ deck.name }}</td>
                    <td>{{ deck.questions }}</td>
                    <td>{{ deck.difficulty }}</td>
                    <th>
                        <a
                            href="/deck/{{ deck.id }}"
                            class="btn btn-outline btn-primary"
                        >
                            Play
                        </a>
                    </th>
                </tr>
                {% endfor %}
        """

        searchWord = request.form.get("search", None)

        db = get_db()
        matchDecks = db.execute(
            "SELECT * FROM decks WHERE name LIKE ?", ("%" + searchWord + "%",)
        ).fetchall()

        return render_template_string(templ, decks=matchDecks)
    # TODO: send all decks if its a GET
    return render_template("explore/explore.html")
