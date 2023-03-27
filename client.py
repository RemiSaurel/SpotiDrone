# LOAD FROM .ENV
import os

import spotipy
from dotenv import load_dotenv
from spotipy import SpotifyOAuth

load_dotenv()

CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

# AUTH CREDENTIALS
scope = "user-library-read user-top-read playlist-modify-public"


def create_spotify_object():
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI,
                                  scope=scope))
