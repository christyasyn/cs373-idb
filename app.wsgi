#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/cs373-idb/")

from app.app import app
app.secret_key = 'Add your secret key'