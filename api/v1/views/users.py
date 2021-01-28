#!/usr/bin/python3
""" View User API """

from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def users_all():
    """ Retrieves the list of all Users objects """
    users = storage.all('User')
    list_users = []
    for user in users.values():
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_id(user_id=None):
    """ Retrieve a User by Id """
    user_id = storage.get('User', user_id)
    if user_id:
        return jsonify(user_id.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user():
    """ Deletes a User object """
    user_obj = storage.get('User', user_id)
    if user_obj:
        storage.delete(user_obj)
        storage.save()
        return make_response(jsonify({}), 200)
    return abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """ Create User object """
    json_dict = request.get_json()
    if not json_dict:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in json_dict:
        return make_response(jsonify({'error': 'Missing email'}), 400)
    elif 'password' not in json_dict:
        return make_response(jsonify({'error': 'Missing password'}), 400)
    new_user = User(**json_dict)
    storage.new(new_user)
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id=None):
    """ Updates a User object """
    dict_json = request.get_json()
    if not dict_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    user_obj = storage.get('User', user_id)
    if user_obj:
        for key, value in dict_json.items():
            setattr(user_obj, key, value)
        storage.save()
        return make_response(jsonify(user_obj.to_dict()), 200)
    else:
        return abort(404)
