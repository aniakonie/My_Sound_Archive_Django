from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


#TODO move forms' style to html
class SignupForm(forms.Form):
    username = forms.CharField(min_length=5, max_length=30)
    password = forms.CharField(min_length=5, max_length=30, widget=forms.PasswordInput)

    username.widget.attrs['class'] = "form-control"
    username.widget.attrs['style'] = "background-color :rgb(20, 20, 20); color:white;"
    password.widget.attrs['class'] = "form-control"
    password.widget.attrs['style'] = "background-color :rgb(20, 20, 20); color:white;"
    password.widget.attrs['id'] = 'pswd'


class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    username.widget.attrs['class'] = "form-control"
    username.widget.attrs['style'] = "background-color :rgb(20, 20, 20); color:white;"
    password.widget.attrs['class'] = "form-control"
    password.widget.attrs['style'] = "background-color :rgb(20, 20, 20); color:white;"



def home(request):
    return render(request, "home.html")


def how_it_works(request):
    return render(request, "how_it_works.html")


def sign_up(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            is_already_taken = User.objects.filter(username=username)
            if is_already_taken:
                messages.add_message(request, messages.ERROR, "Such user already exists. Please choose different username.")
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                user_auth = authenticate(username=username, password=password)
                if user_auth:
                    login(request, user_auth)
                    return redirect(log_in_to_spotify)
    else:
        form = SignupForm()

    return render(request, "sign_up.html", {"form": form})


def log_in(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user_auth = authenticate(username=username, password=password)
            if user_auth:
                login(request, user_auth)
                return redirect(log_in_to_spotify) #change to archive page
            else:
                messages.add_message(request, messages.ERROR, "Wrong login credentials.")
    else:
        form = LoginForm()

    return render(request, "log_in.html", {"form": form})


@login_required
def log_out(request):
    logout(request)
    return redirect(home)


@login_required
def log_in_to_spotify(request):
    user = request.user
    return render(request, "log_in_to_spotify.html", {"username": user.username})


#TODO
#login_required URL