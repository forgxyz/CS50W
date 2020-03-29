import json, os, requests

from flask import Flask, url_for, redirect, render_template, request, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from helpers import login_required


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# global variables
TABLE = 'test_users2'
REV_TABLE = 'reviews_test'

# store your goodreads API key as a json dictionary or delete this and hard code the key
with open('goodreads.json') as f:
    GR_KEY = json.load(f)['key']

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/book/<string:isbn>", methods=['GET', 'POST'])
@login_required
def book_lookup(isbn):
    """Load the book information page
        Title, author year from books table
        bookguru reviews from reviews table
        goodreads reviews from API (TBD)"""
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchall()
    if len(book) == 0:
        return render_template("index.html", msg=f"<div class='alert alert-danger' role='alert'><h3 class='alert-heading'>Invalid ISBN.</h3>Please try again.</div>")
    # check for reviews
    reviews = db.execute(f"SELECT r.review, r.stars, r.user_id, u.username FROM {REV_TABLE} r JOIN {TABLE} u ON r.user_id=u.id WHERE isbn = :isbn", {"isbn": isbn}).fetchall()
    if len(reviews) == 0:
        reviews = None
    summary = db.execute(f"SELECT ROUND(AVG(stars), 2) AS avg, COUNT(stars) AS count FROM {REV_TABLE} WHERE isbn = :isbn", {"isbn": isbn}).first()
    db.commit() # do I need to commit when I am just SELECTing? is that also a transaction, or just when INSERTing? ... what harm does it do to have it
    # pull goodreads statistics
    res = requests.get(f"https://goodreads.com/book/review_counts.json", params={"key": GR_KEY, "isbns": isbn})
    try:
        goodreads = res.json()['books'][0]
    except:
        return render_template("index.html", msg="<div class='alert alert-error' role='alert'><h3 class='alert-heading'>API Error.</h3>Error connecting to the Goodreads API. Please report error.</div>")
    return render_template("book.html", book=book[0], reviews=reviews, summary=summary, goodreads=goodreads)


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
        return render_template("login.html", msg=f"<div class='alert alert-danger' role='alert'><h3 class='alert-heading'>Username {username} not found!</h3>Please <a href='/register' class='alert-link'>register</a> or log in again.</div>")

    # if it does, check the password
    password = request.form["password"]
    if password != db.execute(f"SELECT password FROM {TABLE} WHERE username = :username", {"username" :username}).first()[0]:
        # password does not match. close tx and send error
        db.commit()
        return render_template("login.html", msg=f"<div class='alert alert-danger' role='alert'><h3 class='alert-heading'>Incorrect username or password.</h3>Please <a href='/register' class='alert-link'>register</a> or log in again.</div>")
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


@app.route("/post_review", methods=['GET', 'POST'])
@login_required
def post_review():
    # collect user id
    user_id = session.get("user_id")[0]
    # collect isbn
    isbn = request.form["isbn"]
    stars = request.form.get("stars")
    review = request.form.get("review")
    # TODO:
    # check to make sure the user has not reviewed this book before
    if db.execute(f"SELECT * FROM {REV_TABLE} WHERE user_id = :user_id AND isbn = :isbn", {"user_id": user_id, "isbn": isbn}).rowcount > 0:
        db.commit()
        return render_template("index.html", msg="<div class='alert alert-danger' role='alert'><h3 class='alert-heading'>Unable to post review.</h3>You may only review a book once!</div>")
    # user_id=user_id AND isbn=isbn
    # else - ok to post
    # add user id, isbn, stars, review to database
    db.execute(f"INSERT INTO {REV_TABLE} (user_id, isbn, stars, review) VALUES (:user_id, :isbn, :stars, :review);", {"user_id": user_id, "isbn": isbn, "stars": stars, "review": review})
    db.commit() # DON'T FORGET ME
    return render_template("index.html", msg="<div class='alert alert-success' role='alert'><h3 class='alert-heading'>Success!</h3>Thanks for your review.</div>")


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
        return render_template("register.html", msg=f"<div class='alert alert-danger' role='alert'><h3 class='alert-heading'>{username} is already registered!</h3>Please try again.</div>")

    # username does not exist, add the un/pw to table & grab the id
    db.execute(f"INSERT INTO {TABLE} (username, password) VALUES (:username, :password);", {"username": username, "password": request.form["password"]})
    id = db.execute(f"SELECT id FROM {TABLE} WHERE username = :username", {"username": username}).first()
    db.commit()

    # store id in session
    session["user_id"] = id
    session["username"] = username
    return redirect("/")


@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    query = f"%{request.form.get('q')}%"
    # this is weird. It didn't accept request.form['q'] due to a KeyError but request.form.get('q') is fine. why?
    res = db.execute(f"SELECT * FROM books WHERE isbn ILIKE :query OR title ILIKE :query OR author ILIKE :query", {"query": query}).fetchall()
    if len(res) == 0:
        return render_template("index.html", msg=f"<div class='alert alert-primary' role='alert'><h3 class='alert-heading'>Please try again</h3>No matches found.</div>")
    return render_template("results.html", result=res, num=len(res))
