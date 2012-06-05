from gtkmvc import Model
from twisted.internet import reactor

from protocol.controlfactory import ControlFactory
from models.drivemodel import DriveModel

class MainModel(Model):
    connected = False
    joy_x = 0
    joy_y = 0
    sonar_range = 0
    
    __observables__ = ("connected", "joy_x", "joy_y", "sonar_range")

    def __init__(self):
        Model.__init__(self)
        self.factory = ControlFactory(self)
        self.driveModel = DriveModel(self)

    def connect(self, host, port=2024):
        self.connection = reactor.connectTCP(host, port, self.factory)

    def disconnect(self):
        self.connection.disconnect()

    def onStartConnection(self):
        pass
    
    def onConnect(self):
        self.connected = True

    def onConnectionLost(self):
        self.connected = False

    def onSonarUpdate(self, range):
        self.sonar_range = range
