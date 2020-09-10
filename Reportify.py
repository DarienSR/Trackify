import datetime
# Helper functions that interact with reportlab to aid in the creation of the pdf
MAIN_FONT = "Courier"
BOLD_FONT = "Courier-Bold"
DEFAULT_FONT_SIZE = 10

def Header(pdf):
  # Title on the page
  pdf.setFont('Courier-Bold', 36)
  pdf.drawCentredString(300, 770, "Trackify Report")

  # Set Date below title
  datex = "%s" % (datetime.date.today())
  pdf.setFont(MAIN_FONT, 20) # update font
  pdf.drawCentredString(300, 730, datex)

def SetFont(pdf, font, string, x, y, font_size = DEFAULT_FONT_SIZE):
  pdf.setFont(font, font_size)
  text = string
  DrawText(pdf, text, x, y)

def QuickStats(pdf, data, totalTimeSpentListening, Top10Songs):
  # Left of the page, display quick stats.
  pdf.line(0, 710, 600, 710) # Horizontal Line
  pdf.setFont(MAIN_FONT, 10) # update font
  text = pdf.beginText()

  y_pos = 690
  
  SetFont(pdf, MAIN_FONT, "You have listened to ", 10, y_pos)
  SetFont(pdf, BOLD_FONT, "%s " % (len(data)), 140, y_pos)
  SetFont(pdf, MAIN_FONT, "different artists ", 165, y_pos)

  y_pos = y_pos - 25
  SetFont(pdf, MAIN_FONT, "Total listening time: ", 10, y_pos)
  SetFont(pdf, BOLD_FONT, "%s " % (round(totalTimeSpentListening / 60, 0)), 140, y_pos) # minutes
  SetFont(pdf, MAIN_FONT, "hours ", 170, y_pos)
  
  y_pos = y_pos - 25
  SetFont(pdf, MAIN_FONT, "Top Artist: ", 10, y_pos)
  SetFont(pdf, BOLD_FONT, "%s" % (data[0].name), 90, y_pos)
  SetFont(pdf, MAIN_FONT, " | Played ", 200, y_pos)
  SetFont(pdf, BOLD_FONT, "%s " % (data[0].timesPlayed), 275, y_pos)
  SetFont(pdf, MAIN_FONT, "plays ", 295, y_pos)

  y_pos = y_pos - 25
  SetFont(pdf, MAIN_FONT, "Top Song: ", 10, y_pos)
  SetFont(pdf, BOLD_FONT, "%s" % (Top10Songs[0][0]), 90, y_pos)
  SetFont(pdf, MAIN_FONT, " | Played ", 200, y_pos)
  SetFont(pdf, BOLD_FONT, "%s " % (Top10Songs[0][1]), 275, y_pos)
  SetFont(pdf, MAIN_FONT, "plays ", 295, y_pos)

  
  pdf.line(0, 600, 710, 600) # Horizontal Line

def SubHeader(pdf, text, font_size, x, y):
  pdf.setFont("Courier-Bold", font_size) # update font
  pdf.drawString(x, y, text)
  pdf.setFont(MAIN_FONT, 10)

def DrawText(pdf, string, x, y):
  text = pdf.beginText()
  text.setTextOrigin(x, y)
  text.textLines(string)
  pdf.drawText(text)

def DisplayTopTenArtists(pdf, data):
  count = 1 # count is position of artist in top
  y_pos = 535 # of artist displayed on pdf in top 10 section

  for artist in data[0:10]:
    SetFont(pdf, MAIN_FONT, "%s." % (count), 10, y_pos)
    SetFont(pdf, BOLD_FONT, " %s" % (artist.name), 30, y_pos)
    SetFont(pdf, MAIN_FONT, " | Played ", 220, y_pos)
    SetFont(pdf, BOLD_FONT, " %s"  % (artist.timesPlayed), 275, y_pos)
    SetFont(pdf, MAIN_FONT, "time(s)\n\n", 295, y_pos)
    y_pos = y_pos - 15 # update position of the next artist on the page
    count = count + 1
  pdf.line(0, 340, 710, 340) # Horizontal Line

def DisplayTopTenSongs(pdf, Top10Songs):
  count = 1
  y_pos = 250
  for song in Top10Songs:
    SetFont(pdf, MAIN_FONT, "%s." % (count), 10, y_pos)
    SetFont(pdf, BOLD_FONT, " %s" % (song[0]), 30, y_pos)
    SetFont(pdf, MAIN_FONT, " | Played ", 220, y_pos)
    SetFont(pdf, BOLD_FONT, " %s"  % (song[1]), 275, y_pos)
    SetFont(pdf, MAIN_FONT, "time(s)\n\n", 295, y_pos)
    y_pos = y_pos - 15 # update position of the next artist on the page
    count = count + 1


