from flask import Flask, render_template, request, redirect, url_for
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
SPOTIPY_CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]
SPOTIPY_REDIRECT_URI = 'http://localhost:5000/callback'
SCOPE = "user-read-playback-state,user-modify-playback-state"

@app.route('/play', methods=['POST'])
def play_song():
    song_name = request.form['song_name']

    # Get access token
    sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=SCOPE)
    access_token = sp_oauth.get_access_token(as_dict=False)

    # Create Spotify client
    sp = Spotify(auth=access_token)

    # Search for the song
    results = sp.search(q=song_name, limit=1, type='track')

    if results['tracks']['items']:
        track_uri = results['tracks']['items'][0]['uri']

        # Play the song
        sp.start_playback(uris=[track_uri])

    return "playing song"

if __name__ == '__main__':
    app.run(debug=True)