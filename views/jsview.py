import gtk

from gtkmvc import View

class JsView(View):
    builder = "jsview.glade"
    top = "vbox_joystick"

    def setSensitive(self, sensitive):
        self['rb_js_enable'].set_sensitive(sensitive)
        self['rb_js_disable'].set_sensitive(sensitive)
