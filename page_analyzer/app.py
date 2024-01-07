from flask import Flask

app = Flask(__name__)


@app.route("/")
def start_page():
    return "<p>Project started!</p>"
