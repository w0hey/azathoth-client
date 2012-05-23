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
        
        # let's just add widgets as members programatically.
        widgets = ('btn_disconnect', 'btn_connect', 'statusbar', 'label_js_x',
            'label_js_y', 'rb_js_enable', 'rb_js_disable', 'eb_js_x', 'eb_js_y',
            'eb_drivestatus', 'label_drivestatus', 'label_drive_x', 'label_drive_y',
            'label_raw_x', 'label_raw_y')
        for wid in widgets:
            setattr(self, wid, self.builder.get_object(wid))

        self.context_id = self.statusbar.get_context_id("Azathoth")

        self.prev_x = 0
        self.prev_y = 0
        self.joystick = None
        self.joystick_x = 0
        self.joystick_y = 0
        self.joystick_enabled = False

        self.mainWindow.show_all()

    def connect(self, host, port=2024):
        log.msg(format="Connecting to host %(host)s on port %(port)d", host=host, port=port)
        self.statusbar.push(self.context_id, 'Connecting...')
        self.factory = ControlFactory(self)
        self.connection = reactor.connectTCP(host, port, self.factory)

    def disconnect(self):
        log.msg("Disconnecting")
        self.connection.disconnect()

    def setUiState(self, state):
        connected_controls = ('btn_disconnect', 'rb_js_enable', 'rb_js_disable',
            'tb_estop', 'tb_calibrate', 'imi_calibration')
        if state == 'connecting':
            self.btn_disconnect.set_sensitive(True)
            self.btn_connect.set_sensitive(False)
        elif state == 'connected':
            for control in connected_controls:
                self.builder.get_object(control).set_sensitive(True)
        elif state == 'disconnected':
            if self.joystick_enabled:
                self.rb_js_enable.set_active(False)
                self.rb_js_disable.set_active(True)
                self.disableJoystick()
            for control in connected_controls:
                self.builder.get_object(control).set_sensitive(False)
                self.btn_connect.set_sensitive(True)

    def enableJoystick(self):
        self.joystick_enabled = True
        try:
            self.joystick = Joystick(1)
        except:
            self.joystick_enabled = False
            self.rb_js_enable.set_active(True)
            self.rb_js_disable.set_active(False)
            self.statusbar.push(self.context_id, 'Joystick device error')
            return
        self.js_handler = self.joystick.connect('axis', self.axis_event)

    def disableJoystick(self):
        self.joystick_enabled = False
        if self.joystick is not None:
            self.joystick.disconnect(self.js_handler)
            self.joystick.shutdown()
            self.joystick = None

    def onStartConnection(self):
        self.setUiState('connecting')

    def onConnect(self):
        self.statusbar.remove_all(self.context_id)
        self.statusbar.push(self.context_id, 'Connected')
        self.setUiState('connected')

    def onConnectionLost(self):
        self.setUiState('disconnected')
        self.statusbar.remove_all(self.context_id)
        self.statusbar.push(self.context_id, 'Disconnected')

    def onConnectionFailed(self, reason):
        self.setUiState('disconnected')
        self.statusbar.remove_all(self.context_id)
        self.statusbar.push(self.context_id, 'Connection failed!')

    def onUpdateAxis(self):
        if self.joystick_x != 0:
            self.eb_js_x.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color('#00FF00'))
        elif self.joystick_x == 0:
            self.eb_js_x.modify_bg(gtk.STATE_NORMAL, None)
        if self.joystick_y != 0:
            self.eb_js_y.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color('#00FF00'))
        elif self.joystick_y == 0:
            self.eb_js_y.modify_bg(gtk.STATE_NORMAL, None)

        self.label_js_x.set_label(str(self.joystick_x))
        self.label_js_y.set_label(str(self.joystick_y))
        self.factory.control.send_joystick_command(self.joystick_x, self.joystick_y)

    def onStatusUpdate(self, status, xpos, ypos, xval, yval):
        moving = status & 0x10
        if moving:
            self.label_drivestatus.set_label("MOVING")
            self.eb_drivestatus.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color('#00FF00'))
        else:
            self.label_drivestatus.set_label("STOPPED")
            self.eb_drivestatus.modify_bg(gtk.STATE_NORMAL, None)
        self.label_drive_x.set_label(str(xpos))
        self.label_drive_y.set_label(str(ypos))
        self.label_raw_x.set_label(str(xval))
        self.label_raw_y.set_label(str(yval))

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

    def on_rb_js_enable_toggled(self, btn):
        if btn.get_active():
            self.enableJoystick()
        else: 
            self.disableJoystick()

    def on_tb_estop_clicked(self, btn):
        self.factory.control.send_estop_command()

    def on_tb_reset_clicked(self, btn):
        self.factory.control.send_reset_command()

    def axis_event(self, object, axis, value, init):
        if init == 128:
            # Ignore this event. One gets sent per axis when the joystick
            # is initialized. I should really find out why.
            return
        if axis == 0:
            # dividing by 256 scales the value to fit within a signed char
            self.prev_x = self.joystick_x
            self.joystick_x = value / 256
            if self.joystick_x == self.prev_x:
                return
        if axis == 1:
            # this axis needs to be inverted
            self.prev_y = self.joystick_y
            self.joystick_y = -value / 256
            if self.joystick_y == self.prev_y:
                return
        self.onUpdateAxis()

    def button_event(self, object, button, value, init):
        pass

AzathothClient()
reactor.run()
