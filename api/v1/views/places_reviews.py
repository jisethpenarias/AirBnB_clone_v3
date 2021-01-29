#!/usr/bin/python3
""" View State API """

from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews_all(place_id=None):
    """ Retrieves the list of all Review objects """
    places_id = storage.get('Place', place_id)
    list_reviews = []
    if places_id:
        for review in places_id.reviews:
            list_reviews.append(review.to_dict())
        return jsonify(list_reviews)
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def reviews_id(review_id=None):
    """ Retrieves the list of all review objects """
    reviews_id = storage.get('Review', review_id)
    if reviews_id:
        return jsonify(reviews_id.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id=None):
    """ Deletes a Review object """
    review = storage.get('Review', review_id)
    if review:
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)
    return abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_reviews(place_id=None):
    """Create place object"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    if 'text' not in request.get_json():
        return make_response(jsonify({'error': 'Missing text'}), 400)
    dict_body = request.get_json()
    place_objs = storage.get(Place, place_id)
    user_objs = storage.get(User, dict_body["user_id"])
    if place_objs and user_objs:
        new_review = Review(**dict_body)
        new_review.place_id = place_objs.id
        storage.new(new_review)
        storage.save()
        return make_response(jsonify(new_review.to_dict()), 201)
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_reviews(review_id=None):
    """ Updates a Review object """
    dict_json = request.get_json()
    if not dict_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    reviews_obj = storage.get('Review', review_id)
    list_ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    if reviews_obj:
        for key, value in dict_json.items():
            if key not in list_ignore:
                setattr(reviews_obj, key, value)
        storage.save()
        return make_response(jsonify(reviews_obj.to_dict()), 200)
    else:
        return abort(404)
