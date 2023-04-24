#!/usr/bin/python3
"""Starts Flask web app listening on 0.0.0.0, port 5000"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/states')
def show_states():
    """ display states in HTML page"""
    states = storage.all(State)
    return render_template('9-states.html', states=states, search="all")


@app.route('/states/<id>')
def show_cities_of_state(id):
    """ display states in HTML page"""
    states = storage.all(State)
    for state in states.values():
        if state.id == id:
            return render_template('9-states.html', states=state, search="one")
    return render_template('9-states.html', states=state, search="nothing")


@app.teardown_appcontext
def teardown(self):
    """remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
