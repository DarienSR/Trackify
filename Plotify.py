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

# Generate The Different Plots/Images
HorizontalBar(Top10Artists, "Times Played", "Artist", "Top 10 Most Listened to Artist", "#02e840", "./Images/Top10Artists.png")
HorizontalBar(Top10Songs, "Times Played", "Song", "Top 10 Most Listened to Songs", "#02e840", "./Images/Top10Songs.png")


# TO DO: Get Additional Spotify Information.


# CREATE THE PDF REPORT
from reportlab.pdfgen import canvas

pdfName = "TrackifyReport_%s.pdf" % (datetime.date.today()) # Append todays date to the pdf name
pdf = canvas.Canvas(pdfName)

pdf.setTitle(pdfName) # Title of PDF in title bar

MAIN_FONT = "Courier-Bold"

# Title on the page
pdf.setFont('Courier-Bold', 36)
pdf.drawCentredString(300, 770, "Trackify Report")

# Set Date below title
datex = "%s" % (datetime.date.today())
pdf.setFont(MAIN_FONT, 20) # update font
pdf.drawCentredString(300, 720, datex)

# Left of the page, display quick stats.
pdf.line(30, 710, 560, 710) # Horizontal Line
pdf.setFont(MAIN_FONT, 10) # update font
text = pdf.beginText()
text.setTextOrigin(40, 675)
text.textLines(""" 
Total Listening Time: %s minutes | %s hours\n
Top Artist: %s | Played %s time(s)\n
Top Song: %s | Played %s time(s)\n
""" % (round(totalTimeSpentListening, 2), round(totalTimeSpentListening / 60), Top10Artists[0][0], Top10Artists[0][1], Top10Songs[0][0], Top10Songs[0][1]))
pdf.drawText(text)

pdf.line(30, 600, 560, 600) # Horizontal Line

# Sub Header Top 10 Artists 
text = "Top 10 Artists"
pdf.setFont(MAIN_FONT, 18) # update font
pdf.drawString(40, 560, text)

pdf.setFont(MAIN_FONT, 10) # update font again

string = ""
count = 1
for artist in Top10Artists:
    string += "%s. %s | Played %s time(s)\n\n" % (count, artist[0], artist[1])
    count = count + 1
print(string)
text = pdf.beginText()
text.setTextOrigin(40, 535)
text.textLines(string)
pdf.drawText(text)

pdf.line(30, 290, 560, 290) # Horizontal Line

# Sub Header Top 10 Songs 
text = "Top 10 Songs"
pdf.setFont(MAIN_FONT, 18) # update font
pdf.drawString(40, 265, text)

pdf.setFont(MAIN_FONT, 10) # update font again


string = ""
count = 1
for song in Top10Songs:
    string += "%s. %s | Played %s time(s)\n\n" % (count, song[0], song[1])
    count = count + 1
print(string)
text = pdf.beginText()
text.setTextOrigin(40, 240)
text.textLines(string)
pdf.drawText(text)



pdf.save()