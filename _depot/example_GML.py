#!/usr/bin/env python
import PyGML
#import urllib
from datetime import datetime
from LaserDisplay import *
import random
import sys

def readFile():
    #gmlFile = urllib.urlopen('http://000000book.com/data/154.gml')
    gmlFile = open(sys.argv[1], 'r')
    gml = PyGML.GML(gmlFile)
    gmlFile.close()
    return gml

TOTAL_TIME=float(sys.argv[2])
TIME_STRETCH = 1
ZOOM=1.0
DELTA = 1

DEGRADATION = 0.40
#DEGRADATION is the percentage of points that we ignore in order to render
# faster in the laser display. Unfortunately we are not able to render too
# complex content in our display without resulting in a lot of blinking.

gml = readFile()
LD = LaserDisplay({"server":"localhost","port": 50000})
#LD = LaserDisplay()
LD.set_scan_rate(35000)
LD.set_blanking_delay(0)
LD.set_color(RED)

t0=datetime.now()
num_frame=0
while True:
  delta = datetime.now() - t0
  t = delta.seconds + delta.microseconds/1000000.0
  t = float(t)/TIME_STRETCH

  if t > TOTAL_TIME:
    t0=datetime.now()

  num_frame+=1
  print num_frame, t
  for stroke in gml.iterStrokes():
      first=True
      for point in stroke.iterPoints():
          if point.time <= t and t <= point.time+DELTA and random.random()<(1-DEGRADATION):
            if first:
              first=False
            else:
#             LD.draw_point(WIDTH/2 + ZOOM*point.x*WIDTH/2, HEIGHT/2 + ZOOM*point.y*HEIGHT/2)
              LD.draw_line(WIDTH/2 + ZOOM*p.x*WIDTH/2, HEIGHT/2 + ZOOM*p.y*HEIGHT/2, WIDTH/2 + ZOOM*point.x*WIDTH/2, HEIGHT/2 + ZOOM*point.y*HEIGHT/2)
            p = point
  LD.show_frame()

