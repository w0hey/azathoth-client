import gtk
from gtkmvc import Controller
from gtkmvc.adapters import Adapter

class DriveController(Controller):
    
    def register_view(self, view):
        pass

    def register_adapters(self):
        a = Adapter(self.model, 'estop_act')
        a.connect_widget(self.view['label_estop_act'], setter=self.estop_setter)
        self.adapt(a)
        
        a = Adapter(self.model, 'estop_cmd')
        a.connect_widget(self.view['label_estop_cmd'], setter=self.estop_setter)
        self.adapt(a)
        
        a = Adapter(self.model, 'select_act')
        a.connect_widget(self.view['label_select_act'], setter=self.select_setter)
        self.adapt(a)

        a = Adapter(self.model, 'select_cmd')
        a.connect_widget(self.view['label_select_cmd'], setter=self.select_setter)
        self.adapt(a)

        a = Adapter(self.model, 'moving')
        a.connect_widget(self.view['label_drivestatus'], setter=self.drivestatus_setter)
        self.adapt(a)


    def on_btn_select_clicked(self, btn):
        self.model.select()

    def on_btn_deselect_clicked(self, btn):
        self.model.deselect()

    def on_estop_activate(self, action):
        self.model.estop()

    def on_reset_activate(self, action):
        self.model.reset()

    def on_calibrate_activate(self, action):
        #TODO
        pass

    # special setters
    def estop_setter(self, wid, val):
        if val == 'RUN':
            color = gtk.gdk.Color('#00FF00')
        elif val == 'STOP':
            color = gtk.gdk.Color('#FF0000')
        else:
            color = None
        wid.set_label(val)

        if wid == self.view['label_estop_act']: 
            eb = self.view['eb_estop_act']
        else:
            eb = self.view['eb_estop_cmd']
        eb.modify_bg(gtk.STATE_NORMAL, color)

    def select_setter(self, wid, val):
        if val == 'ROBOT':
            color = gtk.gdk.Color('#00FF00')
        elif val == 'CHAIR':
            color = gtk.gdk.Color('#00FFFF')
        else:
            color = None
        wid.set_label(val)
        
        if wid == self.view['label_select_act']:
            eb = self.view['eb_select_act']
        else:
            eb = self.view['eb_select_cmd']
        eb.modify_bg(gtk.STATE_NORMAL, color)
    
    def drivestatus_setter(self, wid, val):
        if val == 'MOVING':
            color = gtk.gdk.Color('#00FF00')
        else:
            color = None
        wid.set_label(val)
        self.view['eb_drivestatus'].modify_bg(gtk.STATE_NORMAL, color)

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

