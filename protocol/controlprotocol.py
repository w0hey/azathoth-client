import struct

from twisted.internet import defer
from twisted.protocols.basic import NetstringReceiver
from twisted.python import log

class ControlProtocol(NetstringReceiver):
    def connectionMade(self):
        self.factory.control = self
        self.factory.app.onConnect()

    def connectionLost(self, reason):
        self.factory.control = None

    def stringReceived(self, string):
        if string[0] == 'c':
            # calibration value response
            cur_x = ord(string[1])
            cur_y = ord(string[2])
            eeprom_x = ord(string[3])
            eeprom_y = ord(string[4])
            d = {}
            d['current_x'] = cur_x
            d['current_y'] = cur_y
            d['eeprom_x'] = eeprom_x
            d['eeprom_y'] = eeprom_y
            self.calibrate_d.callback(d)
        elif string[0] == 's':
            # status response
            status = ord(string[1])
            xpos = ord(string[2])
            ypos = ord(string[3])
            xval = ord(string[4])
            yval = ord(string[5])
            self.factory.app.onStatusUpdate(status, xpos, ypos, xval, yval)

    def req_cal_values(self):
        self.calibrate_d = defer.Deferred()
        self.sendString('c')
        return self.calibrate_d

    def send_cal_values(self, x, y):
        string = 'C' + chr(x) + chr(y)
        self.sendString(string)

    def cmd_cal_store(self):
        string = 'W'
        self.sendString(string)

    def send_joystick_command(self, x, y):
        # x and y are signed, so a simple chr(x) won't work.
        string = 'J' + struct.pack("!bb", x, y)
        self.sendString(string)

    def send_select_command(self, enable):
        if enable:
            string = 'D' + '\x01'
        else:
            string = 'D' + '\x00'
        self.sendString(string)

    def send_estop_command(self):
        string = 'E'
        self.sendString(string)

    def send_reset_command(self):
        string = 'R'
        self.sendString(string)

    def send_softstop_command(self):
        string = 'S'
        self.sendString(string)



