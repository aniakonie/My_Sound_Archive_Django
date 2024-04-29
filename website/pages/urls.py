from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("how-it-works", views.how_it_works),
    path("signup", views.sign_up),
    path("logout", views.log_out),
    path("login", views.log_in),
    path("log-in-to-spotify",  views.log_in_to_spotify)
]

