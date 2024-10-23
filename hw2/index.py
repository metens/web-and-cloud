from flask import render_template
from flask.views import MethodView
import gbmodel

class Index(MethodView):
    def get(self):
        model = gbmodel.get_model()
        entries = [dict(title=row[0], 
                        artist=row[1],
                        release=row[2],
                        url=row[3],)
                        for row in model.select()]
        return render_template('index.html', entries=entries)
