# Using the spotipy API to interact with spotify, this application tracks your listening habits. Please note, that in order to receive accurate results, this records in batches of 50. So it should run every 45-50 songs
# to prevent losing out on tracking information.

import spotipy
import os # used to get our env variables.
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import time as time
import sqlite3
import datetime


# SPOTIFY AUTHENTICATION

# Our authentication scope, allow access to the following:
scope = 'playlist-modify-private playlist-modify-public user-read-recently-played user-read-playback-position user-top-read user-read-currently-playing user-read-playback-state'


username = ""  # ENTER SPOTIFY USERNAME HERE


# ENV Tokens. Prompt user for access to their account information
token = util.prompt_for_user_token(username, scope, os.environ.get('SPOTIPY_CLIENT_ID'), os.environ.get('SPOTIPY_CLIENT_SECRET'), 'http://localhost:3000/')
sp = spotipy.Spotify(auth=token)


# DATABASE CONNECTION
connection = sqlite3.connect('Trackify.db') # If no database is found within directory, make one.



try:
    connection.execute('CREATE TABLE track (name text, artist text, timeperiod datetime)')
    connection.execute('CREATE TABLE time (time int)')
    print("Creating Trackify Database")
except:
    print("Welcome Back\n")


cursor = connection.cursor()


# Gets the time in ms since UNIX epoch. Store that. Then we used that to get recently played. So we don't get songs we've already recorded listening too during that time period.


cursor.execute("SELECT MAX(time) FROM time")
sinceLast = cursor.fetchall() # returns an array of tuples


sinceLast = (sinceLast[-1][0]) # get the int, which denotes time since database was last updated.

if(sinceLast != None):
    sinceLast = sinceLast + 90000 # 90 seconds, prevents duped data. Becasue spotify call to recently played is not inclusive. 

   
currentTime = int(round(time.time() * 1000))
cursor.execute("INSERT INTO time VALUES({0})".format(currentTime))


# Get recently played tracks after the last db encounter.
recentlyPlayed = sp.current_user_recently_played(limit=50, after=sinceLast, before=None)['items']

time = datetime.datetime.now()

print("Tracking the following songs: \n")
for song in recentlyPlayed:
    name = song['track']['name']
    name = name.replace("'","")
    print(name)
    artist = song['track']['album']['artists'][0]['name']
    cursor.execute("INSERT INTO track (name, artist, timeperiod) VALUES('{0}','{1}','{2}')".format(name, artist, time))

# ensure information gets saved to db
connection.commit()
# close the db
connection.close()





