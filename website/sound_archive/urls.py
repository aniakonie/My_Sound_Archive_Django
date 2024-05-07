from django.urls import path
from . import views

app_name = 'sound_archive'

urlpatterns = [
    path("", views.archive, name='archive'),
]