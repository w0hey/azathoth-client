#!/usr/bin/env python

import sys
import logging

import pygtk
pygtk.require('2.0')
import gtk

from twisted.internet import gtk2reactor
gtk2reactor.install()

from twisted.internet import reactor, protocol
from twisted.python import log
log.startLogging(sys.stdout)

from protocol.controlfactory import ControlFactory

class AzathothClient:
    def __init__(self):
        self.connected = False
        self.builder = gtk.Builder()
        self.builder.add_from_file('main.glade')
        self.mainWindow = self.builder.get_object('window_main')
        self.builder.connect_signals(self)
        self.mainWindow.show_all()

    def connect(self, host, port=2024):
        log.msg(format="Connecting to host %(host)s on port %(port)d", host=host, port=port)
        self.factory = ControlFactory(self)
        self.connection = reactor.connectTCP(host, port, self.factory)
        self.builder.get_object('btn_disconnect').set_sensitive(True)
        self.builder.get_object('btn_connect').set_sensitive(False)

    def disconnect(self):
        log.msg("Disconnecting")
        self.connection.disconnect()
        self.builder.get_object('btn_disconnect').set_sensitive(False)
        self.builder.get_object('btn_connect').set_sensitive(True)

    def get_cal_values(self):
        self.factory.control.req_cal_values()

    def set_cal_values(self):
        x = int(self.builder.get_object('entry_x').get_text())
        y = int(self.builder.get_object('entry_y').get_text())
        self.factory.control.send_cal_values(x, y)

    def store_cal_values(self):
        pass

    def update_calibration(self, cur_x, cur_y, eeprom_x, eeprom_y):
        label_x = self.builder.get_object('label_stored_x')
        label_y = self.builder.get_object('label_stored_y')
        entry_x = self.builder.get_object('entry_x')
        entry_y = self.builder.get_object('entry_y')
        label_x.set_label("X: " + str(eeprom_x))
        label_y.set_label("Y: " + str(eeprom_y))
        entry_x.set_text(str(cur_x))
        entry_y.set_text(str(cur_y))

    def on_window_main_delete_event(self, win, event):
        reactor.stop()

    def on_imi_quit_activate(self):
        reactor.stop()

    def on_btn_connect_clicked(self, widget):
        host = self.builder.get_object('entry_host').get_text()
        self.connect(host)

    def on_btn_disconnect_clicked(self, widget):
        self.disconnect()

    def on_btn_get_values_clicked(self, widget):
        self.get_cal_values()

    def on_btn_set_values_clicked(self, widget):
        self.set_cal_values()

    def on_btn_store_values_clicked(self, widget):
        pass

AzathothClient()
reactor.run()
