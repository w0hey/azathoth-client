import gtk

from gtkmvc import View

from driveview import DriveView
from jsview import JsView

class MainView(View):
    builder = "main.glade"
    top = "window_main"

    def __init__(self):
        View.__init__(self)
        self.driveView = DriveView()
        self['vbox_sidebar_left'].pack_start(self.driveView.get_top_widget())
        self['hsep'] = gtk.HSeparator()
        self['vbox_sidebar_left'].pack_start(self['hsep'])
        self.jsView = JsView()
        self['vbox_sidebar_left'].pack_start(self.jsView.get_top_widget())
    
    def setConnectState(self, state):
        connected_controls = ('btn_disconnect', 'tb_estop', 'tb_reset', 'tb_calibrate',
            'imi_calibration')
        if state == 'connecting':
            self['btn_disconnect'].set_sensitive(True)
            self['btn_connect'].set_sensitive(False)
        elif state == 'connected':
            for control in connected_controls:
                self[control].set_sensitive(True)
                self.jsView.setSensitive(True)
                self.driveView.setSensitive(True)
        elif state == 'disconnected':
            for control in connected_controls:
                self[control].set_sensitive(False)
                self['btn_connect'].set_sensitive(True)
                self.jsView.setSensitive(False)
                self.driveView.setSensitive(False)
