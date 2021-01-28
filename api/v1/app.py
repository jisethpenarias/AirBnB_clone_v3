#!/usr/bin/python3
""" Status api """

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(self):
    """ Remove the current SQLAlchemy Session """
    storage.close()

if __name__ == '__main__':
    port = getenv("HBNB_API_PORT") or 5000
    host = getenv("HBNB_API_HOST") or '0.0.0.0'
    app.run(host=host, port=port, threaded=True)
