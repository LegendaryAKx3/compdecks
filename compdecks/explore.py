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
    User("abe", "vida", "abe@nowhere.com", "2"),
    User("betty", "b", "bb@nowhere.com", "2"),
    User("joe", "robinson", "jrobinson@nowhere.com", "2"),
    User("Luis", "Cortes", "Luis@somewhere.com", "2"),
    User("marty", "hinkle", "mhinkle@nowhere.com", "2"),
    User("matthew", "robinson", "mrobinson@nowhere.com", "2"),
    User("collin", "western", "cwest@nowhere.com", "2"),
    User("marty", "hinkle II", "mhinkle2@nowhere.com", "2"),
    User("joe", "robinson", "jrobinson@nowhere.com", "2"),
    User("juan", "vida", "juanvida@nowhere.com", "2"),
    User("marty", "hinkle III", "mhinkle3@nowhere.com", "2"),
    User("zoe", "omega", "zoe@nowhere.com", "2"),
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
