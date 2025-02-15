from .models import Tracks, UserTracks, UserPlaylists, UserArtists, Artists


def save_spotify_data(playlists_info_library, saved_tracks_library,
                      all_playlists_tracks_library, request):

    save_playlists_info(playlists_info_library, request)
    save_saved_tracks(saved_tracks_library, request)
    save_all_playlists_tracks(all_playlists_tracks_library, request)


def save_playlists_info(playlists_info_library, request):
    for playlist_id, playlist_name, is_owner in playlists_info_library:
        if is_owner:
            display_in_library = True
            user_playlist = UserPlaylists(
                playlist_id = playlist_id,
                playlist_name = playlist_name,
                is_owner = is_owner,
                display_in_library = display_in_library,
                user = request.user
            )
            user_playlist.save()


def save_saved_tracks(saved_tracks_library, request):
    for track in saved_tracks_library:

        new_artist = add_artist_to_artists(track)
        add_artist_to_user_artists(track, request, new_artist)
        new_track = add_track_to_tracks(track, new_artist)
        user_track = UserTracks(
            track_uri = new_track,
            playlist_id_or_saved_song = 'saved song',
            display_in_library = True,
            user = request.user
        )
        user_track.save()


def save_all_playlists_tracks(all_playlists_tracks_library, request):
    playlists_ids = list(all_playlists_tracks_library.keys())
    for playlist in playlists_ids:
        user_playlist = UserPlaylists.objects.get(playlist_id = playlist)
        display_in_library = user_playlist.is_owner
        playlist_tracks = all_playlists_tracks_library[playlist]

        for track in playlist_tracks:
            new_artist = add_artist_to_artists(track)
            add_artist_to_user_artists(track, request, new_artist)
            new_track = add_track_to_tracks(track, new_artist)
            user_track, created = UserTracks.objects.get_or_create(
                track_uri = new_track,
                playlist_id_or_saved_song = playlist,
                display_in_library = display_in_library,
                user = request.user
            )


def add_track_to_tracks(track, new_artist):

    new_track, created = Tracks.objects.get_or_create(
        track_uri = track["track_uri"],
        track_artist_main = track["track_artist_main"][:100],
        main_artist_uri = new_artist,
        track_artist_add1 = track["track_artist_add1"][:100]
        if track["track_artist_add1"] is not None else '',
        track_artist_add2 = track["track_artist_add2"][:100]
        if track["track_artist_add2"] is not None else '',
        track_title = track["track_title"][:100],
        album_artist_main = track["album_artist_main"][:100],
        album_artist_add1 = track["album_artist_add1"][:100]
        if track["album_artist_add1"] is not None else '',
        album_artist_add2 = track["album_artist_add2"][:100]
        if track["album_artist_add2"] is not None else '',
        album_title = track["album_title"][:100],
        album_uri = track["album_uri"]
    )
    return new_track


def add_artist_to_artists(track):

    new_artist, created = Artists.objects.get_or_create(
        artist_uri = track["main_artist_uri"],
        artist_name = track["track_artist_main"][0:50],
    )
    return new_artist


def add_artist_to_user_artists(track, request, new_artist):

    user_artist, created = UserArtists.objects.get_or_create(
        artist_uri = new_artist,
        artist_name = track["track_artist_main"][0:50],
        user = request.user
    )
