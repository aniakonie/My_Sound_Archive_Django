from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .spotify_data import *
from spotify_auth.models import SpotifyToken
from spotify_auth.views import get_access_token

@login_required
def create_archive(request):
    if request.method == "POST":
        if request.POST["create_archive"] == "Changed my mind":
            pass
            #return redirect to archive
        else:
            create_library(request)
            #return redirect to archive
    return render(request, "create_archive.html")


def create_library(request):
    current_user = request.user
    spotify_user = SpotifyToken.objects.get(user_id=current_user.id)
    spotify_id = spotify_user.spotify_id
    access_token = get_access_token(request)
    spotify_playlists, spotify_saved_tracks, spotify_all_playlists_tracks = get_spotify_data(
        access_token,
        spotify_id
        )
    print('library retrieved')
    pass






# def save_default_user_settings():
#     user_settings = UserSettings(current_user.id)
#     db.session.add(user_settings)
#     db.session.commit()