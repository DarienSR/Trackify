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
  pdf.line(30, 710, 560, 710) # Horizontal Line
  pdf.setFont(MAIN_FONT, 10) # update font
  text = pdf.beginText()

  y_pos = 690

  SetFont(pdf, MAIN_FONT, "You have listened to ", 40, y_pos)
  SetFont(pdf, BOLD_FONT, "%s " % (len(data)), 170, y_pos)
  SetFont(pdf, MAIN_FONT, "different artists ", 195, y_pos)

  y_pos = y_pos - 25
  SetFont(pdf, MAIN_FONT, "Total listening time: ", 40, y_pos)
  SetFont(pdf, BOLD_FONT, "%s " % (round(totalTimeSpentListening / 60, 0)), 170, y_pos) # minutes
  SetFont(pdf, MAIN_FONT, "hours ", 200, y_pos)
  
  y_pos = y_pos - 25
  SetFont(pdf, MAIN_FONT, "Top Artist: ", 40, y_pos)
  SetFont(pdf, BOLD_FONT, "%s" % (data[0].name), 120, y_pos)
  SetFont(pdf, MAIN_FONT, " | Played ", 250, y_pos)
  SetFont(pdf, BOLD_FONT, "%s " % (data[0].timesPlayed), 305, y_pos)
  SetFont(pdf, MAIN_FONT, "plays ", 325, y_pos)

  y_pos = y_pos - 25
  SetFont(pdf, MAIN_FONT, "Top Song: ", 40, y_pos)
  SetFont(pdf, BOLD_FONT, "%s" % (Top10Songs[0][0]), 120, y_pos)
  SetFont(pdf, MAIN_FONT, " | Played ", 250, y_pos)
  SetFont(pdf, BOLD_FONT, "%s " % (Top10Songs[0][1]), 305, y_pos)
  SetFont(pdf, MAIN_FONT, "plays ", 325, y_pos)

  
  pdf.line(30, 600, 560, 600) # Horizontal Line

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
    SetFont(pdf, MAIN_FONT, "%s." % (count), 40, y_pos)
    SetFont(pdf, BOLD_FONT, " %s" % (artist.name), 60, y_pos)
    SetFont(pdf, MAIN_FONT, " | Played ", 250, y_pos)
    SetFont(pdf, BOLD_FONT, " %s"  % (artist.timesPlayed), 305, y_pos)
    SetFont(pdf, MAIN_FONT, "time(s)\n\n", 325, y_pos)
    y_pos = y_pos - 15 # update position of the next artist on the page
    count = count + 1
  pdf.line(30, 390, 560, 390) # Horizontal Line

def DisplayTopTenSongs(pdf, Top10Songs):
  count = 1
  y_pos = 330
  for song in Top10Songs:
    SetFont(pdf, MAIN_FONT, "%s." % (count), 40, y_pos)
    SetFont(pdf, BOLD_FONT, " %s" % (song[0]), 60, y_pos)
    SetFont(pdf, MAIN_FONT, " | Played ", 250, y_pos)
    SetFont(pdf, BOLD_FONT, " %s"  % (song[1]), 305, y_pos)
    SetFont(pdf, MAIN_FONT, "time(s)\n\n", 325, y_pos)
    y_pos = y_pos - 15 # update position of the next artist on the page
    count = count + 1


