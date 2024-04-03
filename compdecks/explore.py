from flask import (
    Blueprint,
    render_template,
    request,
    render_template_string,
)

from compdecks.db import get_db

bp = Blueprint("explore", __name__)


@bp.route("/search/", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        templ = """
                {% for deck in decks %}
                <tr>
                    <th>{{ deck.name }}</td>
                    <td>{{ deck.length }}</td>
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
