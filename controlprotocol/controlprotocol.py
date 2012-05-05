from twisted.protocotols.basic import NetstringReceiver
from twisted.python import log

class ControlProtocol(NetstringReceiver):
    def connectionMade(self):
        self.factory.control = self

    def connectionLost(self, reason):
        self.factory.control = None

    def stringReceived(self, string):
        if string[0] == 'c':
            # calibration value response
            cur_x = ord(string[1])
            cur_y = ord(string[2])
            eeprom_x = ord(string[3])
            eeprom_y = ord(string[4])
            self.factory.app.update_calibration(cur_x, cur_y, eeprom_x, eeprom_y)

    def req_cal_values(self):
        self.sendString('c')

    def send_cal_values(self, x, y):
        string = 'C' + chr(x) + chr(y)
        self.sendString(string)


