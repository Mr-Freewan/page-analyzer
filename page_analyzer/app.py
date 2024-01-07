from flask import Flask

from cfg import SECRET_KEY

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY


@app.route("/")
def start_page():
    return "<p>Project started!</p>"
