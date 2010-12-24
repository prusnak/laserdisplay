import time
import pygame
from LaserDisplay import LaserDisplay

class LaserDisplaySimulator(LaserDisplay):

    SCALE = 2

    def __init__(self):
        LaserDisplay.__init__(self)
        try:
            pygame.init()
            self.surface = pygame.display.set_mode((self.SIZE*self.SCALE, self.SIZE*self.SCALE))
            self.surface.fill( (0,0,0) )
            pygame.display.set_caption('Laser Display Simulator')
        except:
            raise IOError('Could not initialize pygame')

    def __color(self):
        return pygame.Color(self.color['R'], self.color['G'], self.color['B'])

    def set_laser_configuration(self):
        pass

    def show_frame(self):
        pygame.display.flip()
        self.surface.fill( (0,0,0) )

    def draw_point(self, x,y):
        x,y = self.apply_context_transforms(x,y)
        x,y = map(lambda a: a*self.SCALE, (x,y) )
        pygame.draw.rect(self.surface, self.__color(), pygame.Rect(x,y,self.SCALE,self.SCALE), 1)

    def draw_line(self, x1, y1, x2, y2):
        x1,y1 = self.apply_context_transforms(x1,y1)
        x2,y2 = self.apply_context_transforms(x2,y2)
        x1,y1,x2,y2 = map(lambda a: a*self.SCALE, (x1,y1,x2,y2) )
        pygame.draw.line(self.surface, self.__color(), (x1,y1), (x2,y2), self.SCALE)

    def draw_rect(self, x, y, w, h):
        x,y,w,h = map(lambda a: a*self.SCALE, (x,y,w,h) )
        pygame.draw.rect(self.surface, self.__color(), pygame.Rect(x,y,w,h), self.SCALE)

    def draw_ellipse(self, cx, cy, rx, ry):
        if rx < 1 or ry < 1:
            return
        cx,cy,rx,ry = map(lambda a: a*self.SCALE, (cx,cy,rx,ry) )
        pygame.draw.ellipse(self.surface, self.__color(), pygame.Rect(cx-rx,cy-ry,2*rx,2*ry), self.SCALE)

    def draw_multiline(self, points):
        for i in range(len(points)):
            points[i] = map(lambda a: a*self.SCALE, points[i] )
        pygame.draw.lines(self.surface, self.__color(), False, points, self.SCALE)

    def draw_quadratic_bezier(self, points, steps):
        if len(points) < 3:
            print 'Quadratic Bezier curves have to have at least three points'
            return

        step_inc = 1.0/(steps)

        old_pos = ( points[0][0]*self.SCALE, points[0][1]*self.SCALE )

        for i in range(0, len(points) - 2, 2):
            t = 0.0
            t_1 = 1.0
            for s in range(steps):
                t += step_inc
                t_1 = 1.0 - t
                pos = ((t_1 * (t_1 * points[i]  [0] + t * points[i+1][0]) + \
                        t   * (t_1 * points[i+1][0] + t * points[i+2][0]))*self.SCALE,  \
                       (t_1 * (t_1 * points[i]  [1] + t * points[i+1][1]) + \
                        t   * (t_1 * points[i+1][1] + t * points[i+2][1]))*self.SCALE)
                pygame.draw.line(self.surface, self.__color(), old_pos, pos, self.SCALE)
                old_pos = pos

    def draw_cubic_bezier(self, points, steps):
        if len(points) < 4:
            print 'Cubic Bezier curves have to have at least four points'
            return

        step_inc = 1.0/(steps)

        old_pos =  ( points[0][0]*self.SCALE, points[0][1]*self.SCALE )

        for i in range(0, len(points) - 3, 2):
            t = 0.0
            t_1 = 1.0
            for s in range(steps):
                t += step_inc
                t_1 = 1.0 - t
                pos = ((t_1 * (t_1 * (t_1 * points[i][0] + t * points[i+1][0]) + \
                        t   * (t_1 * points[i+1][0] + t * points[i+2][0])) +
                        t   * (t_1 * (t_1 * points[i+1][0] + t * points[i+2][0]) + \
                        t   * (t_1 * points[i+2][0] + t * points[i+3][0])))*self.SCALE,  \
                       (t_1 * (t_1 * (t_1 * points[i][1] + t * points[i+1][1]) + \
                        t   * (t_1 * points[i+1][1] + t * points[i+2][1])) +
                        t   * (t_1 * (t_1 * points[i+1][1] + t * points[i+2][1]) + \
                        t   * (t_1 * points[i+2][1] + t * points[i+3][1])))*self.SCALE)
                pygame.draw.line(self.surface, self.__color(), old_pos, pos, self.SCALE)
                old_pos = pos
