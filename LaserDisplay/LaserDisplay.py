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
        '0': [(191, 130), (194, 194), (127, 191), (65, 191), (62, 129), (64, 62), (125, 62), (195, 65), (192, 131)],
        '1': [(178, 133), (130, 149), (119, 191), (118, 116), (121, 62)],
        '2': [(187, 131), (192, 189), (125, 192), (66, 190), (64, 149), (95, 97), (191, 66), (122, 63), (62, 64)],
        '3': [(189, 161), (192, 197), (120, 193), (12, 188), (111, 126), (21, 64), (120, 60), (189, 64), (189, 96)],
        '4': [(66, 127), (121, 128), (193, 125), (134, 156), (124, 194), (123, 128), (122, 64)],
        '5': [(65, 192), (122, 192), (192, 192), (192, 161), (190, 133), (64, 137), (63, 99), (65, 63), (192, 64)],
        '6': [(62, 160), (62, 193), (119, 194), (192, 194), (193, 133), (193, 65), (127, 62), (63, 64), (62, 99), (63, 130), (120, 131), (186, 125), (183, 93)],
        '7': [(194, 191), (124, 191), (64, 191), (146, 142), (188, 63)],
        '8': [(192, 164), (192, 193), (126, 195), (67, 192), (64, 165), (65, 137), (119, 133), (190, 134), (193, 102), (195, 64), (122, 60), (62, 64), (60, 89), (58, 119), (121, 132), (189, 134), (192, 166)],
        '9': [(65, 191), (191, 193), (193, 159), (190, 115), (131, 120), (75, 144), (62, 190), (64, 123), (66, 63)],
        ':': []
    }

    def __init__(self):
        self.__adjust_glyphs()
        # set variables and the initial state
        self.blanking_delay = 202
        self.scan_rate = 37000
        self.noise = 0
        self.set_color(self.WHITE)
        self.ctm = None

# private functions

    def __adjust_glyphs(self):
        for k in self.GLYPHS.keys():
            self.GLYPHS[k] = map(lambda(p):([p[0]/255.0,p[1]/255.0]),self.GLYPHS[k])

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
        self.draw_line(x,y,x+w,y)
        self.draw_line(x+w,y,x+w,y+h)
        self.draw_line(x+w,y+h,x,y+h)
        self.draw_line(x,y+h,x,y)

    def draw_ellipse(self, cx, cy, rx, ry):
        # TODO: change to bezier instead of lines
        for i in range(0,32):
            self.draw_line(cx+rx*math.cos(2*math.pi/32*i),cy+ry*math.sin(2*math.pi/32*i),cx+rx*math.cos(2*math.pi/32*(i+1)),cy+ry*math.sin(2*math.pi/32*(i+1)))

    def draw_multiline(self, points):
        for i in len(points)-1:
            self.draw_line( p[i][0], p[i][1], p[i+1][0], p[i+1][1] )

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
