from flask import (
    Blueprint,
    render_template,
    request,
    render_template_string,
)

from compdecks.db import get_db
from compdecks.auth import login_required

bp = Blueprint("explore", __name__)


@bp.route("/search/", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "POST":
        templ = """
                {% for deck in decks %}
                <tr>
                    <td>{{ deck.owner }}</td>
                    <th>{{ deck.name }}</td>
                    <td>{{ deck.length }}</td>
                    <th>
                        <a
                            href="/deck/{{ deck.id }}"
                            class="btn btn-outline btn-sm btn-primary"
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


@bp.route("/decks/", methods=["GET", "POST"])
@login_required
def decks():
    if request.method == "POST":
        templ = """
                {% for deck in decks %}
                <tr>
                    <td>{{ }}</td>
                    <th>{{ deck.name }}</td>
                    <td>{{ deck.length }}</td>
                    <th>
                        <a
                            href="/deck/{{ deck.id }}"
                            class="btn btn-outline btn-sm btn-primary"
                        >
                            Delete
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
    return render_template("explore/user_decks.html")
