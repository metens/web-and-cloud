from .Model import Model
import sqlite3

DB_FILE = "song_entries.db" # database file

class model(Model):
    def __init__(self):
        """
        Try to connect to the DB_FILE.
        If the database doesn't exist,
        create the table.
        """ 
	# Initial connection attempt each time we try accessing the DB file
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()	

        try:
            cursor.execute("SELECT COUNT(ROWID) FROM songs")
        except sqlite3.OperationalError:
            cursor.execute("""CREATE TABLE songs (title text, 
                           artist text, release date, url text)""")
    
    def select(self):
        """
        Retrieve each row from the DB_FILE.
        """
	# Initial connection attempt:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()	

        cursor.execute("SELECT * FROM songs")
        return cursor.fetchall()
    
    def insert(self, title, artist, release, url):
        """
        Inserts a song into the database.
        """ 
	# Connection attempt:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()	

        new_song = {'title':title,
                    'artist':artist,
                    'release':release,
                    'url':url}

        cursor.execute("""INSERT INTO songs (title, artist, release, url) 
                       VALUES (:title, :artist, :release, :url)""", new_song)
        connection.commit()
        cursor.close()
        return True 
