#-----------------
# init application
#-----------------

from flask import Flask 
from flask.ext.sqlalchemy import sqlalchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/musicdb'

db = SQLAlchemy(app)

import app