from django import forms
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from spotify_library.models import UserSettings


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
    if request.user.is_authenticated:
        return redirect('sound_archive:archive')
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            is_already_taken = User.objects.filter(username=username)
            if is_already_taken:
                messages.add_message(
                    request,
                    messages.ERROR,
                    '''Such user already exists.
                    Please choose different username.''')
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password
                    )
                user.save()
                user_auth = authenticate(username=username, password=password)
                if user_auth:
                    login(request, user_auth)
                    return redirect('pages:log_in_to_spotify')
    else:
        form = SignupForm()
    return render(request, "sign_up.html", {"form": form})


def log_in(request):
    if request.user.is_authenticated:
        return redirect('sound_archive:archive')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user_auth = authenticate(username=username, password=password)
            if user_auth:
                login(request, user_auth)
                return redirect('sound_archive:archive')
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Wrong login credentials.")
    else:
        form = LoginForm()
    return render(request, "log_in.html", {"form": form})


def log_out(request):
    if not request.user.is_authenticated:
        raise Http404
    logout(request)
    return redirect('pages:home')


def log_in_to_spotify(request):
    if not request.user.is_authenticated:
        raise Http404
    is_library_created = UserSettings.objects.filter(user=request.user)
    if is_library_created:
        return redirect('sound_archive:archive')
    if request.method == "POST":
        return redirect('spotify_auth:authorization')
    return render(
        request,
        "log_in_to_spotify.html",
        {"username": request.user.username}
        )


def delete_account(request):
    if not request.user.is_authenticated:
        raise Http404
    user_settings = UserSettings.objects.filter(user = request.user)
    if user_settings:
        is_library_created = True
    else:
        is_library_created = False
    if request.method == "POST":
        if request.POST.get("answer") == "Yes":
            user = request.user
            user.delete()
            messages.add_message(
                request,
                messages.SUCCESS,
                'Your account has been deleted.'
            )
            return redirect("pages:home")
        else:
            return redirect('sound_archive:archive')
    return render(request, "delete_account.html", {
        'is_library_created': is_library_created
    })


#TODO
#login_required URL
