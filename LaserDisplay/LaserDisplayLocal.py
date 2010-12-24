import usb
import time
from LaserDisplay import LaserDisplay

class LaserDisplayLocal(LaserDisplay):

    def __init__(self):
        LaserDisplay.__init__(self)
        self.__buffer = []

        self.usbdev = usb.core.find(idVendor=0x9999, idProduct=0x5555)
        if self.usbdev is None:
            self.__send_initalization()
            self.usbdev = usb.core.find(idVendor=0x9999, idProduct=0x5555)
        if self.usbdev is None:
            raise IOError('Could not find laser device (9999:5555) ...')

        # set the active configuration
        # with no arguments, the first configuration will be the active one
        self.usbdev.set_configuration()

        # get an endpoint instance
        # first interface match the first OUT endpoint
        self.ep = usb.util.find_descriptor(
            self.usbdev.get_interface_altsetting(),
                custom_match = \
                lambda e: \
                    usb.util.endpoint_direction(e.bEndpointAddress) == \
                    usb.util.ENDPOINT_OUT
        )

        assert self.ep is not None
        self.set_laser_configuration()

    def __send_initalization(self):
        usbdev = usb.core.find(idVendor=0x3333, idProduct=0x5555)
        if usbdev is None:
            raise IOError('Could not find laser device (3333:5555) ...')

        handle = usbdev.open()

        print 'Initializing device ... ',
        initlog = open('usbinit.log')

        for line in initlog.readlines():
            setup_packet = line.split('|')[0]
            buf = line.split('|')[-1]
            if len(buf):
                values = setup_packet.strip().split(' ')
                reqType = int(values[0],16)
                req = int(values[1],16)
                value = int(values[2],16)*256+int(values[3],16)
                index = int(values[4],16)*256+int(values[5],16)
                length = int(values[6],16)*256+int(values[7],16)

                binbuf = ''
                for byte in buf.strip().split(' '):
                    binbuf += chr(int(byte,16))

                handle.controlMsg(reqType,req,binbuf,value,index)

        print 'done'
        time.sleep(1)

    def set_laser_configuration(self):
        self.ep.write([self.blanking_delay, (45000 - self.scan_rate)/200])

    def show_frame(self):
        self.ep.write(self.__buffer, 0)
        self.__buffer = []

    def draw_point(self, x, y, flags = 0x01):
        x,y = self.apply_context_transforms(x,y)
        x = noise_clamp(x)
        y = noise_clamp(y)
        self.__buffer += [x, 0x00, y, 0x00, self.color['R'], self.color['G'], self.color['B'], flags]

    def draw_line(self, x1, y1, x2, y2):
        self.draw_point(x1, y1, 0x03)
        self.draw_point(x2, y2, 0x02)

    def draw_rect(self, x, y, w, h):
        self.draw_point(x  , y  , 0x03)
        self.draw_point(x+w, y  , 0x00)
        self.draw_point(x+w, y+h, 0x00)
        self.draw_point(x  , y+h, 0x00)
        self.draw_point(x  ,   y, 0x02)

    def draw_ellipse(self, cx, cy, rx, ry):
        if rx < 1 or ry < 1:
            return
        steps = int(math.sqrt(rx>ry and rx or ry)*2)
        i = 0
        self.draw_point(cx+rx*math.cos(2*math.pi/steps*i),cy+ry*math.sin(2*math.pi/steps*i),0x03)
        for i in range(1,steps):
            self.draw_line(cx+rx*math.cos(2*math.pi/steps*i),cy+ry*math.sin(2*math.pi/steps*i),0x00)
        i = 0
        self.draw_point(cx+rx*math.cos(2*math.pi/steps*i),cy+ry*math.sin(2*math.pi/steps*i),0x02)

    def draw_polyline(self, points):
        self.draw_point( p[0][0], p[0][1], 0x03)
        for i in len(points)-2:
            self.draw_point( p[i][0], p[i][1], 0x00)
        i = len(points)-1
        self.draw_point( p[i][0], p[i][1], 0x02)

    def draw_quadratic_bezier(self, points, steps):
        if len(points) < 3:
            print 'Quadratic Bezier curves have to have at least three points'
            return

        step_inc = 1.0/(steps)

        self.draw_point(points[0][0], points[0][1], 0x03)

        flags = 0x00
        for i in range(0, len(points) - 2, 2):
            t = 0.0
            t_1 = 1.0
            for s in range(steps):
                t += step_inc
                t_1 = 1.0 - t
                if s == steps - 1 and i >= len(points) - 3:
                    flags = 0x02
                self.draw_point(t_1 * (t_1 * points[i]  [0] + t * points[i+1][0]) + \
                                t   * (t_1 * points[i+1][0] + t * points[i+2][0]),  \
                                t_1 * (t_1 * points[i]  [1] + t * points[i+1][1]) + \
                                t   * (t_1 * points[i+1][1] + t * points[i+2][1]), flags)

    def draw_cubic_bezier(self, points, steps):
        if len(points) < 4:
            print 'Cubic Bezier curves have to have at least four points'
            return

        step_inc = 1.0/(steps)

        self.draw_point(points[0][0], points[0][1], 0x03)

        flags = 0x00
        for i in range(0, len(points) - 3, 2):
            t = 0.0
            t_1 = 1.0
            for s in range(steps):
                t += step_inc
                t_1 = 1.0 - t
                if s == steps - 1 and i >= len(points) - 4:
                    flags = 0x02
                self.draw_point(t_1 * (t_1 * (t_1 * points[i][0] + t * points[i+1][0]) + \
                                t   * (t_1 * points[i+1][0] + t * points[i+2][0])) +
                                t   * (t_1 * (t_1 * points[i+1][0] + t * points[i+2][0]) + \
                                t   * (t_1 * points[i+2][0] + t * points[i+3][0])),  \
                                t_1 * (t_1 * (t_1 * points[i][1] + t * points[i+1][1]) + \
                                t   * (t_1 * points[i+1][1] + t * points[i+2][1])) +
                                t   * (t_1 * (t_1 * points[i+1][1] + t * points[i+2][1]) + \
                                t   * (t_1 * points[i+2][1] + t * points[i+3][1])), flags)
