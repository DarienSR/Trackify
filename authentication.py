# Connect to Spotify API
import spotipy
import os # used to get our env variables.
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

# SETUP FOR SPOTIFY API
scope = 'playlist-modify-private playlist-modify-public user-read-recently-played user-read-playback-position user-top-read user-read-currently-playing user-read-playback-state'


username = ""  # ENTER SPOTIFY USERNAME HERE

# ENV Application Tokens. 
CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')

# Prompt user for access to their account informatiSon
token = util.prompt_for_user_token(username, scope, CLIENT_ID, CLIENT_SECRET, 'http://localhost:3000/')
sp = spotipy.Spotify(auth=token)
