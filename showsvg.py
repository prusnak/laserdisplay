#!/usr/bin/env python

import sys
import LaserDisplay
from LaserDisplay.SvgProcessor import SvgProcessor

if len(sys.argv) < 2:
    print 'Usage: showsvg filename.svg'
    sys.exit(1)

LD = LaserDisplay.create()

LD.set_scan_rate(30000)
LD.set_blanking_delay(0)

sp = SvgProcessor(LD)

while True:
    sp.parseFile(sys.argv[1])
    LD.show_frame()
