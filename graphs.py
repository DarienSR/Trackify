import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg
import urllib.request

# xAxis is going to be your object (i.e song name)
# yAxis is going to your comparison (i.e. number of times played)
def HorizontalBar(data, xLabel, yLabel, title, graphColor, fileName):
  # data in the form of a tuple (artist, value) or (song, value)
  xAxis = []
  for obj in data:
    xAxis.append(obj[0]) # appending in the object (i.e. artist or song)

  yAxis = []
  for obj in data:
    yAxis.append(obj[1]) # appending in the value (i.e times played)

  plt.rcdefaults() # restore styling
  fig, ax = plt.subplots()

  
  # data
  y_pos = np.arange(len(xAxis))
  barLength = yAxis # y = amount of times song/artist has been played
  error = np.random.rand(len(xAxis))
  bar = ax.barh(y_pos, barLength, xerr=error, align='center', color=graphColor)
  ax.set_yticks(y_pos)
  ax.set_yticklabels(xAxis)
  ax.set_xlabel(xLabel)
  ax.set_ylabel(yLabel)
  ax.set_title(title)
  ax.invert_yaxis() # largest data set on the top of the graph

  # Label Bar Graphs with their values.
  count = 0
 
  for x in bar:
    width = x.get_width()
    # (x, y, text) x,y being the position of the text.
    ax.text(width / 2 , count + 0.4,
            str(round(width, 2)), # round float 
            ha='center', va='bottom',
            fontweight = 'extra bold',
          )
    count = count + 1
  fig = plt.gcf()
  fig.set_size_inches(2, 2) # 20 x 20 pixels
  fig.savefig(fileName, bbox_inches='tight', dpi=100)
  plt.close()
  return fig

def CreateImage(image, fileName):
  urllib.request.urlretrieve(image, fileName)

def BarChart(filename, data, colors, indexed=False, edgecolor="black",):
  labels = []
  values = [] # height

  if indexed == True:
    for x in data:
      labels.append(x[0]) # name of artist/song
      values.append(x[1]) # times played
  else:
    for x in data:
      labels.append(x.name) # name of artist/song
      values.append(x.timesPlayed) # times played
  
  fig, ax1 = plt.subplots()
  bars = plt.bar(labels, values, width=0.8, edgecolor=edgecolor)
  idx = 0
  for bar in bars:
    bar.set_color(colors[idx].hex)
    idx = idx + 1

  plt.xticks(rotation=90)
  fig = plt.gcf()
  fig.savefig(filename, bbox_inches='tight', dpi=100)  
  
def PieChart(data, filename, colors, radius = 1):
  labels = []
  values = []
  for x in data:
    labels.append(x[0]) # name of artist/song
    values.append(x[1]) # times played

  fig, ax1 = plt.subplots()
  plt.rcParams['axes.labelweight'] = 'bold'
  plt.rcParams['lines.linewidth'] = 2
  plt.rcParams['patch.edgecolor'] = 'black'
  pie = plt.pie(values, labels=labels, autopct="%.1f%%", colors=colors , radius=radius)


  fig = plt.gcf()
  fig.savefig(filename, bbox_inches='tight', dpi=100)
  plt.close()
  
