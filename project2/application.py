import os

from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY") # ???
socketio = SocketIO(app)

CHANNELS = []
CHANNEL_LIST = {}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/create", methods=['GET', 'POST'])
def create_channel(name = None):
    # id will be equal to the list index of the channel
    if request.method == 'POST':
        id = len(CHANNELS)
        CHANNELS.append({name: {"id": id, "messages": []}})
        CHANNEL_LIST[id] = name
        return True
    return "Coming soon..."

@app.route("/home")
def home():
    return "THIS IS THE HOMEPAGE"


@app.route("/post")
def post_message(channel, message, user):
    if channel not in CHANNEL_LIST.values():
        # expand on error
        return False
    id = len(CHANNELS[channel]['messages'])
    CHANNELS[channel]['messages'].append({id: {"timestamp": datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'), "content": message, "user": user}})
    return True


if __name__ == "__main__":
    # app.run(debug=True, host="0.0.0.0")
    socketio.run(app)
