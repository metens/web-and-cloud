import flask
import gbmodel

class Sign(flask.views.MethodView):
    def get(self):
        return flask.render_template('sign.html')
    
    def post(self):
        model = gbmodel.get_model()
        model.insert(flask.request.form['title'],
                     flask.request.form['artist'],
                     flask.request.form['release'],
                     flask.request.form['url'])
        return flask.redirect(flask.url_for('index'))