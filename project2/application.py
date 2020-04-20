import os

from datetime import datetime
from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY") # ???
socketio = SocketIO(app)

# CHANNELS will hold message data in the following structure:
"""{name:
        {messages: [{
            id,
            content,
            timestamp,
            posted_by}]}
    }"""

CHANNELS = {}

# initial channel for testing
CHANNELS['General'] = {'messages': [{'content': 'hello there!', 'timestamp': '2020-04-14 16:45:00', 'posted_by': 'jack'}, {'content': 'need some coffee', 'timestamp': '2020-04-20 12:24:00', 'posted_by': 'jack'}]}


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
            return "Error, channel must have a name"
        if name in CHANNELS.keys():
            # a channel by this name already exists
            return "Error, channel already exists"
        CHANNELS[name] = {'messages': []}
        return "Success."
    # GET request: return the channel list
    return jsonify(list(CHANNELS.keys()))


@app.route('/channels/<channel>', methods=['GET', 'POST'])
def load_channel(channel):
    return jsonify(CHANNELS[channel]['messages'])

@app.route("/home")
def home():
    return "Welcome. Please select a channel from above or create a new one."


# SOCKETS
@socketio.on('post message')
def post_message(data):
    channel = data['data']['channel']
    message = {'content': data['data']['content'], 'timestamp': str(datetime.now()), 'posted_by': data['data']['user']}

    # add message to server storage
    CHANNELS[channel]['messages'].append(message)

    emit('new message', {'message': message, 'channel': channel}, broadcast=True)


if __name__ == "__main__":
    socketio.run(app)
