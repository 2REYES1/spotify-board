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
    # Fetch the user's top 10 tracks
    results = sp.current_user_top_tracks(limit=10)
    tracks = [{'name': track['name']} for track in results['items']]  
    return jsonify(tracks=tracks)

if __name__ == '__main__':
    app.run(debug=True)
