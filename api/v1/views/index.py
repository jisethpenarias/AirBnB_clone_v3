#!/usr/bin/python3
""" Status api """

from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def status_route():
    """ Returns a JSON: "status": "OK" """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def stats_route():
    """ Retrieves the number of each objects """
    if request.method == 'GET':
        number_objects = {
            'amenities': storage.count('Amenity'),
            'cities': storage.count('City'),
            'places': storage.count('Place'),
            'reviews': storage.count('Review'),
            'states': storage.count('State'),
            'users': storage.count('User')
        }
        return jsonify(number_objects)
