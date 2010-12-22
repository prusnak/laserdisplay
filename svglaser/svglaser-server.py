#!/usr/bin/env python

mess = None

from LaserDisplay import LaserDisplay

LD = LaserDisplay()

import xml
from xml.sax.handler import ContentHandler
import threading

lock = threading.Lock()

import sys

import math

class SVGHandler(xml.sax.handler.ContentHandler):
  def startElement(self, name, attrs):
    global LD
    if name=="path":
      tokens = attrs.get('d').replace('m','  m ').replace('c',' c ').replace('l',' l ').replace('h',' h ').replace('v',' v ').replace('z',' z ').replace('  ',' ').strip().split(" ")
      color = attrs.get('stroke')
      LD.set_color(color)
      i=0
      x,y=0,0
      x0,y0=x,y
      cmd = None
      while i<len(tokens):
        if tokens[i].lower() in ["m", "c", "l", "h", "v", "z"]:
          cmd = tokens[i]
          i+=1
        if cmd=="m":
          delta=tokens[i].split(",")
          x+=float(delta[0])/595*255
          y+=float(delta[1])/595*255
          x0,y0=x,y
          cmd="l"
        elif cmd=="M":
          delta=tokens[i].split(",")
          x=float(delta[0])/595*255
          y=float(delta[1])/595*255
          x0,y0=x,y
          cmd="l"
        elif cmd=="l":
          delta=tokens[i].split(",")
          LD.draw_line(x,y,x+float(delta[0])/595*255,y+float(delta[1])/595*255)
          x+=float(delta[0])/595*255
          y+=float(delta[1])/595*255
        elif cmd=="L":
          delta=tokens[i].split(",")
          LD.draw_line(x,y,float(delta[0]/595*255),float(delta[1]/595*255))
          x=float(delta[0]/595*255)
          y=float(delta[1]/595*255)
        elif cmd=="z" or cmd=="Z":
          i-=1
          LD.draw_line(x,y,x0,y0)
          x,y=x0,y0
        elif cmd=="h":
          delta=tokens[i]
          LD.draw_line(x,y,x+float(delta)/595*255,y)
          x+=delta/595*255
        elif cmd=="H":
          delta=tokens[i]
          LD.draw_line(x,y,float(delta)/595*255,y)
          x=delta/595*255
        elif cmd=="v":
          delta=tokens[i]
          LD.draw_line(x,y,x,y+float(delta)/595*255)
          y+=delta/595*255
        elif cmd=="V":
          delta=tokens[i]
          LD.draw_line(x,y,x,float(delta)/595*255)
          y=delta/595*255
        elif cmd=="c":
          ctrl1=tokens[i].split(",")
          ctrl2=tokens[i+1].split(",")
          delta=tokens[i+2].split(",")
          LD.draw_cubic_bezier([[x,y],[x+float(ctrl1[0])/595*255,y+float(ctrl1[1])/595*255],[x+float(ctrl2[0])/595*255,y+float(ctrl2[1])/595*255],[x+float(delta[0])/595*255,y+float(delta[1])/595*255]],15)
          x+=float(delta[0])/595*255
          y+=float(delta[1])/595*255
          i+=2
        elif cmd=="C":
          ctrl1=tokens[i].split(",")
          ctrl2=tokens[i+1].split(",")
          delta=tokens[i+2].split(",")
          LD.draw_cubic_bezier([[x,y],[float(ctrl1[0])/595*255,float(ctrl1[1])/595*255],[float(ctrl2[0])/595*255,float(ctrl2[1])/595*255],[float(delta[0])/595*255,float(delta[1])/595*255]],15)
          x+=float(delta[0])/595*255
          y+=float(delta[1])/595*255
          i+=2
        i+=1

    if name=='ellipse':
        cx = float(attrs.get('cx'))/595*255
        cy = float(attrs.get('cy'))/599*255
        rx = float(attrs.get('rx'))/599*255
        ry = float(attrs.get('ry'))/599*255
        color = attrs.get('stroke')
        LD.set_color(color)
        for i in range(0,32):
            LD.draw_line(cx+rx*math.cos(2*math.pi/32*i),cy+ry*math.sin(2*math.pi/32*i),cx+rx*math.cos(2*math.pi/32*(i+1)),cy+ry*math.sin(2*math.pi/32*(i+1)))

    if name=='rect':
        x = float(attrs.get('x'))/595*255
        y = float(attrs.get('y'))/595*255
        w = float(attrs.get('width'))/595*255
        h = float(attrs.get('height'))/595*255
        color = attrs.get('stroke')
        LD.set_color(color)
        LD.draw_line(x,y,x+w,y)
        LD.draw_line(x+w,y,x+w,y+h)
        LD.draw_line(x+w,y+h,x,y+h)
        LD.draw_line(x,y+h,x,y)

    if name=='polyline':
        points = attrs.get('points').split(' ')
        color = attrs.get('stroke')
        LD.set_color(color)
        for i in range( len(points)-1 ):
            (x1,y1) = points[i].split(',')
            (x2,y2) = points[i+1].split(',')
            LD.draw_line(float(x1)/595*255,float(y1)/595*255,float(x2)/595*255,float(y2)/595*255)

    if name=='line':
        x1 = float(attrs.get('x1'))/595*255
        y1 = float(attrs.get('y1'))/595*255
        x2 = float(attrs.get('x2'))/595*255
        y2 = float(attrs.get('y2'))/595*255
        color = attrs.get('stroke')
        LD.set_color(color)
        LD.draw_line(x1,y1,x2,y2)


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
