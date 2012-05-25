from gtkmvc import Model
from twisted.internet import reactor

from protocol.controlfactory import ControlFactory

class MainModel(Model):
    connected = False
    estop_act = "N/A"
    estop_cmd = "N/A"
    select_act = "N/A"
    select_cmd = "N/A"
    moving = "Unknown"
    xpos = 0
    ypos = 0
    xval = 0
    yval = 0
    joy_x = 0
    joy_y = 0
    
    __observables__ = ("connected", "estop_act", "estop_cmd", "select_act", "select_cmd",
                        "moving", "xpos", "ypos", "xval", "yval", "joy_x", "joy_y")

    def connect(self, host, port=2024):
        self.factory = ControlFactory(self)
        self.connection = reactor.connectTCP(host, port, self.factory)

    def disconnect(self):
        self.connection.disconnect()

    def onStartConnection(self):
        pass
    
    def onConnect(self):
        self.connected = True

    def onConnectionLost(self):
        self.connected = False

    def joystickCommand(self, x, y):
        self.factory.control.send_joystick_command(x, y)
        self.joy_x = x
        self.joy_y = y

    def onStatusUpdate(self, status, xpos, ypos, xval, yval):
        self.estop_act = 'RUN' if (status & 0x01 == 0x01) else 'STOP'
        self.estop_cmd = 'RUN' if (status & 0x02 == 0x02) else 'STOP'
        self.select_act = 'ROBOT' if (status & 0x04 == 0x04) else 'CHAIR'
        self.select_cmd = 'ROBOT' if (status & 0x08 == 0x08) else 'CHAIR'
        self.moving = 'MOVING' if (status & 0x10 == 0x10) else 'STOPPED'

    def select(self):
        self.factory.control.send_select_command(True)

    def deselect(self):
        self.factory.control.send_select_command(False)

    def estop(self):
        self.factory.control.send_estop_command()

    def reset(self):
        self.factory.control.send_reset_command()
