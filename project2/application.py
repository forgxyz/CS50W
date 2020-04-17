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

CHANNELS.append({'General': {'id': 0, 'messages': {'content': 'hello there!', 'timestamp': '2020-04-14 16:45:00', 'posted_by': 'jack'}}})
CHANNEL_LIST = {'General': 0}

@app.route("/")
def index():
    return render_template("index.html", list = list(CHANNEL_LIST.keys()))


@app.route("/channels", methods=['GET', 'POST'])
def channels():
    # id will be equal to the list index of the channel
    if request.method == 'POST':
        name = request.form.get("name")
        if name == None:
            return "Error, name = None"
        if name in CHANNEL_LIST.keys():
            # a channel by this name already exists
            return "Error, name already in list"
        id = len(CHANNELS)
        CHANNELS.append({name: {"id": id, "messages": []}})
        CHANNEL_LIST[name] = id
        return "Success. Refresh to see the channel list."
    # GET request: return the channel list
    return jsonify(list(CHANNEL_LIST.keys()))



@app.route("/channel/<name>")
def load_channel(name):
    messages = CHANNELS[CHANNEL_LIST[name]][name]['messages']
    return jsonify(messages)
    

@app.route("/home")
def home():
    return "THIS IS THE HOMEPAGE"


@app.route("/new_post")
def post_message(channel, message, user):
    if channel not in CHANNEL_LIST.values():
        # expand on error
        return False
    id = len(CHANNELS[channel]['messages'])
    CHANNELS[channel]['messages'].append({"id": id, "timestamp": datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'), "content": message, "posted_by": user})
    return True


if __name__ == "__main__":
    # app.run(debug=True, host="0.0.0.0")
    socketio.run(app)
