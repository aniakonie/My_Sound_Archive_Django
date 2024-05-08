from django.shortcuts import render

from django.db.models import Subquery
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from spotify_library.models import *



@login_required
def archive(request):

    try:
        user_settings = UserSettings.objects.get(user = request.user)
        is_library_created = True
        genres = get_genres(request)
        if request.method == "POST":
            selected_genre = request.form["selected_genre"]
            print(selected_genre)
            # return redirect(url_for("library_bp.library_genres", selected_genre = selected_genre))

    except ObjectDoesNotExist:
        is_library_created = False
        genres = None
        if request.method == "POST":
            return redirect("spotify_auth:authorization")

    return render(request, "archive.html", {"genres": genres, "is_library_created": is_library_created})





def get_genres(request):

    subquery = Tracks.objects.filter(
        usertracks__user=request.user,
        usertracks__display_in_library=True
    ).values('main_artist_uri')

    query = UserArtists.objects.filter(
        user=request.user,
        artist_uri__in=Subquery(subquery)
    ).values('artist_main_genre_custom').distinct().order_by('artist_main_genre_custom')

    genres = list(query)
    if "others" in genres:
        genres.remove("others")
        genres.append("others")
    return genres
