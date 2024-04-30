import os
import string
import random
import base64

import requests
import urllib.parse
from dotenv import load_dotenv

from .models import SpotifyToken
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


load_dotenv()


@login_required
def authorization(request):
    spotify_login_page_url, state = request_authorization()
    request.session['state'] = state
    return redirect(spotify_login_page_url)


@login_required
def callback(request):
    '''in case user accepted app's request and logged in:
    retrieving query parameters (code and state) from spotify callback
    '''
    state_received = request.GET.get("state", None)
    # User tried to access this url by typing it in the browser.
    if state_received == None:
        pass
        # abort(401)
    else:
        if state_received != request.session['state']:
            pass
            # message
        else:
            del request.session['state']
            # Spotify sent back an error - something went wrong
            # or user refused access to his/her spotify account.
            error = request.GET.get("error", None)
            if error != None:
                if error == "access_denied":
                    messages.add_message(
                        request,
                        messages.ERROR,
                        '''Did you mean to refuse access to your Spotify 
                        account? If not, please click 'Log in to Spotify' 
                        again. If you did mean it and you are not sure 
                        whether to accept it, please head over to 
                        'How it works' page and find out more about the app.
                        ''')
                    # return redirect(url_for("library_bp.library"))
                else:
                    messages.add_message(
                        request,
                        messages.ERROR,
                        '''Oops, something went wrong. Spotify refused 
                        to cooperate. Please try again by clicking 
                        'Log in to Spotify
                        ''')
                    # return redirect(url_for("library_bp.library"))
            else:
                code = request.GET.get("code")
                access_token, refresh_token = get_token_initial(code)
                save_token(access_token, refresh_token, request)
    #redirect to archive page
    return redirect('pages:home')


def request_authorization():
    client_id = os.getenv("CLIENT_ID")
    response_type = 'code'
    redirect_uri = os.getenv("REDIRECT_URI_SPOTIFY")
    scope = '''user-library-read playlist-read-private user-follow-read 
        user-read-private user-read-email
        '''
    state = ''.join(random.choices(
        string.ascii_lowercase + string.digits, k=10
        ))
    params = {
        'client_id': client_id,
        'response_type': response_type,
        'redirect_uri': redirect_uri,
        'scope': scope,
        'state': state
        }
    authorize_url = 'https://accounts.spotify.com/authorize'
    spotify_login_page_url = (
        authorize_url + '?' + urllib.parse.urlencode(params)
        )
    #TODO add a behaviour for response status other than 200
    return spotify_login_page_url, state


def get_token_initial(code):
    '''exchanging authorization code for an access token 
    - post request to the token endpoint
    '''
    redirect_uri = os.getenv("REDIRECT_URI_SPOTIFY")
    grant_type = 'authorization_code'
    params = {
        'grant_type': grant_type,
        'code': code,
        'redirect_uri': redirect_uri
        }
    access_token_response_dict = token_request(params)
    access_token = access_token_response_dict['access_token']
    refresh_token = access_token_response_dict['refresh_token']
    return access_token, refresh_token


def token_request(params):
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    get_token_base_url = 'https://accounts.spotify.com/api/token'
    get_token_url = (
        get_token_base_url + '?' + urllib.parse.urlencode(params)
        )
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'Authorization': (
            'Basic ' + convert_to_base64_str(client_id + ':' + client_secret)
            )
    }
    access_token_response = requests.post(get_token_url, headers=headers)
    access_token_response_dict = access_token_response.json()
    return access_token_response_dict


def save_token(access_token, refresh_token, request):
    current_user = request.user
    spotify_user = SpotifyToken.objects.filter(user_id = current_user.id)
    if not spotify_user:
        spotify_id, status_code = get_spotify_id(access_token)
        if status_code == 403:
            messages.add_message(
                request,
                messages.ERROR,
                '''If you wish to create your sound archive, please let us 
                know by sending an email to the following address: 
                mysoundarchiveofficial@gmail.com.
                This app is currently in development mode, so we need to 
                grant you permission first.
                ''')
            return redirect('pages:home')
        else:
            exists_already = SpotifyToken.objects.filter(spotify_id=spotify_id)
            if exists_already:
                messages.add_message(
                    request,
                    messages.ERROR,
                    ''''You have My Sound Archive account with this Spotify
                    account already, please log in to this account.
                    ''')
                return redirect('pages:home')
            else:
                new_spotify_user = SpotifyToken(
                    user_id=current_user.id,
                    spotify_id=spotify_id,
                    access_token=access_token,
                    refresh_token=refresh_token)
                new_spotify_user.save()
    else:
        current_user.access_token = access_token
        current_user.save()
        return access_token


def convert_to_base64_str(data):
    data_bytes = data.encode('ascii')
    data_base64_str = base64.b64encode(data_bytes).decode()
    return data_base64_str


def get_spotify_id(access_token):
    current_user_profile_data_response = spotify_req_get_current_user_profile(access_token)
    status_code = current_user_profile_data_response.status_code
    if status_code == 403:
        spotify_id = None
        return spotify_id, status_code
    else:
        current_user_profile_data = current_user_profile_data_response.json()
        spotify_id = current_user_profile_data["id"]
        return spotify_id, status_code


def spotify_req_get_current_user_profile(access_token):
    get_user_base_url = 'https://api.spotify.com/v1/me'
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    current_user_profile_data_response = requests.get(
        get_user_base_url,
        headers=headers
        )
    return current_user_profile_data_response