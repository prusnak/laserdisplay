from LaserDisplay import LaserDisplay
from LaserDisplayLocal import LaserDisplayLocal
from LaserDisplayRemote import LaserDisplayRemote
from LaserDisplaySimulator import LaserDisplaySimulator

class LaserDisplayProxy(LaserDisplay):

    def __init__(self):
        self.devices = [ LaserDisplaySimulator(), LaserDisplayLocal() ]
        LaserDisplay.__init__(self)

    def set_laser_configuration(self):
        for i in self.devices:
          i.set_laser_configuration()

    def set_color(self, color):
        LaserDisplay.set_color(self, color)
        for i in self.devices:
          i.set_color(color)

    def show_frame(self):
        for i in self.devices:
          i.show_frame()

    def draw_point(self, x, y, flags = 0x01):
        for i in self.devices:
          i.draw_point(x, y, flags)

    def draw_line(self, x1, y1, x2, y2):
        for i in self.devices:
          i.draw_line(x1, y1, x2, y2)

    def draw_rect(self, x, y, w, h):
        for i in self.devices:
            i.draw_rect(x, y, w, h)

    def draw_ellipse(self, cx, cy, rx, ry):
        for i in self.devices:
            i.draw_ellipse(cx, cy, rx, ry)

    def draw_polyline(self, points):
        for i in self.devices:
            i.draw_polyline(points)

    def draw_quadratic_bezier(self, points, steps):
        for i in self.devices:
            i.draw_quadratic_bezier(points, steps)

    def draw_cubic_bezier(self, points, steps):
        for i in self.devices:
            i.draw_cubic_bezier(points, steps)
