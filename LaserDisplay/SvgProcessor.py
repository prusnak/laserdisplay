import xml.sax
import LaserDisplay

class SVGHandler(xml.sax.handler.ContentHandler):

    def __init__(self, LD, scale):
        xml.sax.handler.ContentHandler.__init__(self)
        self.LD = LD
        self.scale = scale

    def startElement(self, name, attrs):
        if name == 'path':
            tokens = attrs.get('d').\
                replace('m',' m ').replace('c',' c ').replace('l',' l ').\
                replace('h',' h ').replace('v',' v ').replace('z',' z ').\
                replace('M',' M ').replace('C',' C ').replace('L',' L ').\
                replace('H',' H ').replace('V',' V ').replace('Z',' Z ').\
                replace('  ',' ').strip().split(' ')
            color = attrs.get('stroke')
            if color:
                self.LD.set_color(color)
            i,x,y = 0,0,0
            x0,y0 = x,y
            cmd = None
            while i < len(tokens):
                if tokens[i] == '':
                    i += 1
                if tokens[i].lower() in ['m', 'c', 'l', 'h', 'v', 'z']:
                    cmd = tokens[i]
                    i += 1
                if cmd == 'm':
                    delta = tokens[i].split(',')
                    x += float(delta[0])*self.scale
                    y += float(delta[1])*self.scale
                    x0,y0 = x,y
                    cmd = 'l'
                elif cmd == 'M':
                    delta = tokens[i].split(',')
                    x = float(delta[0])*self.scale
                    y = float(delta[1])*self.scale
                    x0,y0 = x,y
                    cmd = 'l'
                elif cmd == 'l':
                    delta = tokens[i].split(',')
                    nx = x+float(delta[0])*self.scale
                    ny = y+float(delta[1])*self.scale
                    self.LD.draw_line(x, y, nx, ny)
                    x,y = nx,ny
                elif cmd == 'L':
                    delta = tokens[i].split(',')
                    nx = float(delta[0])*self.scale
                    ny = float(delta[1])*self.scale
                    self.LD.draw_line(x, y, nx, ny)
                    x,y = nx,ny
                elif cmd == 'z' or cmd == 'Z':
                    i -= 1
                    self.LD.draw_line(x, y, x0, y0)
                    x,y = x0,y0
                elif cmd == 'h':
                    delta = tokens[i]
                    nx = x+float(delta)*self.scale
                    self.LD.draw_line(x, y, nx, y)
                    x = nx
                elif cmd == 'H':
                    delta = tokens[i]
                    nx = float(delta)*self.scale
                    self.LD.draw_line(x, y, nx, y)
                    x = nx
                elif cmd == 'v':
                    delta = tokens[i]
                    ny = y+float(delta)*self.scale
                    self.LD.draw_line(x, y, x, ny)
                    y = ny
                elif cmd == 'V':
                    delta = tokens[i]
                    ny = float(delta)*self.scale
                    self.LD.draw_line(x, y, x, ny)
                    y = ny
                elif cmd == 'c':
                    ctrl1 = tokens[i].split(',')
                    ctrl2 = tokens[i+1].split(',')
                    delta = tokens[i+2].split(',')
                    nx = x + float(delta[0])*self.scale
                    ny = y + float(delta[1])*self.scale
                    self.LD.draw_cubic_bezier([[x,y],[x+float(ctrl1[0])*self.scale,y+float(ctrl1[1])*self.scale],[x+float(ctrl2[0])*self.scale,y+float(ctrl2[1])*self.scale],[nx,ny]],8)
                    x = nx
                    y = ny
                    i+=2
                elif cmd == 'C':
                    ctrl1 = tokens[i].split(',')
                    ctrl2 = tokens[i+1].split(',')
                    delta = tokens[i+2].split(',')
                    nx = float(delta[0])*self.scale
                    ny = float(delta[1])*self.scale
                    self.LD.draw_cubic_bezier([[x,y],[float(ctrl1[0])*self.scale,float(ctrl1[1])*self.scale],[float(ctrl2[0])*self.scale,float(ctrl2[1])*self.scale],[nx,ny]],8)
                    x = nx
                    y = ny
                    i+=2
                i+=1

        if name == 'ellipse':
            cx = float(attrs.get('cx'))*self.scale
            cy = float(attrs.get('cy'))*self.scale
            rx = float(attrs.get('rx'))*self.scale
            ry = float(attrs.get('ry'))*self.scale
            color = attrs.get('stroke')
            if color:
                self.LD.set_color(color)
            self.LD.draw_ellipse(cx, cy, rx, ry)

        if name == 'rect':
            x = float(attrs.get('x'))*self.scale
            y = float(attrs.get('y'))*self.scale
            w = float(attrs.get('width'))*self.scale
            h = float(attrs.get('height'))*self.scale
            color = attrs.get('stroke')
            if color:
                self.LD.set_color(color)
            self.LD.draw_rect(x, y, w, h)

        if name == 'polyline':
            points = attrs.get('points').split(' ')
            color = attrs.get('stroke')
            if color:
                self.LD.set_color(color)
            points = map(lambda a: map(lambda b: float(b)*self.scale, a.split(',') ), filter(lambda a: len(a)>0, points) )
            self.LD.draw_polyline(points)

        if name == 'line':
            x1 = float(attrs.get('x1'))*self.scale
            y1 = float(attrs.get('y1'))*self.scale
            x2 = float(attrs.get('x2'))*self.scale
            y2 = float(attrs.get('y2'))*self.scale
            color = attrs.get('stroke')
            if color:
                self.LD.set_color(color)
            self.LD.draw_line(x1,y1,x2,y2)

class SvgProcessor():

    def __init__(self, LD):
        self.LD = LD

    def parseString(self, svg, scale = 1.0):
        xml.sax.parseString(svg,SVGHandler(self.LD, scale))

    def parseFile(self, svgfile, scale = 1.0):
        xml.sax.parse(svgfile,SVGHandler(self.LD, scale))
