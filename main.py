import spotipy
from spotipy.oauth2 import SpotifyOAuth
import datetime
import os
from dotenv import load_dotenv
import random

# LOAD FROM .ENV
load_dotenv()

CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

# AUTH CREDENTIALS
scope = "user-library-read user-top-read playlist-modify-public"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope))

# GET TODAY DATE
today = datetime.date.today()

# GET MY 20 TOP TRACKS
top_tracks = sp.current_user_top_tracks(limit=50, time_range="short_term")

# GET RANDOM TRACK FROM TOP TRACKS
random = random.randint(0, 49)
seed_track_id = top_tracks['items'][random]['id']
seed_track_name = top_tracks['items'][random]['name']
seed_track_artist = top_tracks['items'][random]['artists'][0]['name']

# SET RECOMMENDATION PARAMETERS
recommendation_limit = 50
recommendation_seed_tracks = [seed_track_id]
recommendation_min_danceability = 0.5
recommendation_min_energy = 0.5
recommendation_min_popularity = 0

# GET RECOMMENDATIONS
recommendations = sp.recommendations(
    limit=recommendation_limit,
    seed_tracks=recommendation_seed_tracks,
    min_danceability=recommendation_min_danceability,
    min_energy=recommendation_min_energy,
    min_popularity=recommendation_min_popularity
)

# PRINT RECOMMENDATIONS
print(f"Les recommendations pour le {today.day}/{today.month.real}/{today.year} sont :")
for i, track in enumerate(recommendations['tracks']):
    print(f"{i + 1}. {track['name']} by {track['artists'][0]['name']}")

# CREATION OF THE PLAYLIST
playlists = sp.current_user_playlists()
playlist_name = "📡  RECO DU JOUR  📡"
for playlist in playlists["items"]:
    if playlist["name"] == playlist_name:
        playlist_id = playlist["id"]
        break


track_ids = [track['id'] for track in recommendations['tracks']]
# UPDATE PLAYLIST DESCRIPTION
sp.playlist_change_details(
    playlist_id=playlist_id,
    description="Autogénéré par l\'API de Spotify. Playlist créée le " + str(today.day) + "/" + str(today.month.real) + "/" + str(today.year) + "." + " La musique de référence est " + seed_track_name + " de " + seed_track_artist + "."
)

sp.playlist_replace_items(
    playlist_id=playlist_id,
    items=track_ids
)

# DEBUG
print(f"Playlist '{playlist_name}' has been created and updated with {len(track_ids)} tracks.")