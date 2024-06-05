<h1 align="center"> My Sound Archive </h1> <br>
<p align="center">
    <a href="http://mysoundarchive.com/">www.mysoundarchive.com</a>
</p>
<br>
<br>
<p align="center">
  <a href="http://mysoundarchive.com/">
    <img alt="MySoundArchive" title="MySoundArchive" src="https://github.com/aniakonie/My_Sound_Archive/assets/112773165/b92cfdc9-42b2-4744-8ac1-4f3691d15dc7/logo-inkscape-svg.png" width="200">
  </a>
</p>

A web application that displays Spotify user's library organized into artists, genres and subgenres folders, offering a convenient way to browse through the music collection.

## What problem does it solve

Spotify is renowned for its highly effective music recommendation algorithm, yet the user's library lacks methods for organizing its content. While it's easy to discover new music to add to your collection, it becomes increasingly challenging to keep track of it.

Unless you search through a long list of liked songs or artists when selecting something to listen to there's a risk of missing a significant portion of your content. While it's possible to organize songs into playlists, adding them all to playlists isn't a practical solution. Playlists can be organized into folders but unfortunately this feature is not extended to artists whom the user follows.

## In what way does it solve this problem

My Sound Archive app retrieves liked songs and all tracks from a user's playlists through the Spotify API. It then consolidates them and organizes the collection into corresponding artists and genres folders. Users can play songs on Spotify by using the links provided within the app.

<p align="center">
    <img alt="MySoundArchive" title="MySoundArchive" src="https://github.com/aniakonie/My_Sound_Archive/assets/112773165/7732115e-dce4-400b-b908-4ba6d3d386a9/Capture.png" width="700">
</p>

## Technologies used

* Python 3.12
* Django 5.0
* PostgreSQL 16
* Spotify REST API
* OAuth 2.0
* Bootstrap 5.3
* Docker, Poetry

## APIs used

My Sound Archive app uses Spotify API (REST API) with OAuth 2.0 standard.
The authorization code flow used in the app is shown in the following Whimsical schema:

https://whimsical.com/vml-s-oauth-2-0-AK9SEvFpFv4AvF9nLMGuSb

## Whimsical mockup designs

Mockup designs for the app can be found in the following link:

https://whimsical.com/vml-mockups-3bYjFTHMP4NWSAbbUh7khH

## Deployed website

You can access the live version of the web app here: http://mysoundarchive.com/

## Project status

Project is currently in development mode, which means that it can serve up to 25 users (according to Spotify's rules).

Some of the improvements on the horizon:

* submitting an extension request to Spotify for the app (to serve more users),
* addressing library retrieval failures caused by temporary issues in Spotify's backend,
* improving the algorithm for assigning genres to artists,
* adding an option to modify genres assigned by the app,
* integrating Google authentication.

## What I'm currently working on

You can check what I am currently working on here:
http://github.com/users/aniakonie/projects/1


## Setup with Docker

1. Clone the repository:<br>
    `git clone https://github.com/aniakonie/My_Sound_Archive_Django.git`

2. Create a new `.env` file and save it in the root directory of the project.<br>

    Add the following variables to the file (values to be added in the next steps):<br>
    `CLIENT_ID = ""`<br>
    `CLIENT_SECRET = ""`<br>
    `SECRET_KEY = ""`<br>
    `REDIRECT_URI_SPOTIFY = "http://127.0.0.1:8000/spotify/callback"`<br>
    `DEMO_USER_ID = ""`<br>
    `DB_DOCKER_PASSWORD = ""`<br>
    (`SECRET_KEY` should be a long random bytes or string)<br>
    (`DEMO_USER_ID` is the ID of the user whose archive is shown on the "see an example" page)<br>
    (`DB_DOCKER_PASSWORD` - choose your password)

3. Head over to Spotify for Developers: http://developer.spotify.com/<br>
    Go to your dashboard and create a new app.<br>
    In the "Redirect URIs" field, paste the following link: `http://127.0.0.1:8000/spotify/callback`<br>
    Copy your Client ID and Client Secret to your `.env` file (`CLIENT_ID` and `CLIENT_SECRET`).

4. Install Docker Desktop from Docker’s official website, if you haven’t already.

5. In terminal, head over to the root directory of the project containing `Dockerfile` and `compose.yaml` and run the command:<br>
    `docker-compose up -d` 
    
6. To perform the initial migration for the database, execute the following command:<br>
    `docker-compose exec web python manage.py migrate`
    
7. With the development server running, visit the following URL in your browser:
    
    http://127.0.0.1:8000/

8. If you wish to stop the Docker containers, run:<br>
    
    `docker-compose down`<br>
    All data that was added to the database will be stored in the root folder of the project. Next time you run `docker-compose up -d`, no additional commands need to be executed and your postgres data will be abailable to use.


## Setup with Poetry

1. Clone the repository:<br>
    `git clone https://github.com/aniakonie/My_Sound_Archive_Django.git`

2. Install poetry to set up a virtual environment:<br>
    `pip install poetry`
    Change poetry configuration so that the virtual environments will be installed in the project folder:
    `poetry config virtualenvs.in-project true`

3. Navigate to the project directory containing the `pyproject.toml` file and create a virtual environment with the following command:<br>
    `poetry install`<br>
    All required dependencies are installed with this command as well.

4. Create a new `.env` file and save it in the root directory of the project.<br>

    Add the following variables to the file (values to be added in the next steps):<br>
    `CLIENT_ID = ""`<br>
    `CLIENT_SECRET = ""`<br>
    `SECRET_KEY = ""`<br>
    `DATABASE_URL = ""`<br>
    `REDIRECT_URI_SPOTIFY = "http://127.0.0.1:8000/spotify/callback"`<br>
    `DEMO_USER_ID = ""`<br>
    (`SECRET_KEY` should be a long random bytes or string)<br>
    (`DEMO_USER_ID` is the ID of the user whose archive is shown on the "see an example" page)

5. Head over to Spotify for Developers: http://developer.spotify.com/<br>
    Go to your dashboard and create a new app.<br>
    In the "Redirect URIs" field, paste the following link: `http://127.0.0.1:8000/spotify/callback`<br>
    Copy your Client ID and Client Secret to your `.env` file (`CLIENT_ID` and `CLIENT_SECRET`).

6. Install PostgreSQL and create a new database. It will store users' login credentials and data retrieved from Spotify.<br>
    Add your database url to your `.env` file (`DATABASE_URL`).<br>
    The URI scheme can be of the following form:<br>
    `"postgres://[username]:[password]@[host]:[port]/[database_name]"`<br>
    Replace the placeholders in square brackets with your actual PostgreSQL credentials.

7. Navigate to the root directory of the project, activate your environment and initialize database migrations with the following commands:<br>

    `poetry shell`<br>
    `python manage.py migrate`

8. With your environment activated, run the application using `python manage.py runserver`<br>

    With the development server running, visit the following URL in your browser:<br>
    http://127.0.0.1:8000/

