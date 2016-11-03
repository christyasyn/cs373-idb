#-----------------
# init application
#-----------------

from flask import Flask 
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import cache
import os

template_dir = '/var/www/cs373-idb/app/static/templates'
app = Flask(__name__.split('.')[0])
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///musicdb'
app.config['CACHE_TYPE'] = 'simple'
app.cache = Cache(app)

db = SQLAlchemy(app)

#import app
