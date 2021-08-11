import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred

OFFLINE_PLAYLIST_NAME = "Liked Songs Manager"
N_SONGS = 50

scope = "user-library-modify playlist-modify-private user-library-read playlist-modify-public playlist-read-private playlist-read-collaborative"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id, client_secret= cred.client_secret, redirect_uri=cred.redirect_uri, scope=scope))

def create_playlist(playlist_name):
    playlists = sp.current_user_playlists()['items']
    if not any([x['name'] == playlist_name for x in playlists]):
        sp.user_playlist_create(sp.me()['id'], playlist_name)


def get_playlist(playlist_name):
    playlists = sp.current_user_playlists()['items']
    for playlist in playlists:
        if playlist['name'] == OFFLINE_PLAYLIST_NAME:
            return sp.playlist_items(playlist['id'])
    return None


def get_playlist_id(playlist_name):
    playlists = sp.current_user_playlists()['items']
    for playlist in playlists:
        if playlist['name'] == OFFLINE_PLAYLIST_NAME:
            return playlist['id']

    return None

create_playlist(OFFLINE_PLAYLIST_NAME)
manager_playlist = get_playlist(OFFLINE_PLAYLIST_NAME)
liked_songs_playlist = sp.current_user_saved_tracks(limit=N_SONGS)

songs_in_manager_playlist = [x['track']['id'] for x in manager_playlist['items']]
songs_in_liked_playlist = [x['track']['id'] for x in liked_songs_playlist['items']]
manager_playlist_id = get_playlist_id(OFFLINE_PLAYLIST_NAME)
for tid in songs_in_liked_playlist:
    if tid not in songs_in_manager_playlist:
        sp.playlist_add_items(manager_playlist_id, [tid])

for tid in songs_in_manager_playlist:
    if tid not in songs_in_liked_playlist:
        sp.playlist_remove_all_occurrences_of_items(manager_playlist_id, [tid])

