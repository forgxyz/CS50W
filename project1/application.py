import os

from flask import Flask, session, render_template, request, redirect, g, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from helpers import login_required

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


TABLE = 'test_users2'

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["EXPLAIN_TEMPLATE_LOADING"] = True
Session(app)


# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if session.get("user_id") != None:
            return redirect("/")
        return render_template("login.html")

    username = request.form["username"]
    # check username
    if db.execute(f"SELECT * FROM {TABLE} WHERE username = :username", {"username" : username}).rowcount == 0:
        # if 0 rows returned, the username is not correct
        db.commit()
        return render_template("login.html", msg = f"<div class='alert alert-danger' role='alert'><h3 class='alert-heading'>Username {username} not found!</h3> Please <a href='/register' class='alert-link'>register</a> or log in again.</div>")

    # if it does, check the password
    password = request.form["password"]
    if password != db.execute(f"SELECT password FROM {TABLE} WHERE username = :username", {"username" :username}).first()[0]:
        # password does not match. close tx and send error
        db.commit()
        return render_template("login.html", msg = f"<div class='alert alert-danger' role='alert'><h3 class='alert-heading'>Incorrect username or password.</h3> Please <a href='/register' class='alert-link'>register</a> or log in again.</div>")
    id = db.execute(f"SELECT id FROM {TABLE} WHERE username = :username", {"username": username}).first()[0]
    db.commit()
    # yay! if you made it here you are a registed user or successful hacker
    # store id in session
    session["user_id"] = id
    session["username"] = username
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# register a new user
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        if session.get("user_id") != None:
            return redirect("/")
        return render_template("register.html")

    username = request.form["username"]
    if db.execute(f"SELECT * FROM {TABLE} WHERE username = :username", {"username": username}).rowcount > 0:
        # the username already exists, try again
        db.commit()
        return render_template("register.html", msg = f"<div class='alert alert-danger' role='alert'><h3 class='alert-heading'>{username} is already registered!</h3> Please try again.</div>")

    # username does not exist, add the un/pw to table & grab the id
    db.execute(f"INSERT INTO {TABLE} (username, password) VALUES (:username, :password);", {"username": username, "password": request.form["password"]})
    id = db.execute(f"SELECT id FROM {TABLE} WHERE username = :username", {"username": username}).first()[0]
    db.commit()

    # store id in session
    session["user_id"] = id
    session["username"] = username
    return redirect("/")
