
#model_backend = "sqlite3"
model_backend = "datastore"

if model_backend == "sqlite3":
    from .model_sqlite3 import model
elif model_backend == "datastore":
    from .model_datastore import model


def get_model():
	""" Return the model_sqlite3.py class model. """
	return model()
