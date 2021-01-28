#!/usr/bin/python3
""" View State API """

from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def states_all():
    """ Returns a JSON: all states """
    states = storage.all('State')
    list_states = []
    for state in states.values():
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def states_id():
    """ Returns a JSON: states with id """
    
