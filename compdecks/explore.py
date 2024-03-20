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

from compdecks.db import get_db

bp = Blueprint("explore", __name__)


class User:
    id = 0

    def __init__(self, fname, lname, email, extra):
        User.id += 1
        self.id = User.id
        self.fname = fname
        self.lname = lname
        self.email = email
        self.extra = extra

    def search(self, word):
        if word is None:
            return False
        all = self.fname + self.lname + self.email + self.extra
        return word.lower() in all.lower()


users = [
    User("C", "My math deck", "10", "2"),
    User("N", "Spanish is good", "3", "2"),
    User("C", "Scary science", "105", "2"),
    User("N", "Awesome anthropology", "204", "2"),
    User("N", "Cool Chemistry", "14", "2"),
    User("P", "French", "3", "2"),
    User("P", "My latin deck", "49", "2"),
    User("N", "Comp sci", "590", "2"),
    User("C", "Business", "23", "2"),
    User("P", "Bio studying", "43", "2"),
    User("C", "Calc III", "87", "2"),
    User("N", "Hard economics test", "51", "2"),
]


@bp.route("/explore")
def explore():
    # db = get_db()
    return render_template("explore/explore.html")


@bp.route("/search/", methods=["POST"])
def search():
    templ = """
            {% for user in users %}
            <tr>
                <td>{{ user.id }}</td>
                <td>{{ user.fname }}</td>
                <td>{{ user.lname }}</td>
                <td>{{ user.email }}</td>
                <td>{{ user.extra }}</td>
            </tr>
            {% endfor %}
    """
    searchWord = request.form.get("search", None)
    matchusers = [user for user in users if user.search(searchWord)]
    return render_template_string(templ, users=matchusers)
