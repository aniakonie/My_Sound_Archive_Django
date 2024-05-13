from django.urls import path
from . import views

app_name = 'spotify_library'

urlpatterns = [
    path("create-archive", views.create_archive, name='create_archive'),
]
