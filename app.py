from functools import wraps
from flask import Flask, render_template, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
import sqlite3

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def connect_db():
    connection = sqlite3.connect("CD.db")
    return connection

def login_required(f):
    """Code from CS50 finance"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("uuid") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

@app.route("/")
@login_required
def hello_world():
    return render_template("index.html", title="Hello")

# NOT WORKING CODE, NEEDS TO BE UPDATED FOR SQLITE3 LIBRARY
@app.route("/login")
def login():
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Check both username and password are submitted
        if (not request.form.get("username")) or (not request.form.get("password")):
            return render_template(
                "login.html")

        user = db.execute(
            "SELECT * FROM accounts WHERE username = ?", request.form.get("username")
        )
        # Ensure username exists and password is correct

        # HACK: len(user) != 1?
        if len(user) != 1 or not check_password_hash(
            user[0]["hash"], request.form.get("password")
        ):
            return render_template("login.html")

        # store account login status until session is cleared
        session["uuid"] = user[0]["id"]
        return redirect("/")

    else:
        return render_template("login.html")

# ALSO NEEDS TO BE UPDATED FOR SQLITE3
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # get form info and check validity

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return render_template(
                "register.html", error="Username field cannot be empty"
            )

        for entry in db.execute("SELECT username FROM accounts;"):
            if username == entry["username"]:
                return render_template(
                    "register.html", error="Username is Already Taken"
                )

        # check password valididty
        if password != confirmation or (not password) or (not confirmation):
            return render_template(
                "register.html", error="Invalid password or confirmation"
            )

        elif (len(password) < 8) or (password.lower() == password):
            return render_template(
                "register.html",
                error="Password Must be at Least 8 Characters Long and Contain a Capital Letter",
            )

        db.execute(
            "INSERT INTO accounts (username, hash) VALUES(?, ?);",
            username,
            generate_password_hash(password),
        )
        return redirect("/")
    return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/")


# TODO:
@app.route("/explore", methods=["GET", "POST"])
def explore():
    return render_template("explore.html")