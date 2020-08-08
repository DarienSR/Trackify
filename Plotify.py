# Uses the Trackify database to plot recorded information.

import collections
import sqlite3
from graphs import *  # import our graphing file. Holds the different functions to create our graphs
from matplotlib.backends.backend_pdf import PdfPages
import datetime
# CONNECT TO DATABASE
connection = sqlite3.connect('Trackify.db')
cursor = connection.cursor()

db = cursor.execute("SELECT * FROM track") # returns track information in a tupe (name, artist, timeperiod) *name = song name. timeperiod = timeperiod when song was inserted into database.

# Data Collection/Organize
tracks = []
artists = []
for row in db:
    tracks.append(row[0])
    artists.append(row[1])

countSongPlayedAmount = collections.Counter()
countArtistPlayedAmount = collections.Counter()

for song in tracks:
    countSongPlayedAmount[song] += 1

for artist in artists:
    countArtistPlayedAmount[artist] += 1

Top3Artists = countArtistPlayedAmount.most_common(3)
Top3Songs = countSongPlayedAmount.most_common(3)

Top5Artists = countArtistPlayedAmount.most_common(5)
Top5Songs = countSongPlayedAmount.most_common(5)

Top10Artists = countArtistPlayedAmount.most_common(10)
Top10Songs = countSongPlayedAmount.most_common(10)




# CLOSE DATABASE
connection.close()

# CREATE THE PDF REPORT


pdfName = "TrackifyReport_%s.pdf" % (datetime.date.today()) # Append todays date to the pdf name

with PdfPages(pdfName) as pdf:
    # We are creating the plot/figure, which is being returned and saved to the pdf (each pdf.savefig saves it on its own page)
    pdf.savefig(HorizontalBar(Top3Songs, "Times Played", "Song", "Top 3 Most Listened to Songs", "#ac053e"), bbox_inches='tight')
    pdf.savefig(HorizontalBar(Top3Artists, "Times Played", "Artist", "Top 3 Artists", "#3498eb"), bbox_inches='tight') 

    pdf.savefig(HorizontalBar(Top5Songs, "Times Played", "Song", "Top 5 Most Listened to Songs", "#ac053e"), bbox_inches='tight')
    pdf.savefig(HorizontalBar(Top5Artists, "Times Played", "Artist", "Top 5 Artists", "#3498eb"), bbox_inches='tight') 

    pdf.savefig(HorizontalBar(Top10Songs, "Times Played", "Song", "Top 10 Most Listened to Songs", "#ac053e"), bbox_inches='tight')
    pdf.savefig(HorizontalBar(Top10Artists, "Times Played", "Artist", "Top 10 Artists", "#3498eb"), bbox_inches='tight') 