#!/usr/bin/env python

import LaserDisplay
import math
from random import random

LD = LaserDisplay.create()

LD.set_scan_rate(30000)
LD.set_blanking_delay(0)

def draw_cube(LD, a, b, mode):
    i = 0
    col = [LD.WHITE, LD.RED, LD.GREEN, LD.BLUE, LD.CYAN, LD.MAGENTA, LD.YELLOW, LD.WHITE]
    for x in [-1,1]:
        for y in [-1,1]:
            for z in [-1,1]:
                u = x * math.cos(a) - y * math.sin(a)
                v = x * math.sin(a) + y * math.cos(a)
                w = z
                u2 = u
                v2 = v * math.cos(b) - w * math.sin(b)
                w2 = v * math.sin(b) + w * math.cos(b)
                u,v,w = u2,v2,w2
                cx = 128 + u * (w + 2) * 25
                cy  = 128 + v * (w + 2) * 25
                r = (w + 2) * 4
                LD.set_color(col[i])
                if mode == 0:
                    LD.draw_ellipse(cx, cy, r, r)
                if mode == 1:
                    LD.draw_rect(cx-r, cy-r, r*2, r*2)
                i += 1

a = b = 0
da = db = 0.001
mode = 0
while True:
    draw_cube(LD, a, b, mode)
    a += da
    b += db
    if random() > 0.9999: da = -da
    if random() > 0.9999: db = -db
    if random() > 0.9999: mode = (mode+1)%2
    LD.show_frame()
