from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("how-it-works", views.how_it_works),
    path("sign-up", views.sign_up)
]

