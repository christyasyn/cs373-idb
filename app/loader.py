#-----------------
# init application
#-----------------

import flask
from flask_sqlalchemy import SQLAlchemy
from flask_cache import Cache

import os

template_dir = '/var/www/cs373-idb/app/static/templates'
app = flask.Flask(__name__.split('.')[0])
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///musicdb'

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

db = SQLAlchemy(app)
