from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth.models import User


class UserPlaylists(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        )
    playlist_id = models.CharField(max_length=25)
    playlist_name = models.CharField(max_length=100)
    is_owner = models.BooleanField()
    display_in_library = models.BooleanField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'playlist_id'],
                name='unique_playlist_ids_for_user'
                )
        ]


class UserTracks(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        )
    track_uri = models.CharField(max_length=36)
    playlist_id_or_saved_song = models.CharField(max_length=25)
    display_in_library = models.BooleanField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'track_uri', 'playlist_id_or_saved_song'],
                name='unique_track_uris_for_user'
                )
        ]


class UserArtists(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        )
    artist_uri = models.CharField(max_length=37)
    artist_name = models.CharField(max_length=50)
    artist_main_genre_custom = models.CharField(max_length=20)
    artist_subgenre_custom = models.CharField(max_length=30)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'artist_uri'],
                name='unique_artist_uris_for_user'
                )
        ]


class Artists(models.Model):
    artist_uri = models.CharField(max_length=37, unique=True)
    artist_name = models.CharField(max_length=50)
    artist_genres = models.CharField(max_length=300)
    artist_main_genre = models.CharField(max_length=20)
    artist_subgenre = models.CharField(max_length=30)


class Tracks(models.Model):
    track_uri = models.CharField(max_length=36, unique=True)
    track_artist_main = models.CharField(max_length=100)
    main_artist_uri = models.CharField(max_length=37)
    track_artist_add1 = models.CharField(max_length=100)
    track_artist_add2 = models.CharField(max_length=100)
    track_title = models.CharField(max_length=100)
    album_artist_main = models.CharField(max_length=100)
    album_artist_add1 = models.CharField(max_length=100)
    album_artist_add2 = models.CharField(max_length=100)
    album_title = models.CharField(max_length=100)
    album_uri = models.CharField(max_length=36)


class UserSettings(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,)
    is_library_created = models.BooleanField(default=False)
    no_of_songs_into_folder = models.IntegerField(default=3)
    include_songs_from_playlists = models.BooleanField(default=True)
    include_followed_playlists = models.BooleanField(default=False)