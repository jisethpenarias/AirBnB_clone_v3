#!/usr/bin/python3
""" View State API """

from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage
from models.city import City
from models.state import State


@app_views.route('states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_all(state_id=None):
    """ Retrieves the list of all City objects """
    states_id = storage.get('State', state_id)
    list_cities = []
    if states_id:
        for city in states_id.cities:
            list_cities.append(city.to_dict())
        return jsonify(list_cities)
    else:
        abort(404)


@app_views.route('cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def cities(city_id=None):
    """ Retrieves the list of all City objects """
    cities_id = storage.get('City', city_id)
    if cities_id:
        return jsonify(cities_id.to_dict())
    abort(404)


@app_views.route('cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id=None):
    """ Deletes a city object """
    city = storage.get('City', city_id)
    if city:
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)
    return abort(404)


@app_views.route('states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_cities(state_id=None):
    """ Creates a city """
    states = storage.get('State', state_id)
    if not states:
        abort(404)
    dict_json = request.get_json()
    if not dict_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in dict_json:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_city = City(**dict_json)
    storage.new(new_city)
    new_city.state_id = state_id
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_cities(city_id=None):
    """ Updates a city object """
    dict_json = request.get_json()
    if not dict_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    cities_obj = storage.get('City', city_id)
    if cities_obj:
        for key, value in dict_json.items():
            setattr(cities_obj, key, value)
        storage.save()
        return make_response(jsonify(cities_obj.to_dict()), 200)
    else:
        return abort(404)
