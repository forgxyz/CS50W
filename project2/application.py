import os

from flask import Flask
from flask_socketio import SocketIO, emit

from helpers import *


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


@app.route("/")
@login_required
def index():
    return "Project 2: TODO"


@app.route("/login")
def login:
    """Display Name: When a user visits your web application for the first time, they should be prompted to type
    in a display name that will eventually be associated with every message the user sends.
    If a user closes the page and returns to your app later, the display name should still be remembered."""
    # like login but no password, not formally creating an account
    return "TODO"
