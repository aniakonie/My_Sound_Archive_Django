import urllib.parse

import requests


def get_spotify_data(access_token, spotify_id):

    spotify_playlists = get_spotify_playlists(access_token)
    print("playlists retrieved")
    spotify_saved_tracks = get_spotify_saved_tracks(access_token)
    print("saved tracks retrieved")
    spotify_all_playlists_tracks = get_spotify_all_playlists_tracks(
        access_token,
        spotify_id
        )
    print("playlists tracks retrieved")
    return spotify_playlists, spotify_saved_tracks, spotify_all_playlists_tracks


def get_spotify_saved_tracks(access_token):
    '''adding batches of retrieved 50 songs to make a whole list of songs'''

    spotify_saved_tracks = get_spotify_response_all_items(
        spotify_req_get_users_saved_tracks, access_token
        )
    return spotify_saved_tracks


def get_spotify_all_playlists_tracks(access_token, spotify_id):
    '''adding songs from all playlists'''

    spotify_playlists = get_spotify_playlists(access_token)
    spotify_playlists_ids = get_spotify_playlists_ids(
        spotify_playlists,
        spotify_id
        )
    spotify_all_playlists_tracks = {}

    # adding songs of each playlist to a dictionary:
    # key = playlist_id, value: list of songs
    for playlist_id in spotify_playlists_ids:
        spotify_playlist_tracks = get_spotify_playlist_songs_one_playlist(
            access_token,
            playlist_id
            )
        spotify_all_playlists_tracks[playlist_id] = spotify_playlist_tracks
    return spotify_all_playlists_tracks


def get_spotify_playlists(access_token):
    '''adding batches of retrieved 50 playlists data
    to make a whole list of playlists data
    '''

    spotify_playlists = get_spotify_response_all_items(
        spotify_req_get_users_playlists,
        access_token
        )
    return spotify_playlists


def get_spotify_playlist_songs_one_playlist(access_token, playlist_id):
    '''adding batches of retrieved 50 songs from spotify's particular playlist
    to make a whole list of one playlist's songs
    '''

    spotify_playlist_tracks = []
    offset = 0
    while True:
        spotify_playlist_items_response, status_code = spotify_req_get_playlist_items(
            access_token,
            offset,
            playlist_id
        )
        print(status_code)
        spotify_playlist_items_50items = spotify_playlist_items_response['items']
        if len(spotify_playlist_items_50items) == 0:
            break
        spotify_playlist_tracks.extend(spotify_playlist_items_50items)
        offset += 50
    return spotify_playlist_tracks


def get_spotify_playlists_ids(spotify_playlists, spotify_id):

    spotify_playlists_ids = set()
    for playlist in spotify_playlists:
        if playlist["owner"]["id"] == spotify_id:
            spotify_playlists_ids.add(playlist["id"])
    return spotify_playlists_ids


# REQUESTS OFFSET

def get_spotify_response_all_items(spotify_req_function, access_token):
    offset = 0
    spotify_response_all_items = []
    while True:
        spotify_response, status_code = spotify_req_function(
            access_token,
            offset
            )
        print(status_code)
        spotify_50items = spotify_response['items']
        if len(spotify_50items) == 0:
            break
        spotify_response_all_items.extend(spotify_50items)
        offset += 50
    return spotify_response_all_items


# SPOTIFY API REQUESTS

def spotify_request(base_url, offset, access_token):

    params = {'limit': 50, 'offset': offset}
    url = base_url + '?' + urllib.parse.urlencode(params)
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    spotify_response_json = requests.get(url, headers=headers)
    status_code = spotify_response_json.status_code
    spotify_response = spotify_response_json.json()
    return spotify_response, status_code


def spotify_req_get_users_saved_tracks(access_token, offset):
    '''retrieving 50 saved songs from spotify at a time'''

    base_url = 'https://api.spotify.com/v1/me/tracks'
    spotify_saved_tracks_response, status_code = spotify_request(
        base_url,
        offset,
        access_token
    )
    return spotify_saved_tracks_response, status_code


def spotify_req_get_users_playlists(access_token, offset):
    '''retrieving info about 50 playlists from spotify at a time'''

    base_url = 'https://api.spotify.com/v1/me/playlists'
    spotify_playlists_response, status_code = spotify_request(
        base_url,
        offset,
        access_token
        )
    return spotify_playlists_response, status_code


def spotify_req_get_playlist_items(access_token, offset, playlist_id):
    '''retrieving 50 songs from spotify's particular playlist at a time'''
    base_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    spotify_playlist_items_response, status_code = spotify_request(
        base_url,
        offset,
        access_token
        )
    return spotify_playlist_items_response, status_code
