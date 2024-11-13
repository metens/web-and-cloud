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
        self.client = datastore.Client('songs-441606')

    def select(self) -> list:
        """Fetches all reviews from Datastore.
        
        Returns: A list of reviews, where each review is a list of title, artist, release, and url.
        """
        """
        Fetches all reviews from Datastore.

        Returns:
            A list of reviews, where each review is a list of title, artist, release, and url.
        
        query = self.client.query(kind='Review')
        entities = list(map(from_datastore, query.fetch()))
        return entities
        """
        query = self.client.query(kind='Review')
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
        """Inserts a new review into Datastore.

        Args:
            title: The title of the song.
            artist: The artist of the song.
            release: The release date of the song.
            url: The URL of the song.

        Returns:
            True if the insertion is successful, False otherwise.
        """
        try:
            key = self.client.key('Review')
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
"""
from .Model import Model
from google.cloud import datastore

def from_datastore(entity):
    if not entity:
        return None
    if isinstance(entity, list):
        entity = entity.pop()

    return [entity['title'],entity['artist'],entity['release'],entity['url']]

class model(Model):
    def __init__(self):
        self.client = datastore.Client('songs-441606')

    def select(self):
        query = self.client.query(kind = 'Review')
        entities = list(map(from_datastore,query.fetch()))
        return entities

    def insert(self,name,email,message):
        key = self.client.key('Review')
        rev = datastore.Entity(key)
        rev.update( {
            'title': title,
            'artist' : artist,
            'release' : release,
            'url' : url 
            })
        self.client.put(rev)
        return True
"""
def insert_sample_data():
    client = datastore.Client('songs-441606')  # I made a new project for hw4

    # Example data to insert
    song_data = [
        {'title': 'Song 1', 'artist': 'Artist 1', 'release': '2024-01-01', 'url': 'http://example.com/1'},
        {'title': 'Song 2', 'artist': 'Artist 2', 'release': '2024-02-01', 'url': 'http://example.com/2'},
        {'title': 'Song 3', 'artist': 'Artist 3', 'release': '2024-03-01', 'url': 'http://example.com/3'},
    ]
    
    for data in song_data:
        key = client.key('Review')  # Assuming your entity kind is 'Review'
        entity = datastore.Entity(key)
        entity.update(data)
        client.put(entity)

    print("Sample data inserted into Datastore.")

# Call this function to insert the data
#insert_sample_data()
