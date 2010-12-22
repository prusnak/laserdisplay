#!/usr/bin/env python

import LaserDisplay
import math
import time

LD = LaserDisplay.create()

LD.set_scan_rate(30000)
LD.set_blanking_delay(0)

while True:
    t = time.localtime()

    hours = t.tm_hour % 12
    minutes = t.tm_min
    seconds = t.tm_sec

    LD.set_color(LD.RED)
    LD.draw_text("%02i:%02i:%02i"%(hours,minutes,seconds), 5, 5, 20)

    angle = 2*math.pi*seconds/60 + 3*math.pi/2
    r = 2.0/3 * (LD.SIZE/2)
    LD.set_color(LD.GREEN)
    LD.draw_line(LD.SIZE/2, LD.SIZE/2, LD.SIZE/2 + r*math.cos(angle), LD.SIZE/2 + r*math.sin(angle))

    angle = 2*math.pi*minutes/60 + 2*math.pi/60 * float(seconds)/60 + 3*math.pi/2
    LD.set_color(LD.BLUE)
    LD.draw_line(LD.SIZE/2, LD.SIZE/2, LD.SIZE/2 + r*math.cos(angle), LD.SIZE/2 + r*math.sin(angle))

    angle = 2*math.pi*hours/12 + 2*math.pi*minutes/(60*12) + 3*math.pi/2
    r *= 2.0/3
    LD.draw_line(LD.SIZE/2, LD.SIZE/2, LD.SIZE/2 + r*math.cos(angle), LD.SIZE/2 + r*math.sin(angle))

    r1 = 2.0/3 * (LD.SIZE/2)
    r2 = 1.9/3 * (LD.SIZE/2)

    LD.set_color(LD.WHITE)
    for i in range(12):
        angle = i * 2*math.pi/12
        LD.draw_line(LD.SIZE/2 + r1*math.cos(angle), LD.SIZE/2 + r1*math.sin(angle), LD.SIZE/2 + r2*math.cos(angle), LD.SIZE/2 + r2*math.sin(angle))

    LD.show_frame()
