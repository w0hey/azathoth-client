import gtk

from gtkmvc import View

class BarView(View):
    
    def __init__(self, parent):
        View.__init__(self)
        manager = gtk.UIManager()
        driveView = parent.driveView

        manager.insert_action_group(parent['actgrp_main'])
        manager.insert_action_group(driveView['actgrp_drive'])
        manager.add_ui_from_file("ui.xml")

        vb = gtk.VBox()
        menubar = manager.get_widget("/menubar")
        toolbar = manager.get_widget("/toolbar")
        vb.pack_start(menubar)
        vb.pack_start(toolbar)
        self['vbox_bars'] = vb
        self.top = 'vbox_bars'
        vb.show_all()
