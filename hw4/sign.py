from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import gbmodel

class Sign(MethodView):
	def get(self):
		""" Display the sign.html page. """

		return render_template('sign.html')

	def post(self):
		""" Catches all the inserted values in the form 
		on sign.html and passes it to the model_sqlite3.py
		method 'insert' to be inserted into the songs table. """

		model = gbmodel.get_model()
		model.insert(	request.form['title'],
				request.form['artist'],
				request.form['release'],
				request.form['url'])

		return redirect(url_for('index'))
