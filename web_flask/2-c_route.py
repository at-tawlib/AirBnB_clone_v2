#!/usr/bin/python3
"""Starts Flask web app listening on 0.0.0.0, port 5000"""
from flask import Flask


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello():
    """route to print out a text"""
    return 'Hello HBNB!'


@app.route('/hbnb')
def hbnb():
    """displays HBNB"""
    return "HBNB"


@app.route("/c/<text>")
def c_text(text):
    """Displays "C" followed by the value of text"""
    return "C {}".format(text.replace("_", " "))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
