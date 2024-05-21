import time
import json

from django.http import Http404
from django.shortcuts import render, redirect

from spotify_auth.models import SpotifyToken
from spotify_auth.views import get_access_token
from sound_archive.genre_classification import classify_artists_genres
from .models import UserSettings
from .get_spotify_data import get_spotify_data
from .parse_spotify_data import parse_spotify_data
from .save_spotify_data import save_spotify_data


def create_archive(request):
    if not request.user.is_authenticated:
        raise Http404
    is_library_created = UserSettings.objects.filter(user=request.user)
    if is_library_created:
        return redirect('sound_archive:archive')
    is_token_saved = SpotifyToken.objects.filter(user=request.user)
    if not is_token_saved:
        return redirect('sound_archive:archive')
    if request.method == "POST":
        if request.POST['create_archive'] == 'Changed my mind':
            return redirect('sound_archive:archive')
        else:
            do_create_archive(request)
            return redirect('sound_archive:archive')
    return render(request, 'create_archive.html')


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
