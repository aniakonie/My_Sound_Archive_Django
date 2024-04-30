from django.db import models
from django.contrib.auth.models import User

class SpotifyToken(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,)
    spotify_id = models.CharField(max_length=40)
    access_token = models.CharField(max_length=270)
    refresh_token = models.CharField(max_length=150)
