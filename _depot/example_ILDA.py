#!/usr/bin/env python
# display ILDA animations from a given file

from LaserDisplay import *
import ILDA

#LD = LaserDisplay()
LD = LaserDisplay({"server":"localhost","port": 50000})
LD.set_scan_rate(37000)
LD.set_blanking_delay(0)


WIDTH=200
HEIGHT=200
import sys
import random
ilda_file = open(sys.argv[1], 'rb')
ilda_frames = ILDA.readFrames(ilda_file)

frames = []
for f in ilda_frames:
  frame = []
  for p in f.iterPoints():
    frame.append([WIDTH/2 + (WIDTH/2)*p.x, HEIGHT/2 + (HEIGHT/2)*p.y])
  frames.append(frame)
ilda_file.close()

LD.set_color(YELLOW)

for frame in frames:
  for _ in range(2):
    for point in frame:
        #LD.set_color(p.color)
      if random.random()<=0.5:
        LD.draw_point(point[0], point[1])
m = LD.messageBuffer

while True:
  LD.messageBuffer = m
  LD.show_frame()

