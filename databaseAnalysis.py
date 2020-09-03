import collections
import sqlite3

# CONNECT TO DATABASE
connection = sqlite3.connect('Trackify.db')
cursor = connection.cursor()

db = cursor.execute("SELECT * FROM track") # returns track information in a tupe (name, artist, timeperiod) *name = song name. timeperiod = timeperiod when song was inserted into database.


#                                               row[0] row[1]     row[2]        row[3]      row[4]
# Row is a tuple containing entry information: (Track, Artist, Track Duration, Played At, Release Date)

data = []
class Artist:
    def __init__(self, name, uri, song):
        self.name = name
        self.uri = uri
        self.songs = []
        self.songs.append(song)
        self.timesPlayed = 1


class Song:
    def __init__(self, name, released, duration, datePlayed, image):
        self.name = name
        self.released = released
        self.duration = duration
        self.timesPlayed = 1
        self.image = image
        self.datePlayed = []
        self.datePlayed.append(datePlayed)

for row in db:
    toAdd = True
    for x in data:
        if row[1] == x.name: 
            toAdd = False
            break

    # Add New Artist
    if(toAdd or len(data) <= 0):
        data.append(Artist(row[1], row[6], Song(row[0], row[4], row[2], row[3], row[5])))
    else: # Update Artist Information
        addedSong = False
        for x in data:
            if(x.name == row[1]): # if selected song is same as index
                # update info
                x.timesPlayed = x.timesPlayed + 1
                for y in x.songs:
                    if y.name == row[0]:
                        # print("Already Added %s" % (row[0]))
                        y.timesPlayed = y.timesPlayed + 1
                        y.datePlayed.append(row[3]) # add to datePlayed
                        addedSong = True
                if addedSong == False:
                    x.songs.append(Song(row[0], row[4], row[2], row[3], row[5]))

# CLOSE DATABASE
connection.close()

# Data Collection/Organize
countSongPlayedAmount = collections.Counter()
countArtistPlayedAmount = collections.Counter()
totalTimeSpentListening = 0

for artist in data:
    # Artist Information
    countArtistPlayedAmount[artist.name] = artist.timesPlayed 

    # Song Information
    for song in artist.songs:
        countSongPlayedAmount[song.name] += song.timesPlayed
        totalTimeSpentListening += (song.duration / 1000) / 60 # time in ms -> time in s


Top10Artists = countArtistPlayedAmount.most_common(10)
Top10Songs = countSongPlayedAmount.most_common(10)

Top10List = []
for x in Top10Artists:
    Top10List.append(x[0])

Top10 = []

for d in data:
    if d.name in Top10List:
        Top10.append(d)

def get_timesPlayed(artist):
    return artist.timesPlayed

data.sort(key=get_timesPlayed, reverse=True)
Top10.sort(key=get_timesPlayed, reverse=True)

