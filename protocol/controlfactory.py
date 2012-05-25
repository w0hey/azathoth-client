from twisted.internet import protocol
from twisted.python import log

from protocol.controlprotocol import ControlProtocol

class ControlFactory(protocol.ClientFactory):
    protocol = ControlProtocol

    def __init__(self, model):
        self.model = model
        self.control = None

    def startedConnecting(self, connector):
        self.model.onStartConnection()

    def clientConnectionFailed(self, connector, reason):
        log.err(reason.getErrorMessage())
        self.model.onConnectionFailed(reason)

    def clientConnectionLost(self, connector, reason):
        self.model.onConnectionLost()


