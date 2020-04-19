import os

from datetime import datetime
from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY") # ???
socketio = SocketIO(app)

# CHANNELS will hold message data in the following structure:
"""[{name:
        {id,
        messages: [{
            id,
            content,
            timestamp,
            posted_by}]
    }
    }]"""

CHANNELS = []
# CHANNEL_LIST will be a "table of contents" that maps name: id
CHANNEL_LIST = {}

# initial channel for testing
CHANNELS.append({'General': {'id': 0, 'messages': [{'content': 'hello there!', 'timestamp': '2020-04-14 16:45:00', 'posted_by': 'jack'}]}})
CHANNEL_LIST = {'General': 0}


# ROUTES
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/channels", methods=['GET', 'POST'])
def channels():
    # id will be equal to the list index of the channel
    if request.method == 'POST':
        # create the channel
        name = request.form.get("name")
        if name == None or name == '':
            return "Error, name = None"
        if name in CHANNEL_LIST.keys():
            # a channel by this name already exists
            return "Error, name already in list"
        id = len(CHANNELS)
        CHANNELS.append({name: {"id": id, "messages": []}})
        CHANNEL_LIST[name] = id
        return "Success."
    # GET request: return the channel list
    return jsonify(list(CHANNEL_LIST.keys()))


@app.route("/home")
def home():
    return "Welcome. Please select a channel from above or create a new one."


# SOCKETS
@socketio.on('load_messages')
def load_messages(channel):
    emit('messages', CHANNELS[channel]['messages'][0]['content'])


# @socketio.on('post_message')
# def post_message(message):



if __name__ == "__main__":
    socketio.run(app)
