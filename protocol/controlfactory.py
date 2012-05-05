from twisted.internet import protocol
from twisted.python import log

from protocol.controlprotocol import ControlProtocol

class ControlFactory(protocol.ClientFactory):
    protocol = ControlProtocol

    def __init__(self, application):
        self.app = application
        self.control = None

    def startedConnecting(self, connector):
        self.app.onStartConnection()

    def clientConnectionFailed(self, connector, reason):
        log.err(reason.getErrorMessage())
        self.app.onConnectionFailed(reason)

    def clientConnectionLost(self, connector, reason):
        self.app.onConnectionLost()


