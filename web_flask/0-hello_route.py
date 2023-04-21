#!/usr/bin/python3
from flask import Flask
"""Starts Flask web app"""


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello_world():
    """route to print out a text"""
    return 'Hello HBNB!'


if __name__ == '__main__':
    app.run(debug=True, port=5000)
