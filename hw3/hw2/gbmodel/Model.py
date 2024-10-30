class Model():
	def select(self):
	       	""" Gets all entries from the database.
		:return: Tuple containing all rows of database. """
        	pass

	def insert(self):
		""" Inserts song into database:
		:param id: INTEGER
		:param title: String
		:param artist: String
		:param release: String
		:param url: String
		:return: none
		:raises: Database errors on connection and insertion. """
		pass

	def delete(self):
		""" Removes a song in the database by its
		song id parameter. """
		pass
