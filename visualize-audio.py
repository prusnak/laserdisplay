#!/usr/bin/env python

DEVICE = 'alsa_output.pci-0000_00_1b.0.analog-stereo.monitor'

import pygst
pygst.require("0.10")
import gst
import struct
import LaserDisplay

pipeline=gst.parse_launch('pulsesrc device=%s ! audio/x-raw-int ! appsink name=sink' % DEVICE)
sink = pipeline.get_by_name('sink')
pipeline.set_state(gst.STATE_PLAYING)

LD = LaserDisplay.create()

while True:
    try:
        buf = sink.emit('pull-buffer')
    except:
        print 'err'
        break
    raw = struct.unpack(str(len(buf)/2)+'h', buf)
    rawlen = len(raw)
    for i in range(0,256):
        LD.draw_point(i, 128+raw[int(rawlen/256.0*i)]/128 )
    LD.show_frame()
