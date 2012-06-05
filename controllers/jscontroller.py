import logging

import gtk
from gtkmvc import Controller
from gtkmvc.adapters import Adapter

from joystick import Joystick

class JsController(Controller):
    
    def __init__(self, model, view):
        Controller.__init__(self, model, view)
        self.joystick = None
        self.joystick_x = 0
        self.joystick_y = 0

    def register_view(self, view):
        pass

    def register_adapters(self):
        a = Adapter(self.model, 'joy_x')
        a.connect_widget(self.view['label_js_x'], setter=self.joystick_setter)
        self.adapt(a)

        a = Adapter(self.model, 'joy_y')
        a.connect_widget(self.view['label_js_y'], setter=self.joystick_setter)
        self.adapt(a)

    def enableJoystick(self):
        logging.debug('enableJoystick')
        self.joystick_enabled = True
        try:
            self.joystick = Joystick(1)
        except:
            self.joystick_enabled = False
            #self.view['rb_js_enable'].set_active(False)
            #self.view['rb_js_disable'].set_active(True)
            logging.error('could not enable joystick')
            return
        self.jsAxisHandler = self.joystick.connect('axis', self.on_axis_event)
        self.jsButtonHandler = self.joystick.connect('button', self.on_button_event)

    def disableJoystick(self):
        self.joystick_enabled = False
        #self.view['rb_js_enable'].set_active(True)
        #self.view['rb_js_disable'].set_active(False)
        if self.joystick is not None:
            self.joystick.disconnect(self.jsAxisHandler)
            self.joystick.disconnect(self.jsButtonHandler)
            self.joystick = None

    # signal handlers
    def on_rb_js_enable_toggled(self, btn):
        logging.debug('on_rb_js_enable_toggled')
        if btn.get_active():
            self.enableJoystick()
        else:
            self.disableJoystick()

    def on_tb_calibrate_clicked(self, btn):
        #TODO
        pass

    def on_axis_event(self, object, axis, value, init):
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
        elif axis == 1:
            # this axis needs to be inverted
            self.prev_y = self.joystick_y
            self.joystick_y = -value / 256
            if self.joystick_y == self.prev_y:
                return
        else: # ignore other axises
            logging.debug("unexpected axis event - axis %d" % axis)
            return
        self.model.driveModel.joystickCommand(self.joystick_x, self.joystick_y)

    def on_button_event(self, object, button, value, init):
        pass

    # special setters
    def joystick_setter(self, wid, val):
        if val != 0:
            color = gtk.gdk.Color('#00FF00')
        else:
            color = None
        wid.set_label(str(val))
        if wid == self.view['label_js_x']:
            self.view['eb_js_x'].modify_bg(gtk.STATE_NORMAL, color)
        else:
            self.view['eb_js_y'].modify_bg(gtk.STATE_NORMAL, color)

