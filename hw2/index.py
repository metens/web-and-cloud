from flask import render_template
from flask.views import MethodView
import gbmodel

class Index(MethodView):
    def get(self):
        model = gbmodel.get_model()
        entries = [dict(song_title=row[0], 
                        artist=row[1],
                        release_date=row[2],
                        song_url=row[3],)
                        for row in model.select()]
        return render_template('index.html', entries=entries)