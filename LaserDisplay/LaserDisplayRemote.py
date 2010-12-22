import telnetlib
from LaserDisplay import LaserDisplay

class LaserDisplayRemote(LaserDisplay):

    def __init__(self, server, port = 31337):
        LaserDisplay.__init__(self)
        try:
            self.remote = telnetlib.Telnet(server, port)
        except:
            raise IOError('Cannot reach %s:%d ...' % (server, port))

    def set_laser_configuration(self):
        self.remote.write('config %d %d\n' % (self.blanking_delay, self.scan_rate))

    def show_frame(self):
        self.remote.write('show\n')

    def draw_point(self, x,y):
        self.remote.write('point %f %f\n' % (x, y))

    def draw_line(self, x1, y1, x2, y2):
        self.remote.write('line %f %f %f %f\n' % (x1, y1, x2, y2))

    def draw_quadratic_bezier(self, points, steps):
        msg = 'quadratic'
        for p in points:
            msg += ' %f %f' % (p[0], p[1])
        self.remote.write(msg + '\n')

    def draw_cubic_bezier(self, points, steps):
        msg = 'cubic'
        for p in points:
            msg += ' %f %f' % (p[0], p[1])
        self.remote.write(msg + '\n')
