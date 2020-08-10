import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

# xAxis is going to be your object (i.e song name)
# yAxis is going to your comparison (i.e. number of times played)
def HorizontalBar(data, xLabel, yLabel, title, graphColor):
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
    ax.text(width / 2 , count + 0.1,
            str(round(width, 2)), # round float 
            ha='center', va='bottom',
            fontweight = 'extra bold'
          )
    count = count + 1
  plt.close()
  return fig

