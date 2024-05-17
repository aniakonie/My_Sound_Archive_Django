import os
import string
import random
import base64
import urllib.parse

import requests
from dotenv import load_dotenv

from django.http import Http404
from django.contrib import messages
from django.shortcuts import redirect

from spotify_library.models import UserSettings
from .models import SpotifyToken

load_dotenv()



def authorization(request):
    if not request.user.is_authenticated:
        raise Http404    
    is_library_created = UserSettings.objects.filter(user=request.user)
    if is_library_created:
        return redirect('sound_archive:archive')
    is_token_saved = SpotifyToken.objects.filter(user=request.user)
    if is_token_saved:
        return redirect('spotify_library:create_archive')

    spotify_login_page_url, state = request_authorization()
    request.session['state'] = state
    return redirect(spotify_login_page_url)


def callback(request):
    '''in case user accepted app's request and logged in:
    retrieving query parameters (code and state) from spotify callback
    '''
    if not request.user.is_authenticated:
        raise Http404
    state_received = request.GET.get("state", None)
    # User tried to access this url by typing it in the browser.
    if state_received is None:
        raise Http404
    else:
        if state_received != request.session['state']:
            pass
            #TODO
        else:
            del request.session['state']
            # Spotify sent back an error - something went wrong
            # or user refused access to his/her spotify account.
            error = request.GET.get("error", None)
            if error is not None:
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
                    return redirect('sound_archive:archive')
                else:
                    messages.add_message(
                        request,
                        messages.ERROR,
                        '''Oops, something went wrong. Spotify refused 
                        to cooperate. Please try again by clicking 
                        'Log in to Spotify'
                        ''')
                    return redirect('sound_archive:archive')
            else:
                code = request.GET.get("code")
                access_token, refresh_token = get_token_initial(code)
                save_token(access_token, refresh_token, request)
    return redirect('spotify_library:create_archive')


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
    spotify_user = SpotifyToken.objects.filter(user = request.user)
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
                    '''You have My Sound Archive account with this Spotify
                    account already, please log in to this account.
                    ''')
                return redirect('pages:home')
            else:
                new_spotify_user = SpotifyToken(
                    user=request.user,
                    spotify_id=spotify_id,
                    access_token=access_token,
                    refresh_token=refresh_token)
                new_spotify_user.save()
    else:
        spotify_user[0].access_token = access_token
        spotify_user[0].save()
        return access_token


def get_access_token(request):
    current_user = request.user
    spotify_user = SpotifyToken.objects.get(user_id=current_user.id)
    access_token = spotify_user.access_token
    refresh_token = spotify_user.refresh_token
    is_valid = check_token_validity(access_token)
    if is_valid is False:
        access_token = do_refresh_token(refresh_token, request)
    return access_token


def check_token_validity(access_token):
    '''making an API request to check the type of response'''
    response = spotify_req_get_current_user_profile(access_token)
    return response.status_code != 401


def do_refresh_token(refresh_token, request):
    grant_type = 'refresh_token'
    params = {'grant_type': grant_type, 'refresh_token': refresh_token}
    access_token_response_dict = token_request(params)
    access_token = access_token_response_dict['access_token']
    save_token(access_token, refresh_token, request)
    return access_token


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


def convert_to_base64_str(data):
    data_bytes = data.encode('ascii')
    data_base64_str = base64.b64encode(data_bytes).decode()
    return data_base64_str
