from Model import Model, sqlite3

DB_FILE = "song_entries.db" # database file

class model(Model):
    def __init__(self):
        """
        Try to connect to the DB_FILE.
        If the database doesn't exist,
        create the table.
        """ 
        try:
            self.cursor.execute("SELECT COUNT(ROWID) FROM songs")
        except sqlite3.OperationalError:
            self.cursor.execute("""CREATE TABLE songs (song_title text, 
                           artist text, release_year date, song_url text""")
    
    def select(self):
        """
        Retrieve each row from the DB_FILE.
        """
        self.cursor.execute("SELECT * FROM songs")
        return self.cursor.fetchall()
    
    def insert(self, title, artist, release, url):
        """
        Inserts a song into the database.
        """ 
        new_song = {'title':title,
                    'arist':artist,
                    'release':release,
                    'url':url}
        self.cursor.execute("""INSERT INTO songs (title, artist, release, url) 
                       VALUES (:title, artist, release, url)""", new_song)
        self.connection.commit()
        self.cursor.close()
        return True 