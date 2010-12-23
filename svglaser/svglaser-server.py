#!/usr/bin/env python

mess = None

from LaserDisplay import LaserDisplay

LD = LaserDisplay()

import threading

lock = threading.Lock()

import sys

import math

LD.set_scan_rate(40000)
LD.set_blanking_delay(0)

##### server

import BaseHTTPServer
import urllib

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_POST(self):
        if self.headers.has_key('content-length'):
            length= int( self.headers['content-length'] )
            content = self.rfile.read(length)
            svg = urllib.unquote_plus(content[4:])
            global lock, LD, mess
            lock.acquire()
            LD.show_frame()
            xml.sax.parseString(svg,SVGHandler())
            mess = LD.messageBuffer
            lock.release()
        self.send_response(200)
        self.end_headers()

server_address = ('', 8000)
httpd = BaseHTTPServer.HTTPServer(server_address, MyHandler)

print 'listening at 8000 ...'


def laser_loop():
    while True:
        global mess
        if not mess is None:
            global lock
            lock.acquire()
            LD.messageBuffer = mess
            LD.show_frame()
            lock.release()


try:
    t = threading.Thread(target = laser_loop)
    t.start()
    pass
except:
   print "Error: unable to start thread"

while True:
    httpd.handle_request()
