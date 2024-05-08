import time
import json

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import UserSettings
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
            return redirect("sound_archive:archive")
        else:
            do_create_archive(request)
            return redirect("sound_archive:archive")
    return render(request, "create_archive.html")


def do_create_archive(request):
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


    # with open('spotify_playlists.json', 'r') as json_file:
    #     spotify_playlists = json.load(json_file)

    # with open('spotify_saved_tracks.json', 'r') as json_file:
    #     spotify_saved_tracks = json.load(json_file)
    
    # with open('spotify_all_playlists_tracks.json', 'r') as json_file:
    #     spotify_all_playlists_tracks = json.load(json_file)


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

    user_settings = UserSettings(user = request.user, is_library_created = True)
    user_settings.save()

