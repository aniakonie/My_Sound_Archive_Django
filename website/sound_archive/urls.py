from django.urls import path
from . import views

app_name = 'sound_archive'

urlpatterns = [
    path("", views.archive, name='archive'),
    path("<selected_genre>", views.archive_genres, name='archive_genres'),
    path("<selected_genre>/<selected_subgenre>", views.archive_subgenres, name='archive_subgenres'),
    path("<selected_genre>/<selected_subgenre>/<selected_artist_name>", views.archive_tracks, name='archive_tracks'),
]