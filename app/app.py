from flask import *
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)



@app.route('/sanity', methods=['GET'])
def sanity():
	return "This is a sanity check!"


@app.route('/index.html', methods=['GET'])
def index_exp():
	return send_file('index.html')


@app.route('/', methods=['GET'])
def index():
	return send_file('index.html')

if __name__ == "__main__":
	app.run()
