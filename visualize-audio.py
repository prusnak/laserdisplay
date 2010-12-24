#!/usr/bin/env python

DEVICE = 'alsa_output.pci-0000_00_1b.0.analog-stereo.monitor'

import pygst
pygst.require("0.10")
import gst
import struct
import LaserDisplay

pipeline = gst.parse_launch('pulsesrc device=%s ! audio/x-raw-int ! appsink name=sink' % DEVICE)
sink = pipeline.get_by_name('sink')
pipeline.set_state(gst.STATE_PLAYING)

LD = LaserDisplay.create()

def setcolor(v):
    if ( abs(v-128) < 20 ):
        LD.set_color(LD.GREEN)
    elif ( abs(v-128) < 40 ):
        LD.set_color(LD.YELLOW)
    else:
        LD.set_color(LD.RED)

while True:
    try:
        buf = sink.emit('pull-buffer')
    except:
        print 'err'
        break
    raw = struct.unpack(str(len(buf)/2)+'h', buf)
    rawlen = len(raw)
    setcolor(128+raw[0]/128)
    LD.draw_point(0, 128+raw[0]/128, 0x03 )
    for i in range(1,255):
        setcolor(128+raw[int(rawlen/256.0*i)]/128)
        LD.draw_point(i, 128+raw[int(rawlen/256.0*i)]/128, 0x00 )
    setcolor(128+raw[rawlen-1]/128)
    LD.draw_point(255, 128+raw[rawlen-1]/128, 0x02 )
    LD.show_frame()
