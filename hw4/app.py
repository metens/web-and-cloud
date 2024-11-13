from flask import Flask # WSGI (Web Server Gateway Interface)
#from gbmodel.model_sqlite3 import model
from gbmodel.model_datastore import model
from index import Index 
from sign import Sign
from update import Update

app = Flask(__name__) # An instance of the Flask class

# The homepage that shows all entries on index.html:
app.add_url_rule('/', view_func=Index.as_view('index'), methods=['GET'])

# The sign page that has the form (sign.html):
app.add_url_rule('/sign', view_func=Sign.as_view('sign'), methods=['GET', 'POST'])

# The update page that can remove song entries:
app.add_url_rule('/update', view_func=Update.as_view('update'), methods=['GET', 'POST'])

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, debug=True) # Port 5000 was already in use on my PC

