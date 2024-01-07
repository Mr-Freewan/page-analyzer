from flask import Flask, render_template

from page_analyzer.cfg import SECRET_KEY

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/")
def start_page():
    return render_template('index.html')


@app.post("/urls")
def verify_url():
    return '<h1>Method not allowed!<h1>', 405
