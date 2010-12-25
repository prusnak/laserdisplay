#!/usr/bin/env python

DEVICE = 'alsa_output.pci-0000_00_1b.0.analog-stereo.monitor'

import pygst
pygst.require("0.10")
import gst
import struct
import numpy.fft
import LaserDisplay

pipeline = gst.parse_launch('pulsesrc device=%s ! audio/x-raw-int ! appsink name=sink' % DEVICE)
sink = pipeline.get_by_name('sink')
pipeline.set_state(gst.STATE_PLAYING)

LD = LaserDisplay.create()

def setcolor(v):
    if v < 60:
        LD.set_color(LD.GREEN)
    elif v < 120:
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
    raw = numpy.log( numpy.abs(numpy.fft.fft(raw))**2 )

    idx = 0
    for i in range(0, 16):
        val = 0
        steps = int(round((1.20**i)*4))
        for _ in range(steps):
            val += raw[idx]
            idx += 1
        try:
            val = int( 1.5*numpy.exp(val/steps/6) )
        except:
            val = 1
        setcolor(val)
        LD.draw_rect(i*16+3, 255-val, 10, val)

    LD.show_frame()
