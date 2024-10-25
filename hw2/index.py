from flask import render_template
from flask.views import MethodView
import gbmodel

class Index(MethodView):
    def get(self):
        model = gbmodel.get_model()
        songs = [dict(
			id=row[0],
			title=row[1], 
                        artist=row[2],
                        release=row[3],
                        url=row[4],) for row in model.select()]
        return render_template('index.html', entries=songs)
