import gtk

from gtkmvc import View

class DriveView(View):
    builder = "driveview.glade"
    top = "table_drive"

    def setSensitive(self, sensitive):
        self['btn_select'].set_sensitive(sensitive)
        self['btn_deselect'].set_sensitive(sensitive)
        self['actgrp_drive'].set_sensitive(sensitive)
        
