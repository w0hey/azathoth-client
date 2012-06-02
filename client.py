#!/usr/bin/env python

import logging
import ConfigParser

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
    logging.getLogger('gtkmvc').setLevel(logging.DEBUG)
    logging.root.setLevel(logging.DEBUG)
    config = ConfigParser.RawConfigParser()
    config.read('client.cfg')
    m = MainModel()
    v = MainView()
    c = MainController(m, v, config)
    reactor.run()
