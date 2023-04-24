#!/usr/bin/python3
"""Starts Flask web app listening on 0.0.0.0, port 5000"""
from flask import Flask, render_template
from models import storage


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/hbnb_filters')
def hbnb_filters():
    """display a beautiful HTML with loaded data"""
    states = storage.all("State")
    amenities = storage.all("Amenity")
    return render_template('6-index.html', amenities=amenities, states=states)


@app.teardown_appcontext
def teardown(self):
    """remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
