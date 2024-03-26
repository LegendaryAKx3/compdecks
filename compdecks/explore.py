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
                            href="/quiz"
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
    return render_template("explore/explore.html")
