from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import gbmodel

class Update(MethodView):
	def get(self):
		""" Returns the html file for the update screen """

		return render_template('update.html')

	def post(self):
		""" Grabs the song 'id' inputed by the user in the
		update.html form submission and removes it from the
		songs table in the database. """

		song_id = request.form['id'] # Retrieve the song by id from the form

		model = gbmodel.get_model() # Get the model
		# Call the delete method in model_sqlite3.py:
		model.delete(song_id) # Delete the song from the DB

		return redirect(url_for('index')) # Go back to the index.html page
