from twisted.internet import reactor, protocol
from twisted.protocols import basic

QUAD_QUALITY = 8
CUBIC_QUALITY = 8

LD = None

def process_line(line):
    s = line.split(' ')
    if LD is None or len(s) < 1:
        return

    if s[0] == 'config':
        LD.set_blanking_delay( int(s[1]) )
        LD.set_scan_rate( int(s[2]) )

    elif s[0] == 'color':
        LD.set_color( (int(s[1]),int(s[2]),int(s[3])) )

    elif s[0] == 'show':
        LD.show_frame()

    elif s[0] == 'point':
        LD.draw_point( float(s[1]), float(s[2]), int(s[3]) )

    elif s[0] == 'line':
        LD.draw_line( float(s[1]), float(s[2]), float(s[3]), float(s[4]) )

    elif s[0] == 'rect':
        LD.draw_rect( float(s[1]), float(s[2]), float(s[3]), float(s[4]) )

    elif s[0] == 'ellipse':
        LD.draw_ellipse( float(s[1]), float(s[2]), float(s[3]), float(s[4]) )

    elif s[0] == 'polyline':
        points = []
        for i in range((len(s)-1)/2):
            points.append( (float(s[2*i+1]),float(s[2*i+2])) )
        LD.draw_polyline(points)

    elif s[0] == 'quadratic':
        points = []
        for i in range((len(s)-1)/2):
            points.append( (float(s[2*i+1]),float(s[2*i+2])) )
        LD.draw_quadratic_bezier(points, QUAD_QUALITY)

    elif s[0] == 'cubic':
        points = []
        for i in range((len(s)-1)/2):
            points.append( (float(s[2*i+1]),float(s[2*i+2])) )
        LD.draw_cubic_bezier(points, CUBIC_QUALITY)

class LaserProtocol(basic.LineOnlyReceiver):

    def lineReceived(self, line):
        process_line(line)

class LaserServer():

    def __init__(self, port = 31337):
        self.port = port

    def start(self, emulator = False):
        global LD
        if emulator:
            from LaserDisplaySimulator import LaserDisplaySimulator
            LD = LaserDisplaySimulator()
        else:
            from LaserDisplayLocal import LaserDisplayLocal
            LD = LaserDisplayLocal()
        factory = protocol.ServerFactory()
        factory.protocol = LaserProtocol
        reactor.listenTCP(self.port, factory)
        print 'Listening on port %d ...' % self.port
        reactor.run()
