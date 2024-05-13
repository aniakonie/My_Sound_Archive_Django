from django.urls import path
from . import views, views_demo

app_name = 'sound_archive'

urlpatterns = [
    path("archive/", views.archive, name='archive'),
    path("archive/<selected_genre>", views.archive_genres, name='archive_genres'),
    path("archive/<selected_genre>/<selected_subgenre>", views.archive_subgenres, name='archive_subgenres'),
    path("archive/<selected_genre>/<selected_subgenre>/<selected_artist_name>", views.archive_tracks, name='archive_tracks'),
    path("demo/", views_demo.demo_archive, name='demo_archive'),
    path("demo/<selected_genre>", views_demo.demo_archive_genres, name='demo_archive_genres'),
    path("demo/<selected_genre>/<selected_subgenre>", views_demo.demo_archive_subgenres, name='demo_archive_subgenres'),
    path("demo/<selected_genre>/<selected_subgenre>/<selected_artist_name>", views_demo.demo_archive_tracks, name='demo_archive_tracks'),
    path("settings", views.settings, name='settings'),
]