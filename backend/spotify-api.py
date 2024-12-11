import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, jsonify
from flask_cors import CORS  

app = Flask(__name__)


CORS(app) # allows the html port to connect to the server port locally

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri=SPOTIFY_REDIRECT_URI,
                                               scope='user-top-read'))

@app.route('/top-tracks')
def top_tracks():
    results = sp.current_user_top_tracks(limit=10, time_range="short_term")
    
    tracks = []
    for track in results['items']:
        track_info = {
            'name': track['name'],
            'album': track['album']['name'],
            'album_image': track['album']['images'][0]['url'],
            'artists': [artist['name'] for artist in track['artists']]
        }
        tracks.append(track_info)
    
    return jsonify(tracks=tracks)


if __name__ == '__main__':
    app.run(debug=True)
