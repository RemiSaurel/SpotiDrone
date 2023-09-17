import datetime
import random
import argparse
from client import create_spotify_object

# CONSTANTS
PLAYLIST_NAME = "📡  RECO DU JOUR  📡"
SP = create_spotify_object()
TODAY = datetime.date.today()


def getTopTracks(number_of_tracks, time_range):
    """
    Get the top tracks of the user
    :param number_of_tracks:
    :param time_range: short_term | medium_term | long_term
    :return: the top tracks of the user
    """
    return SP.current_user_top_tracks(limit=number_of_tracks, time_range=time_range)


def setRecommendation(limit, seed_track_id, min_danceability, min_energy, min_popularity):
    """
    Set the recommendations
    :param limit:
    :param seed_track_id:
    :param min_danceability:
    :param min_energy:
    :param min_popularity:
    :return: the recommendations
    """
    recommendation_limit = limit
    recommendation_seed_tracks = [seed_track_id]
    recommendation_min_danceability = min_danceability
    recommendation_min_energy = min_energy
    recommendation_min_popularity = min_popularity

    # GET RECOMMENDATIONS
    return SP.recommendations(
        limit=recommendation_limit,
        seed_tracks=recommendation_seed_tracks,
        min_danceability=recommendation_min_danceability,
        min_energy=recommendation_min_energy,
        min_popularity=recommendation_min_popularity
    )


def getNbTracksArgs():
    """
    Get the number of tracks from the args
    :return: the number of tracks
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", type=int, help="Number of tracks on the playlist")
    args = parser.parse_args()
    return args.number


def getPlaylistId():
    """
    Get the playlistId from existing playlist or create a new one if it doesn't exist
    :return:
    """
    playlists = SP.current_user_playlists()
    for playlist in playlists["items"]:
        if playlist["name"] == PLAYLIST_NAME:
            return playlist["id"]
    return SP.user_playlist_create(user=SP.me()['id'], name=PLAYLIST_NAME, public=True)["id"]


NB_TRACKS = getNbTracksArgs()
# GET MY TOP TRACKS
top_tracks = getTopTracks(NB_TRACKS, "short_term")

# GET RANDOM TRACK FROM TOP TRACKS
random = random.randint(0, NB_TRACKS - 1)
seed_track_id = top_tracks['items'][random]['id']
seed_track_name = top_tracks['items'][random]['name']
seed_track_artist = top_tracks['items'][random]['artists'][0]['name']

# SET RECOMMENDATIONS
recommendations = setRecommendation(NB_TRACKS, seed_track_id, 0.5, 0.5, 0)

# PRINT RECOMMENDATIONS
print(f"Les recommendations pour le {TODAY.day}/{TODAY.month.real}/{TODAY.year} sont :")
for i, track in enumerate(recommendations['tracks']):
    print(f"{i + 1}. {track['name']} by {track['artists'][0]['name']}")

# GET PLAYLIST
playlist_id = getPlaylistId()

track_ids = [track['id'] for track in recommendations['tracks']]
# UPDATE PLAYLIST DESCRIPTION
SP.playlist_change_details(
    playlist_id=playlist_id,
    description="Autogénéré par l\'API de Spotify. Playlist créée le " + str(TODAY.day) + "/" + str(
        TODAY.month.real) + "/" + str(
        TODAY.year) + "." + " La musique de référence est " + seed_track_name + " de " + seed_track_artist + "."
)

SP.playlist_replace_items(
    playlist_id=playlist_id,
    items=track_ids
)

# DEBUG
print(f"Playlist '{PLAYLIST_NAME}' has been created and updated with {len(track_ids)} tracks.")
