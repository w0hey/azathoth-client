#!/usr/bin/env python

import logging

from twisted.internet import gtk2reactor
gtk2reactor.install()

from twisted.internet import reactor
from twisted.python import log
from view import MainView
from controller import MainController
from model import MainModel

if __name__ == "__main__":
    observer = log.PythonLoggingObserver()
    observer.start()
    #logging.getLogger('gtkmvc').setLevel(logging.DEBUG)
    m = MainModel()
    v = MainView()
    c = MainController(m, v)
    reactor.run()
