#!/usr/bin/python3
""" Status api """

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def status_route():
    """ Returns a JSON: "status": "OK" """
    return jsonify({"status": "OK"})
