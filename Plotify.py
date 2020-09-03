from graphs import *  # import our graphing file. Holds the different functions to create our graphs
from matplotlib.backends.backend_pdf import PdfPages
import datetime
from databaseAnalysis import *
from reportlab.pdfgen import canvas
from collections import Counter

# GENERATE THE IMAGES/PLOTS USED FOR THE REPORT
# Generate The Different Plots/Images
HorizontalBar(Top10Artists, "Times Played", "Artist", "Top 10 Most Listened to Artist", "#02e840", "./Images/Top10Artists.png")
HorizontalBar(Top10Songs, "Times Played", "Song", "Top 10 Most Listened to Songs", "#02e840", "./Images/Top10Songs.png")

# Connec to Spotify API
from authentication import sp
# Get Top 50 Artist Information
count = 0
uris = []
while count < 50 or count > len(data):
    uris.append(data[count].uri)
    count = count + 1
print()
API_INFO = sp.artists(uris)

# GET Top 3 Artist Images
CreateImage(API_INFO['artists'][0]['images'][2]['url'], "./Images/top1Artist.png")
CreateImage(API_INFO['artists'][1]['images'][2]['url'], "./Images/top2Artist.png")
CreateImage(API_INFO['artists'][2]['images'][2]['url'], "./Images/top3Artist.png")

# Get Top 3 Song Images
CreateImage(Top10[0].songs[0].image, "./Images/top1Song.png")
CreateImage(Top10[1].songs[0].image, "./Images/top2Song.png")
CreateImage(Top10[2].songs[0].image, "./Images/top3Song.png")

# CREATE THE PDF REPORT
import Reportify as Report
pdfName = "TrackifyReport_%s.pdf" % (datetime.date.today()) # Append todays date to the pdf name
pdf = canvas.Canvas(pdfName)
pdf.setTitle(pdfName) # Title of PDF in title bar

MAIN_FONT = "Courier"
BOLD_FONT = "Courier-Bold"


# Create Header. Trackify Report and the Date
Report.Header(pdf)

# Create Quick Stats.
Report.QuickStats(pdf, data, totalTimeSpentListening, Top10Songs)

# Create Header for Top 10 Artists.
Report.SubHeader(pdf, "Top 10 Artists", 18, 40, 560)
pdf.setFont(MAIN_FONT, 10) # update font again

# Top 10 Artists
Report.DisplayTopTenArtists(pdf, data)

# Sub Header Top 10 Songs 
Report.SubHeader(pdf, "Top 10 Songs", 18, 40, 350)
pdf.setFont(MAIN_FONT, 10) # update font again

# Top 10 Songs
Report.DisplayTopTenSongs(pdf, Top10Songs)

pdf.showPage() # creates a new page.

# Pages with breakdown the top 3 artists. Showing top 5 songs played from said artist. Total time listened to said artist, artist origin, etc.
count = 0

# --------------------
# -    TOP 3 START   -
# --------------------
for artist in Top10[:3]:
    # Name and Artist Picture
    pdf.setFont(MAIN_FONT, 20) # update font
    text = "%s" % (artist.name)
    pdf.drawString(130, 775, text)
    pdf.drawInlineImage("./Images/top%sArtist.png" % (count + 1), 40, 750, 60, 60) # x, y, height, width


    total = 0

    y_pos = 720
    Report.SetFont(pdf, MAIN_FONT, "Listened to ", 40, y_pos, 12)
    Report.SetFont(pdf, BOLD_FONT, "%s %s " % (artist.name, artist.timesPlayed), 125, y_pos)
    Report.SetFont(pdf, MAIN_FONT, "times ", 225, y_pos)

    y_pos = y_pos - 15
    Report.SetFont(pdf, MAIN_FONT, "Listened to ", 40, y_pos)
    Report.SetFont(pdf, BOLD_FONT, "%s " % (len(artist.songs)), 110, y_pos)
    Report.SetFont(pdf, MAIN_FONT, "different songs by ", 125, y_pos)
    Report.SetFont(pdf, BOLD_FONT, "%s " % (artist.name), 240, y_pos)

    y_pos = y_pos - 15
    Report.SetFont(pdf, MAIN_FONT, "Spotify Popularity: ", 40, y_pos)
    Report.SetFont(pdf, BOLD_FONT, "%s " % (API_INFO['artists'][count]['popularity']), 160, y_pos)

    y_pos = y_pos - 15
    Report.SetFont(pdf, MAIN_FONT, "Number of followers on Spotify: ", 40, y_pos)
    Report.SetFont(pdf, BOLD_FONT, "%s " % (API_INFO['artists'][count]['followers']['total']), 235, y_pos)

    # Display the genres of the artist
    y_pos = y_pos - 15
    Report.SetFont(pdf, MAIN_FONT, "Genres: ", 40, y_pos)
    string = ""
    for genre in API_INFO['artists'][count]['genres']:
        string += genre + ", "
    Report.SetFont(pdf, BOLD_FONT, string, 90, y_pos)

    # Move on to the next artist
    count = count + 1

    # SONG INFORMATION
    # Setup the table

    Report.SubHeader(pdf, "Song", 14, 20, 600)
    Report.SubHeader(pdf, "Times Played", 14, 250, 600)
    Report.SubHeader(pdf, "Listening Time", 14, 400, 600)

    y = 580
    for song in artist.songs:
        Report.DrawText(pdf, song.name, 20, y)
        Report.DrawText(pdf, str(song.timesPlayed), 250, y)
        Report.DrawText(pdf, str(round(((song.duration / 1000) / 60) * song.timesPlayed, 0)) + " minutes", 400, y)
        # calc total listening time per artist
        total += (song.duration / 1000) * song.timesPlayed
        y = y - 12 
    

    # This gets drawn ABOVE the listed songs. We just have to calculate total time listening here.
    Report.SetFont(pdf, MAIN_FONT, "Total time listened to ", 40, 645)
    Report.SetFont(pdf, BOLD_FONT, "%s: %s " % (artist.name, round(total / 60, 0)), 175, 645)
    Report.SetFont(pdf, MAIN_FONT, "minutes ", 300, 645)
    
    pdf.showPage() # Start another page for the next arits tin the top 3

# --------------------
# -   TOP 3 FINISH   -
# --------------------    

# Third Page with some misc stats, like origin of artists. Top genres. Release dates of music
# This information will be based off of Top 50 artists played. So it is not totally inclusive. For example, if it says you've listened
# to the genre Pop for 15 hours. That is the genre of Pop for 15hrs from artists within your Top 50.

# PAGE TITLE TOP 50 STATS AT A GLANCE.

pdf.showPage() # creates a new page

genres = []
# Calculate occurence of all genres
for artist in API_INFO['artists']:
    for genre in artist['genres']:
        genres.append(genre)


genres = Counter(genres)

pdf.save()
