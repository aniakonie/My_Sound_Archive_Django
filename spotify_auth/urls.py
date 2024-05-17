from django.urls import path
from . import views

app_name = 'spotify_auth'

urlpatterns = [
    path("authorization", views.authorization, name='authorization'),
    path("callback", views.callback),
]
