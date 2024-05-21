import random

from spotify_library.get_spotify_genres import spotify_get_artists_genres
from spotify_library.models import Artists, UserArtists



def classify_artists_genres(request):
    '''retrieving all artists without corresponding genres from database'''
    artists = Artists.objects.filter(artist_genres = '')
    if artists:
        artists_uris = [artist.artist_uri[15:] for artist in list(artists)]
        artists_uris_genres = spotify_get_artists_genres(artists_uris, request)
        artists_uris_genres_classified = []
        for artist in artists_uris_genres:
            genres_string = ", ".join(artist[1])
            classified_genre, classified_subgenre = assign_genres(genres_string)
            artists_uris_genres_classified.append((artist + (classified_genre, classified_subgenre)))
        save_artists_genres(artists_uris_genres_classified)
    save_user_artists_genres(request)


def save_artists_genres(artists_uris_genres_classified):
    '''saving genres and subgenres to global table artists'''
    for artist in artists_uris_genres_classified:
        artist_uri_genre = Artists.objects.get(artist_uri = artist[0])
        artist_uri_genre.artist_genres = ', '.join(artist[1])
        artist_uri_genre.artist_main_genre = artist[2]
        artist_uri_genre.artist_subgenre = artist[3]
        artist_uri_genre.save()


def save_user_artists_genres(request):
    '''saving genres and subgenres to table user_artists'''
    user_artists = UserArtists.objects.filter(user = request.user)
    for user_artist in user_artists:
        artist = user_artist.artist_uri
        user_artist.artist_main_genre_custom = artist.artist_main_genre
        user_artist.artist_subgenre_custom = artist.artist_subgenre
        user_artist.save()


main_genres = {
    "electronic": [
        "dubstep",
        "techno",
        "house",
        "drum and bass",
        "dnb",
        "liquid funk",
        "future garage",
        "electronica",
    ],
    "metal":{},
    "rock":{
        "punk"
    },
    "jazz":{},
    "pop":{},
    "rap":{
        "hip hop"
    },
    "reggae":{
        "polish reggae",
        "dub",
        "roots reggae"
    },
    "classical music":{},
    "country":{},
    "funk":{},
    "blues":{},
    "ambient":{},
}


def assign_genres(genres_string):

    genres_string = genres_string.lower()
    main_genres_dict = {}

    for genre, subgenres in main_genres.items():

        # Counting how many times names of the main genres occur
        # in the artist_genres retrieved from spotify (exclude 0 times)
        if genres_string.count(genre) > 0:
            main_genres_dict[genre] = genres_string.count(genre)

        for subgenre in subgenres:
            if subgenre in genres_string:
                classified_genre = genre
                if "dnb" in subgenre:
                    classified_subgenre = "drum and bass"
                elif "liquid" in subgenre:
                    classified_subgenre = "liquid funk"
                elif "electronica" in subgenre:
                    classified_subgenre = "others"
                elif "hip hop" in subgenre:
                    classified_subgenre = "others"
                else:
                    classified_subgenre = subgenre
                return classified_genre, classified_subgenre

    # If classification based on subgenre doesn't return a result,
    # then classification based solely on genres is performed
    genre_classification = [
        name for (name, num_of_occur) in main_genres_dict.items()
        if num_of_occur == max(main_genres_dict.values())
        ]
    if len(genre_classification) == 1:
        classified_genre = genre_classification[0]
    elif len(genre_classification) > 1:
        classified_genre = random.choice(genre_classification)
    elif len(genre_classification) == 0:
        classified_genre = "others"
    classified_subgenre = "others"
    return classified_genre, classified_subgenre
