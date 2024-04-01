from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()


SPOTIPY_CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]
SPOTIPY_REDIRECT_URI = os.environ["SPOTIPY_REDIRECT_URI"]
SCOPE = "user-read-playback-state,user-modify-playback-state"


def play_song(song_name):
    print(song_name)
    # Get access token
    sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=SCOPE)
    access_token = sp_oauth.get_access_token(as_dict=False)
    print(access_token)

    # Create Spotify client
    sp = Spotify(auth=access_token)

    # Search for the song
    results = sp.search(q=song_name, limit=1, type='track')

    if results['tracks']['items']:
        track_uri = results['tracks']['items'][0]['uri']

        # Play the song
        sp.start_playback(uris=[track_uri])

    return "Your song is being played!"
