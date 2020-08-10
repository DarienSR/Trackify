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
countSongPlayedAmount = collections.Counter()
timeSpentListeningToSong = collections.Counter()

countArtistPlayedAmount = collections.Counter()
timeSpentListeningToArtist = collections.Counter()

totalTimeSpentListening = 0
#                                               row[0] row[1]     row[2]        row[3]      row[4]
# Row is a tuple containing entry information: (Track, Artist, Track Duration, Played At, Release Date)

for row in db:
    countArtistPlayedAmount[row[1]] += 1 
    countSongPlayedAmount[row[0]] += 1
    totalTimeSpentListening += ((row[2] / 1000) / 60) # length of song is stored in ms. We convert to seconds, than minutes.
    timeSpentListeningToArtist[row[1]] += ((row[2] / 1000) / 60)
    timeSpentListeningToSong[row[0]] += ((row[2] / 1000) / 60)
    


Top10Artists = countArtistPlayedAmount.most_common(10)
Time10Artists = timeSpentListeningToArtist.most_common(10)
Top10Songs = countSongPlayedAmount.most_common(10)
Time10Songs = timeSpentListeningToSong.most_common(10)


# CLOSE DATABASE
connection.close()

# CREATE THE PDF REPORT


pdfName = "TestTrackifyReport_%s.pdf" % (datetime.date.today()) # Append todays date to the pdf name

with PdfPages(pdfName) as pdf:

    firstPage = plt.figure(figsize=(11.69,8.27))
    firstPage.clf()
    txt = "Trackify Report\n {}\n\n Quick Overview:\n Total Time Spent Listening to Music: {:.2f}\n Favorite Song: {}\n Favorite Artist: {}".format(datetime.date.today(), totalTimeSpentListening, Top10Songs[0][0], Top10Artists[0][0]) 
    firstPage.text(0.5,0.5,txt, transform=firstPage.transFigure, size=24, ha="center")
    pdf.savefig()
    plt.close()

    # We are creating the plot/figure, which is being returned and saved to the pdf (each pdf.savefig saves it on its own page)
    # We are using our top 10 to generate the top 5 and 3.
    pdf.savefig(HorizontalBar(Top10Songs[:3], "Times Played", "Song", "Top 3 Most Listened to Songs", "#ac053e"), bbox_inches='tight')
    pdf.savefig(HorizontalBar(Top10Artists[:3], "Times Played", "Artist", "Top 3 Artists", "#3498eb"), bbox_inches='tight') 
    pdf.savefig(HorizontalBar(Time10Songs[:3], "Time Listened (Minutes)", "Song", "Time Spent Listening to Top 3 Songs", "#3498eb"), bbox_inches='tight') 
    pdf.savefig(HorizontalBar(Time10Artists[:3], "Time Listened (Minutes)", "Artist", "Time Spent Listening to Top 3 Artist", "#42f57e"), bbox_inches='tight') 

    pdf.savefig(HorizontalBar(Top10Songs[:5], "Times Played", "Song", "Top 5 Most Listened to Songs", "#ac053e"), bbox_inches='tight')
    pdf.savefig(HorizontalBar(Top10Artists[:5], "Times Played", "Artist", "Top 5 Artists", "#3498eb"), bbox_inches='tight') 
    pdf.savefig(HorizontalBar(Time10Songs[:5], "Time Listened (Minutes)", "Song", "Time Spent Listening to Top 5 Songs", "#3498eb"), bbox_inches='tight') 
    pdf.savefig(HorizontalBar(Time10Artists[:5], "Time Listened (Minutes)", "Artist", "Time Spent Listening to Top 5 Artist", "#42f57e"), bbox_inches='tight') 

    pdf.savefig(HorizontalBar(Top10Songs, "Times Played", "Song", "Top 10 Most Listened to Songs", "#ac053e"), bbox_inches='tight')
    pdf.savefig(HorizontalBar(Top10Artists, "Times Played", "Artist", "Top 10 Artists", "#3498eb"), bbox_inches='tight') 
    pdf.savefig(HorizontalBar(Time10Songs, "Time Listened (Minutes)", "Song", "Time Spent Listening to Top 10 Songs", "#3498eb"), bbox_inches='tight') 
    pdf.savefig(HorizontalBar(Time10Artists, "Time Listened (Minutes)", "Artist", "Time Spent Listening to Top 10 Artist", "#42f57e"), bbox_inches='tight') 