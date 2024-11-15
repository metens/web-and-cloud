# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from .Model import Model
from google.cloud import datastore

def from_datastore(entity):
    """Translates Datastore results into the format expected by the application.

    Args:
        entity: The Datastore entity to translate.

    Returns:
        A list containing the entity's title, artist, release, and url.
    """
    if not entity:
        return None
    if isinstance(entity, list):
        entity = entity.pop()

    return [entity.get('title'), entity.get('artist'), entity.get('release'), entity.get('url')]
   
class model(Model):
    def __init__(self):
        """Initializes the Datastore client."""
        self.client = datastore.Client('songs-441606') # My new project-ID for hw4

    def select(self) -> list:
        """
        Fetches all songs from Datastore.

        Returns:
            A list of songs, where each song is a list of title, artist, release, and url.
        """
        query = self.client.query(kind='Song') # Song is the kind of data in google-cloud datastore
        entities = list(query.fetch())

        # Convert entities to a list of lists
        reviews = []
        for entity in entities:
            # Assuming entity is a dictionary with keys 'title', 'artist', 'release', 'url'
            reviews.append([
                entity.key.id,      # ID is usually stored in entity.key.id
                entity.get('title', ''),
                entity.get('artist', ''),
                entity.get('release', ''),
                entity.get('url', '')
            ])
        return reviews

    def insert(self, title: str, artist: str, release, url: str) -> bool:
        """Inserts a new song into Datastore.

        Args:
            title: The title of the song.
            artist: The artist of the song.
            release: The release date of the song.
            url: The URL of the song.

        Returns:
            True if the insertion is successful, False otherwise.
        """
        try:
            key = self.client.key('Song')
            rev = datastore.Entity(key)
            rev.update({
                'title': title,
                'artist': artist,
                'release': release,
                'url': url
            })
            self.client.put(rev)
            return True

        except Exception as e:
            print(f"Error inserting entity: {e}")
            return False

    def delete(self, song_id: str) -> bool:
        """Deletes a song from Datastore by its ID.

        Args:
            song_id: The ID of the song to be deleted.

        Returns:
            True if the deletion is successful, False if the song was not found.
        """
        try:
            # If song_id is an integer, use the integer type
            if song_id.isdigit():
                key = self.client.key('Song', int(song_id))  # Use integer key for numeric IDs
            else:
                key = self.client.key('Song', song_id)  # Use string key for non-numeric IDs
            
            song = self.client.get(key)

            if song:
                # If the song exists, delete it
                self.client.delete(key)
                return True
            else:
                # If the song doesn't exist, return False
                return False

        except Exception as e:
            # Log any exceptions that occur
            print(f"Error deleting song with ID {song_id}: {e}");
            return False
