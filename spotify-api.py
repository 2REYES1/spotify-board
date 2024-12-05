from flask import Flask, request, redirect, session, url_for, jsonify, send_from_directory
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Secret key for sessions (use a secure key in production)
app.secret_key = os.urandom(24)
app.config['SESSION_COOKIE_NAME'] = 'spotify-session'

# Get Spotify credentials from environment variables
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

# Spotify OAuth configuration
sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-top-read"
)

@app.route('/')
def index():
    # Redirect to login page to authenticate with Spotify
    return redirect(url_for('login'))

@app.route('/login')
def login():
    # Get Spotify authentication URL and redirect user to login
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    # Handle the callback from Spotify's OAuth
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('main_page'))

@app.route('/main-page')
def main_page():
    # Serve the main HTML page
    return send_from_directory('frontend', 'main-page.html')

@app.route('/api/top-tracks')
def top_tracks():
    # Fetch the top tracks for the authenticated user
    token_info = session.get('token_info', None)
    if not token_info:
        return jsonify({"error": "Not authenticated"}), 401

    # Use the Spotify API to get the top tracks
    sp = Spotify(auth=token_info['access_token'])
    results = sp.current_user_top_tracks(limit=10, time_range='short_term')

    # Format the top tracks into a response
    top_tracks = [
        {
            'name': track['name'],
            'artist': ', '.join(artist['name'] for artist in track['artists']),
            'url': track['external_urls']['spotify']
        }
        for track in results['items']
    ]
    return jsonify(top_tracks)

@app.route('/static/<path:filename>')
def serve_static(filename):
    # Serve static files from the 'frontend' directory
    return send_from_directory('frontend', filename)

if __name__ == '__main__':
    app.run(debug=True)
