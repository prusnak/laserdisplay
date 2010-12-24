import telnetlib
from LaserDisplay import LaserDisplay

class LaserDisplayRemote(LaserDisplay):

    def __init__(self, server, port = 31337):
        try:
            self.remote = telnetlib.Telnet(server, port)
        except:
            raise IOError('Cannot reach %s:%d ...' % (server, port))
        LaserDisplay.__init__(self)

    def set_laser_configuration(self):
        self.remote.write('config %d %d\r\n' % (self.blanking_delay, self.scan_rate))

    def set_color(self, color):
        LaserDisplay.set_color(self, color)
        self.remote.write('color %d %d %d\r\n' % (self.color['R'],self.color['G'],self.color['B']))

    def show_frame(self):
        self.remote.write('show\r\n')

    def draw_point(self, x,y):
        self.remote.write('point %f %f\r\n' % (x, y))

    def draw_line(self, x1, y1, x2, y2):
        self.remote.write('line %f %f %f %f\r\n' % (x1, y1, x2, y2))

    def draw_rect(self, x, y, w, h):
        self.remote.write('rect %f %f %f %f\r\n' % (x, y, w, h))

    def draw_ellipse(self, cx, cy, rx, ry):
        self.remote.write('ellipse %f %f %f %f\r\n' % (cx, cy, rx, ry))

    def draw_polyline(self, points):
        msg = 'polyline'
        for p in points:
            msg += ' %f %f' % (p[0], p[1])
        self.remote.write(msg + '\r\n')

    def draw_quadratic_bezier(self, points, steps):
        msg = 'quadratic'
        for p in points:
            msg += ' %f %f' % (p[0], p[1])
        self.remote.write(msg + '\r\n')

    def draw_cubic_bezier(self, points, steps):
        msg = 'cubic'
        for p in points:
            msg += ' %f %f' % (p[0], p[1])
        self.remote.write(msg + '\r\n')
