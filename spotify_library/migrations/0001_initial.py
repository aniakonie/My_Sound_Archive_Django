# Generated by Django 5.0.4 on 2024-05-02 22:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Artists',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist_uri', models.CharField(max_length=37, unique=True)),
                ('artist_name', models.CharField(max_length=50)),
                ('artist_genres', models.CharField(max_length=300)),
                ('artist_main_genre', models.CharField(max_length=20)),
                ('artist_subgenre', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Genres',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(max_length=30, unique=True)),
                ('subgenre', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Tracks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('track_uri', models.CharField(max_length=36, unique=True)),
                ('track_artist_main', models.CharField(max_length=100)),
                ('main_artist_uri', models.CharField(max_length=37)),
                ('track_artist_add1', models.CharField(max_length=100)),
                ('track_artist_add2', models.CharField(max_length=100)),
                ('track_title', models.CharField(max_length=100)),
                ('album_artist_main', models.CharField(max_length=100)),
                ('album_artist_add1', models.CharField(max_length=100)),
                ('album_artist_add2', models.CharField(max_length=100)),
                ('album_title', models.CharField(max_length=100)),
                ('album_uri', models.CharField(max_length=36)),
            ],
        ),
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('is_library_created', models.BooleanField(default=False)),
                ('no_of_songs_into_folder', models.IntegerField(default=3)),
                ('include_songs_from_playlists', models.BooleanField(default=True)),
                ('include_followed_playlists', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserArtists',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist_uri', models.CharField(max_length=37)),
                ('artist_name', models.CharField(max_length=50)),
                ('artist_main_genre_custom', models.CharField(max_length=20)),
                ('artist_subgenre_custom', models.CharField(max_length=30)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserPlaylists',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playlist_id', models.CharField(max_length=25)),
                ('playlist_name', models.CharField(max_length=100)),
                ('is_owner', models.BooleanField()),
                ('display_in_library', models.BooleanField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserTracks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('track_uri', models.CharField(max_length=36)),
                ('playlist_id_or_saved_song', models.CharField(max_length=25)),
                ('display_in_library', models.BooleanField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='userartists',
            constraint=models.UniqueConstraint(fields=('user', 'artist_uri'), name='unique_artist_uris_for_user'),
        ),
        migrations.AddConstraint(
            model_name='userplaylists',
            constraint=models.UniqueConstraint(fields=('user', 'playlist_id'), name='unique_playlist_ids_for_user'),
        ),
        migrations.AddConstraint(
            model_name='usertracks',
            constraint=models.UniqueConstraint(fields=('user', 'track_uri'), name='unique_track_uris_for_user'),
        ),
    ]
