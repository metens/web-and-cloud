from flask import Flask # WSGI (Web Server Gateway Interface)
from model_sqlite3 import model
from index import Index
from sign import Sign

app = Flask(__name__) # an instance of the Flask class is out WSGI app

app.add_url_rule('/', view_func=Index.as_view('index'), methods=['GET'])

app.add_url_rule('/sign', view_func=Sign.as_view('sign'), methods=['GET', 'POST'])

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, debug=True)

