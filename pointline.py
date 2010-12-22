#!/usr/bin/env python

import LaserDisplay

LD = LaserDisplay.create()
LD.set_scan_rate(35000)

y=0
while True:
    y += 1
    if y > 255: y = 0
    LD.draw_point(128-10, y)
    LD.draw_line(128+10, 0, 128+10, y)
    LD.show_frame()
