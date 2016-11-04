#-----------------
# init application
#-----------------

import flask
#from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

import os

template_dir = '/var/www/cs373-idb/app/static/templates'
app = flask.Flask(__name__.split('.')[0])
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///musicdb'



db = SQLAlchemy(app)

#import app
