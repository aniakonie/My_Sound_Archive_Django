import json
import time

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .get_spotify_data import get_spotify_data
from .parse_spotify_data import parse_spotify_data
from .save_spotify_data import save_spotify_data
from spotify_auth.models import SpotifyToken
from spotify_auth.views import get_access_token
from sound_archive.genre_classification import classify_artists_genres


@login_required
def create_archive(request):
    if request.method == "POST":
        if request.POST["create_archive"] == "Changed my mind":
            pass
            #return redirect to archive
        else:
            create_archive(request)
            #return redirect to archive
    return render(request, "create_archive.html")


def create_archive(request):
    spotify_user = SpotifyToken.objects.get(user_id=request.user.id)
    spotify_id = spotify_user.spotify_id
    access_token = get_access_token(request)

    start = time.perf_counter()
    (spotify_playlists, spotify_saved_tracks,
     spotify_all_playlists_tracks) = get_spotify_data(
        access_token,
        spotify_id
        )
    end = time.perf_counter()
    print('spotify_data time: ', end - start)


    start = time.perf_counter()
    (playlists_info_library, saved_tracks_library,
     all_playlists_tracks_library) = parse_spotify_data(
        spotify_playlists, 
        spotify_saved_tracks,
        spotify_all_playlists_tracks,
        spotify_id
        )
    end = time.perf_counter()
    print('parsing time: ', end - start)


    start = time.perf_counter()
    save_spotify_data(playlists_info_library, saved_tracks_library,
                      all_playlists_tracks_library, request)
    end = time.perf_counter()
    print('saving to database time: ', end - start)   

    start = time.perf_counter()
    classify_artists_genres(request)
    end = time.perf_counter()
    print('retrieving and saving artists genres time: ', end - start) 


    print('library retrieved')
    pass




# def save_default_user_settings():
#     user_settings = UserSettings(current_user.id)
#     db.session.add(user_settings)
#     db.session.commit()