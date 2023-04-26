#!/usr/bin/python3
"""Starts Flask web app listening on 0.0.0.0, port 5000"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/hbnb_filters')
def filters():
    """ display filtered states in HTML page"""
    states = storage.all(State)
    amenities = storage.all(Amenity)
    return render_template('6-index.html', states=states, amenities=amenities)


@app.teardown_appcontext
def teardown(self):
    """remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
