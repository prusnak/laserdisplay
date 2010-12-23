import math
from numpy import matrix

class LaserDisplay():

# constants

    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    CYAN = (0,255,255)
    MAGENTA = (255,0,255)
    YELLOW = (255,255,0)
    WHITE = (255,255,255)

    SIZE = 256

    GLYPHS = {
        '0': [(0.25, 0.49), (0.24, 0.24), (0.50, 0.25), (0.75, 0.25), (0.76, 0.49), (0.75, 0.76), (0.51, 0.76), (0.24, 0.75), (0.25, 0.49)],
        '1': [(0.30, 0.48), (0.49, 0.42), (0.53, 0.25), (0.54, 0.55), (0.53, 0.76)],
        '2': [(0.27, 0.49), (0.25, 0.26), (0.51, 0.25), (0.74, 0.25), (0.75, 0.42), (0.63, 0.62), (0.25, 0.74), (0.52, 0.75), (0.76, 0.75)],
        '3': [(0.26, 0.37), (0.25, 0.23), (0.53, 0.24), (0.95, 0.26), (0.56, 0.51), (0.92, 0.75), (0.53, 0.76), (0.26, 0.75), (0.26, 0.62)],
        '4': [(0.74, 0.50), (0.53, 0.50), (0.24, 0.51), (0.47, 0.39), (0.51, 0.24), (0.52, 0.50), (0.52, 0.75)],
        '5': [(0.75, 0.25), (0.52, 0.25), (0.25, 0.25), (0.25, 0.37), (0.25, 0.48), (0.75, 0.46), (0.75, 0.61), (0.75, 0.75), (0.25, 0.75)],
        '6': [(0.76, 0.37), (0.76, 0.24), (0.53, 0.24), (0.25, 0.24), (0.24, 0.48), (0.24, 0.75), (0.50, 0.76), (0.75, 0.75), (0.76, 0.61), (0.75, 0.49), (0.53, 0.49), (0.27, 0.51), (0.28, 0.64)],
        '7': [(0.24, 0.25), (0.51, 0.25), (0.75, 0.25), (0.43, 0.44), (0.26, 0.75)],
        '8': [(0.25, 0.36), (0.25, 0.24), (0.51, 0.24), (0.74, 0.25), (0.75, 0.35), (0.75, 0.46), (0.53, 0.48), (0.25, 0.47), (0.24, 0.60), (0.24, 0.75), (0.52, 0.76), (0.76, 0.75), (0.76, 0.65), (0.77, 0.53), (0.53, 0.48), (0.26, 0.47), (0.25, 0.35)],
        '9': [(0.75, 0.25), (0.25, 0.24), (0.24, 0.38), (0.25, 0.55), (0.49, 0.53), (0.71, 0.44), (0.76, 0.25), (0.75, 0.52), (0.74, 0.75)],
        ':': [(0.50, 0.40), (0.30, 0.50), (0.50, 0.60), (0.70, 0.50), (0.50, 0.40)]
    }

    def __init__(self):
        # set variables and the initial state
        self.blanking_delay = 202
        self.scan_rate = 37000
        self.noise = 0
        self.set_color(self.WHITE)
        self.ctm = None

# private functions

    def __gen_glyph_data(self, char, x, y, rx, ry):
        glyph_data = []
        for i in range(len(self.GLYPHS[char])):
            glyph_data.append([(int)(x+(self.GLYPHS[char][i][0])*rx),(int)(y+(self.GLYPHS[char][i][1])*ry)]);
        return glyph_data

# public functions

    def noise_clamp(value):
        min = 0
        max = SIZE-1
        if self.noise > 0:
            value += random()*self.noise - self.noise/2
        if value > max: return max
        if value < min: return min
        return int(value)

    def set_noise(self, noise):
        self.noise = noise

    def set_color(self, c):
        if len(c) == 3:
            self.color = {'R': int(c[0]), 'G': int(c[1]), 'B': int(c[2])}
        elif len(c) == 7:
            self.color = {'R': int(c[1:3],16), 'G': int(c[3:5],16), 'B': int(c[5:7],16)}
        if self.color['R'] < 0: self.color['R'] = 0
        if self.color['G'] < 0: self.color['G'] = 0
        if self.color['B'] < 0: self.color['B'] = 0
        if self.color['R'] > 255: self.color['R'] = 255
        if self.color['G'] > 255: self.color['G'] = 255
        if self.color['B'] > 255: self.color['B'] = 255

    def set_scan_rate(self, value):
        self.scan_rate = value
        self.set_laser_configuration()

    def set_blanking_delay(self, value):
        self.blanking_delay = value
        self.set_laser_configuration()

    def set_laser_configuration(self):
        raise NotImplementedError

    def show_frame(self):
        raise NotImplementedError

    def draw_point(self, x, y):
        raise NotImplementedError

    def draw_line(self, x1, y1, x2, y2):
        raise NotImplementedError

    def draw_quadratic_bezier(self, points, steps):
        raise NotImplementedError

    def draw_cubic_bezier(self, points, steps):
        raise NotImplementedError

    def draw_rect(self, x, y, w, h):
        raise NotImplementedError

    def draw_ellipse(self, cx, cy, rx, ry):
        raise NotImplementedError

    def draw_multiline(self, points):
        raise NotImplementedError

    def draw_text(self, string, x, y, size, kerning_percentage = -0.3):
        for char in string:
            glyph_curve = self.__gen_glyph_data(char, x, y, size, size*2)
            self.draw_quadratic_bezier(glyph_curve, 5)
            x += int(size + size * kerning_percentage)

# routines that deal with coordinate system transforms:

    def init_transform(self):
        self.ctm = matrix([[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]])
        self.saved_matrix = self.ctm

    def apply_context_transforms(self, x,y):
        if self.ctm is None:
            return (x,y)
        else:
            vector = self.ctm*matrix([x,y,1]).transpose()
            return vector[0], vector[1]

    def save(self):
        self.saved_matrix = self.ctm

    def restore(self):
        self.ctm = self.saved_matrix

    def rotate(self, angle):
        self.ctm = matrix([[math.cos(angle), -math.sin(angle), 0.0], [math.sin(angle), math.cos(angle), 0.0], [0.0, 0.0, 1.0]])*self.ctm

    def translate(self, x, y):
        self.ctm = matrix([[1.0, 0.0, float(x)], [0.0, 1.0, float(y)], [0.0, 0.0, 1.0]])*self.ctm

    def scale(self, s):
        self.ctm = matrix([[float(s), 0.0, 0.0], [0.0, float(s), 0.0], [0.0, 0.0, 1.0]])*self.ctm

    def rotate_at(self,cx,cy,angle):
        self.translate(-cx,-cy)
        self.rotate(angle)
        self.translate(cx,cy)
