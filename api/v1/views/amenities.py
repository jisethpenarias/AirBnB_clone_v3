#!/usr/bin/python3
""" View State API """

from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage
from models.amenity import Amenity
from models.state import State


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def amenities_all():
    """ Retrieves the list of all amenities objects """
    amenities = storage.all('Amenity')
    list_amenities = []
    for amenity in amenities.values():
        list_amenities.append(amenity.to_dict())
    return jsonify(list_amenities)


@app_views.route('amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenities_id(amenity_id=None):
    """ Retrieve a amenities by Id """
    amenities_id = storage.get('Amenity', amenity_id)
    if amenities_id:
        return jsonify(amenities_id.to_dict())
    abort(404)


@app_views.route('amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenities(amenity_id=None):
    """ Deletes a Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)
    return abort(404)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def post_amenities():
    """ Creates a amenity """
    dict_json = request.get_json()
    if not dict_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in dict_json:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_amenity = Amenity(**dict_json)
    storage.new(new_amenity)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenities(amenity_id=None):
    """ Updates a Amenity object """
    dict_json = request.get_json()
    if not dict_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    amenities_obj = storage.get('Amenity', amenity_id)
    if amenities_obj:
        for key, value in dict_json.items():
            setattr(amenities_obj, key, value)
        storage.save()
        return make_response(jsonify(amenities_obj.to_dict()), 200)
    else:
        return abort(404)
