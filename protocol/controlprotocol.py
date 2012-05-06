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

    def req_cal_values(self):
        self.calibrate_d = defer.Deferred()
        self.sendString('c')
        return self.calibrate_d

    def send_cal_values(self, x, y):
        string = 'C' + chr(x) + chr(y)
        self.sendString(string)

    def send_joystick_command(self, x, y):
        string = 'J' + chr(x) + chr(y)
        self.sendString(string)



