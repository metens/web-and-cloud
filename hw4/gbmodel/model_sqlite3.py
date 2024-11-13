from .Model import Model
import sqlite3

DB_FILE = "song_entries.db" # Database file

class model(Model):
	""" model is derived from the Model base class. """

	def __init__(self):
		""" Try to connect to the DB_FILE. 
		If the database doesn't exist, create the table. """

		# Initial connection attempt each time we try accessing the DB file:
		connection = sqlite3.connect(DB_FILE)
		cursor = connection.cursor()	

		try:
			cursor.execute("SELECT COUNT(ROWID) FROM songs")
		except sqlite3.OperationalError: # If the database doesn't exist:
			cursor.execute("""CREATE TABLE songs (
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					title TEXT,
					artist TEXT,
					release DATE,
					url VARCHAR(512)
					);""")

	def select(self):
		""" Retrieve each row from the DB_FILE.
		Each row has  a song id, title, artist, release date,
		and a url where the song can be found on the internet.
		:return: List of lists containing all rows of the database. """

		# Initial connection attempt:
		connection = sqlite3.connect(DB_FILE)
		cursor = connection.cursor()	

		cursor.execute("SELECT * FROM songs;")
		return cursor.fetchall()

	def insert(self, title: str, artist: str, release: str, url: str) -> bool:
		""" Inserts a song into the database. Given the title,
		artist, release date, and the url where the song can be found. """ 

		# Connection attempt:
		connection = sqlite3.connect(DB_FILE)
		cursor = connection.cursor()	

		# The id for each new song entry is autoincremented,
		# so there is no need to add the id to the song entry:
		new_song = {
			'title':title,
			'artist':artist,
			'release':release,
			'url':url}

		cursor.execute("""INSERT INTO songs (title, artist, release, url) 
				VALUES (:title, :artist, :release, :url);""", new_song)
		connection.commit()
		cursor.close()
		return True 

	def delete(self, song_id: int) -> bool:
		""" Takes a song_id and deletes it from the DB_FILE. """

		# Initial database connection attempt:
		connection = sqlite3.connect(DB_FILE);
		cursor = connection.cursor();

		cursor.execute("DELETE FROM songs WHERE id = :song_id;", {'song_id': song_id})
		connection.commit()
		cursor.close()
		return True
