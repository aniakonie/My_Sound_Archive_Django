from django.shortcuts import render


def home(request):
    return render(request, "home.html")

def how_it_works(request):
    return render(request, "how_it_works.html")

def sign_up(request):
    return render(request, "sign_up.html")