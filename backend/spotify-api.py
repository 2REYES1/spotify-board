from flask import Flask, request, redirect, session, url_for
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24) 
app.config['SESSION_COOKIE_NAME'] = 'spotify-session'

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')


sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-top-read"
)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('top_tracks'))

@app.route('/top-tracks')
def top_tracks():
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('login'))

    sp = Spotify(auth=token_info['access_token'])
    results = sp.current_user_top_tracks(limit=10)
    top_tracks = [
        {
            'name': track['name'],
            'artist': ', '.join(artist['name'] for artist in track['artists']),
            'url': track['external_urls']['spotify']
        }
        for track in results['items']
    ]

    html = "<h1>User's Top 10 Tracks</h1><ul>"
    for num, track in enumerate(top_tracks, start=1):
        html += f"<li>{num}. <a href='{track['url']}'>{track['name']}</a> by {track['artist']}</li>"
    html += "</ul>"

    return html

if __name__ == '__main__':
    app.run(debug=True)
