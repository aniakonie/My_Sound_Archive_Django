from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("pages.urls")),
    path("spotify/", include("spotify_auth.urls")),
    path("spotify/", include("spotify_library.urls")),
    path('admin/', admin.site.urls),
]
