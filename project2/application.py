import os

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from helpers import *


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


@app.route("/")
@login_required
def index():
    name = session.get("username")
    return render_template("index.html", name=name)


@app.route("/home")
def home():
    return("THIS IS THE HOMEPAGE")


@app.route("/login")
def login():
    return render_template("index.html")
