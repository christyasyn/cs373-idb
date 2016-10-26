#-----------------
# init application
#-----------------

from flask import Flask 
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///musicdb'

db = SQLAlchemy(app)

#import app
