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
