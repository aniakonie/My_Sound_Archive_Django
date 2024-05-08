import random

from spotify_library.get_spotify_genres import spotify_get_artists_genres
from spotify_library.models import Artists, UserArtists

from django.contrib.auth.models import User


def classify_artists_genres(request):
    '''retrieving all artists without corresponding genres from database'''
    artists = Artists.objects.filter(artist_genres = '')
    if artists:
        artists_uris = [artist.artist_uri[15:] for artist in list(artists)]
        artists_uris_genres = spotify_get_artists_genres(artists_uris, request)

        artists_uris_genres_main_genre = []
        for artist in artists_uris_genres:
            genres_string = ", ".join(artist[1])
            main_genre = assign_main_genre(genres_string)
            artists_uris_genres_main_genre.append((artist + (main_genre,)))
        save_artists_genres(artists_uris_genres_main_genre)
    save_user_artists_genres(request)


def save_artists_genres(artists_uris_genres_main_genre):
    '''saving genres and subgenres to global table artists'''
    for artist in artists_uris_genres_main_genre:
        artist_uri_genre = Artists.objects.get(artist_uri = artist[0])
        artist_uri_genre.artist_genres = ', '.join(artist[1])
        artist_uri_genre.artist_main_genre = artist[2]
        #TODO assign subgenres
        artist_uri_genre.artist_subgenre = 'others'
        artist_uri_genre.save()

#TODO add subgenres classification

def save_user_artists_genres(request):
    '''saving genres and subgenres to table user_artists'''
    user_artists = UserArtists.objects.filter(user = request.user)
    for user_artist in user_artists:
        artist = user_artist.artist_uri
        user_artist.artist_main_genre_custom = artist.artist_main_genre
        user_artist.artist_subgenre_custom = artist.artist_subgenre
        user_artist.save()


main_genres ={
    "metal",
    "rock",
    "jazz", 
    "pop",
    "rap",
    "reggae",
    "electronic",
    "classical music",
    "country",
    "funk",
    "blues",
    "ambient",
    }

electronic = {
    "dubstep",
    "techno",
    "house",
    "drum and bass",
    "liquid funk"
}

reggae = {
    "polish reggae",
    "dub",
    "roots reggae"
}

rock = {
    "punk"
}


rap = {
    "hip hop"
}


def assign_main_genre(genres_string):

    genres_string = genres_string.lower()
    main_genres_dict = dict()
    #counting how many times names of the main genres occur in the artist_genres retrieved from spotify (exclude 0 times)
    for item in main_genres:
        if genres_string.count(item) > 0:
            main_genres_dict[item] = genres_string.count(item)
            
    #list of the biggest occurences
    genre_classification = [
        name for (name, num_of_occur) in main_genres_dict.items()
        if num_of_occur == max(main_genres_dict.values())
        ]

    if len(genre_classification) == 1:
        main_genre = genre_classification[0]
    elif len(genre_classification) > 1:
        main_genre = random.choice(genre_classification)
    elif len(genre_classification) == 0:
        main_genre = "others"
    return main_genre



#dnb
#liquid funk is an electronic subgenre (=liquid drum and bass)!
#electronica
#metalcore, post-metal, post-rock
