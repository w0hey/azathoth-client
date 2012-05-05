from twisted.internet import protocol
from twisted.python import log

class ControlFactory(protocol.ClientFactory):
    protocol = ControlProtocol

    def __init__(self, application):
        self.app = application
        self.control = None

    def clientConnectionFailed(self, connector, reason):
        log.err(reason.getErrorMessage())


