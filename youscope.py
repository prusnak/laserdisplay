#!/usr/bin/env python
#
# Youscope Emulator (adapted to render on a laser show LD)
#
#(c)2010,2007 Felipe Sanches <juca@members.fsf.org>
#(c)2007 Leandro Lameiro <lameiro@gmail.com>
#licensed under GNU GPL v3 or later

import wave
import struct
import sys
import LaserDisplay

FPS = 25

try:
    wro = wave.open('youscope-wave.wav')
except:
    print '\nPlease download youscope-wave.wav:\n'
    print 'wget http://mirror.kapsi.fi/koodaa.mine.nu/tvt/youscope-wave.wav'
    sys.exit(1)

READ_LENGTH = wro.getframerate()/FPS

for _ in range(250):
   frames = wro.readframes(READ_LENGTH)

LD = LaserDisplay.create()
LD.set_scan_rate(45000)
LD.set_blanking_delay(0)
LD.set_color(LD.WHITE)

while True:
    frames = wro.readframes(READ_LENGTH)
    for i in range(0,READ_LENGTH,4):
        r = struct.unpack('hh', frames[i:i+4])
        x = int(r[1]*LD.SIZE/65536) + LD.SIZE/2
        y = int(-r[0]*LD.SIZE/65536) + LD.SIZE/2
        LD.draw_point(x,y)
        i += 4
    LD.show_frame()
