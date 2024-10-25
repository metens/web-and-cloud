from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import gbmodel

class Update(MethodView):
	def get(self):
		return render_template('update.html')

	def post(self):
		# Delete a song in the database by its id:
		song_id = request.form['id'] # Retrieve the song by id

		model = gbmodel.get_model() # Get the model
		model.delete(song_id) # Delete the song from the DB calls model_sqlit3 method!
		return redirect(url_for('index'))
