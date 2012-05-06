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

from calibrationdialog import CalibrationDialog
from protocol.controlfactory import ControlFactory
from joystick import Joystick

class AzathothClient:
    def __init__(self):
        self.connected = False
        self.builder = gtk.Builder()
        self.builder.add_from_file('main.glade')
        self.mainWindow = self.builder.get_object('window_main')

        self.builder.connect_signals(self)

        self.btn_disconnect = self.builder.get_object('btn_disconnect')
        self.btn_connect = self.builder.get_object('btn_connect')
        self.statusbar = self.builder.get_object('statusbar')
        self.context_id = self.statusbar.get_context_id("Azathoth")
        self.label_js_x = self.builder.get_object('label_js_x')
        self.label_js_y = self.builder.get_object('label_js_y')
        self.rb_js_enable = self.builder.get_object('rb_js_enable')
        self.rb_js_disable = self.builder.get_object('rb_js_disable')

        self.joystick_x = 0
        self.joystick_y = 0

        self.mainWindow.show_all()

    def connect(self, host, port=2024):
        log.msg(format="Connecting to host %(host)s on port %(port)d", host=host, port=port)
        self.statusbar.push(self.context_id, 'Connecting...')
        self.factory = ControlFactory(self)
        self.connection = reactor.connectTCP(host, port, self.factory)

    def disconnect(self):
        log.msg("Disconnecting")
        self.connection.disconnect()

    def enableJoystick(self):
        self.joystick = Joystick(0)
        self.js_handler = self.joystick.connect('axis', self.axis_event)

    def disableJoystick(self):
        self.joystick.disconnect(self.js_handler)
        self.joystick.shutdown()
        self.joystick = None

    def onStartConnection(self):
        self.btn_connect.set_sensitive(False)

    def onConnect(self):
        self.btn_disconnect.set_sensitive(True)
        self.btn_connect.set_sensitive(False)
        self.statusbar.remove_all(self.context_id)
        self.statusbar.push(self.context_id, 'Connected')

    def onConnectionLost(self):
        self.btn_disconnect.set_sensitive(False)
        self.btn_connect.set_sensitive(True)
        self.statusbar.remove_all(self.context_id)
        self.statusbar.push(self.context_id, 'Disconnected')

    def onConnectionFailed(self, reason):
        self.btn_connect.set_sensitive(True)
        self.statusbar.remove_all(self.context_id)
        self.statusbar.push(self.context_id, 'Connection failed!')

    def onUpdateAxis(self):
        self.label_js_x.set_label(str(self.joystick_x))
        self.label_js_y.set_label(str(self.joystick_y))
        self.factory.control.send_joystick_command(self.joystick_x, self.joystick_y)

    def on_window_main_delete_event(self, win, event):
        reactor.stop()

    def on_imi_quit_activate(self, widget):
        reactor.stop()

    def on_imi_calibration_activate(self, widget):
        dlg = CalibrationDialog(self)

    def on_btn_connect_clicked(self, widget):
        host = self.builder.get_object('entry_host').get_text()
        self.connect(host)

    def on_btn_disconnect_clicked(self, widget):
        self.disconnect()

    def on_rb_js_enable_clicked(self, widget):
        if self.rb_js_enable.get_active():
            self.enableJoystick()

    def on_rb_js_disable_clicked(self, widget):
        if self.rb_js_disable.get_active():
            self.disableJoystick()

    def axis_event(self, object, axis, value, init):
        if axis == 0:
            self.joystick_x = value / 256
        if axis == 1:
            self.joystick_y = -value / 256
        self.onUpdateAxis()

    def button_event(self, object, button, value, init):
        pass

AzathothClient()
reactor.run()
