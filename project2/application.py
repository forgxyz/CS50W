import os

from flask import Flask, redirect, render_template, request, url_for
from flask_socketio import SocketIO, emit


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY") # ???
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home")
def home():
    return "THIS IS THE HOMEPAGE"


@app.route("/set_name", methods=['GET', 'POST'])
def set_name():
    return f"""
            <div class="container">
              <form onsubmit="disp_name(); return false;">
                <div class="form-group">
                  <label for="displayname">What should we call you?</label>
                  <input type="text" class="form-control" id="displayname" aria-describedby="Display name">
                </div>
                <button type="submit" class="btn btn-primary">Submit</button>
              </form>
            </div>
    """


@app.route("/test")
def test():
    return "TESTING ROUTE"

if __name__ == "__main__":
    # app.run(debug=True, host="0.0.0.0")
    socketio.run(app)
