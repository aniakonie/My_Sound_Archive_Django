from spotify_library.models import UserPlaylists, UserSettings, UserTracks


def get_user_playlists(user):
    user_playlists = UserPlaylists.objects.filter(user = user).order_by('playlist_name')
    if not user_playlists:
        user_playlists_included = "no playlists"
        user_playlists_excluded = "no playlists"
    else:
        user_playlists_included = []
        user_playlists_excluded = []
        for playlist in list(user_playlists):
            if playlist.display_in_library is True:
                user_playlists_included.append(
                    (playlist.playlist_name, playlist.playlist_id)
                )
            else:
                user_playlists_excluded.append(
                    (playlist.playlist_name, playlist.playlist_id)
                )
    return user_playlists_included, user_playlists_excluded


def change_number_of_songs_into_folders(user, number_of_songs_into_folders):
    user_settings = UserSettings.objects.get(user = user)
    user_settings.no_of_songs_into_folder = number_of_songs_into_folders
    user_settings.save()


def change_playlist_display_setting(user, playlist_id_exclude, playlist_id_include):
    playlist_id_to_change = playlist_id_exclude if playlist_id_exclude is not None else playlist_id_include
    change_display_to = False if playlist_id_exclude is not None else True

    playlist_to_change = UserPlaylists.objects.get(
        user=user,
        playlist_id = playlist_id_to_change
    )
    playlist_to_change.display_in_library = change_display_to
    playlist_to_change.save()

    user_tracks = UserTracks.objects.filter(
        user=user,
        playlist_id_or_saved_song = playlist_id_to_change
    )

    for track in user_tracks:
        track.display_in_library = change_display_to
        track.save()
    return change_display_to
