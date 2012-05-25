#!/usr/bin/env python

import logging

from twisted.internet import gtk2reactor
gtk2reactor.install()

from twisted.internet import reactor

from view import MainView
from controller import MainController
from model import MainModel

if __name__ == "__main__":
    m = MainModel()
    v = MainView()
    c = MainController(m, v)
    reactor.run()
