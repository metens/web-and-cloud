from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import gbmodel

class Sign(MethodView):
    def get(self):
        return render_template('sign.html')
    
    def post(self):
        model = gbmodel.get_model()
        model.insert(request.form['title'],
                     request.form['artist'],
                     request.form['release'],
                     request.form['url'])
        return redirect(url_for('index'))
