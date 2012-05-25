import gtk

from gtkmvc import View

class MainView (View):
    builder = "main.glade"
    top = "window_main"
    
    def setConnectState(self, state):
        connected_controls = ('btn_disconnect', 'rb_js_enable', 'rb_js_disable',
            'btn_select', 'btn_deselect', 'tb_estop', 'tb_reset', 'tb_calibrate',
            'imi_calibration')
        if state == 'connecting':
            self['btn_disconnect'].set_sensitive(True)
            self['btn_connect'].set_sensitive(False)
        elif state == 'connected':
            for control in connected_controls:
                self[control].set_sensitive(True)
        elif state == 'disconnected':
            for control in connected_controls:
                self[control].set_sensitive(False)
                self['btn_connect'].set_sensitive(True)
