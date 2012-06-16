import gtk

from gtkmvc import View

from views.driveview import DriveView
from views.jsview import JsView
from views.barview import BarView
from views.videoview import VideoView

class MainView(View):
    builder = "main.glade"
    top = "window_main"

    def __init__(self):
        View.__init__(self)
        self.driveView = DriveView()
        self['vbox_sidebar_left'].pack_start(self.driveView.get_top_widget())
        self['hsep'] = gtk.HSeparator()
        self['hsep'].show_all()
        self['vbox_sidebar_left'].pack_start(self['hsep'])
        self.jsView = JsView()
        self['vbox_sidebar_left'].pack_start(self.jsView.get_top_widget())
        self.videoView = VideoView()
        self['hbox1'].pack_start(self.videoView.get_top_widget())
        self['hbox1'].reorder_child(self.videoView.get_top_widget(), 1)
        self.barView = BarView(self)
        self['vbox_main'].pack_start(self.barView.get_top_widget())
        self['vbox_main'].reorder_child(self.barView.get_top_widget(), 0)
    
    def setConnectState(self, state):
        if state == 'connecting':
            self['btn_disconnect'].set_sensitive(True)
            self['btn_connect'].set_sensitive(False)
        elif state == 'connected':
            self['btn_disconnect'].set_sensitive(True)
            self['btn_connect'].set_sensitive(False)
            self.jsView.setSensitive(True)
            self.driveView.setSensitive(True)
        elif state == 'disconnected':
            self['btn_connect'].set_sensitive(True)
            self['btn_disconnect'].set_sensitive(False)
            self.jsView.setSensitive(False)
            self.driveView.setSensitive(False)
