import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, jsonify, request
from flask_cors import CORS  
from dotenv import load_dotenv
load_dotenv()  

app = Flask(__name__)


CORS(app) 

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

ratings = {}
@app.route('/rate', methods=['POST'])
def rate():
    data = request.json
    track_name = data['track_name']
    rating = data['rating']
    ratings[track_name] = rating
    print(ratings)
    return jsonify({"message": "Rating saved!", "ratings": ratings})


@app.route('/get-rating', methods=['GET'])
def get_rating():
    track_name = request.args.get('track_name')
    rating = ratings.get(track_name, None)
    return jsonify({"rating": rating})



if __name__ == '__main__':
    app.run(debug=True)