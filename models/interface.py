class DatabaseInterface(object):
	MODELS_PATH="models"
	def __init__(self, model_name, connection_string=None):
		self.models = self.get_model(model_name)
		self.engine = self.models.DataBase(connection_string)
		
	def get_model(self, model_name):
		database_name = ".".join([self.MODELS_PATH, model_name])
		database_module = __import__(database_name, globals(), locals(), [])
		return getattr(database_module, model_name)
