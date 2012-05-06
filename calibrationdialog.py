import pygtk
pygtk.require('2.0')
import gtk

from twisted.python import log

class CalibrationDialog:
    def __init__(self, app):
        self.app = app
        self.builder = gtk.Builder()
        self.builder.add_from_file('calibrate.glade')
        self.dialog = self.builder.get_object('dialog_calibration')

        self.builder.connect_signals(self)

        self.label_x_cur = self.builder.get_object('label_x_cur')
        self.label_y_cur = self.builder.get_object('label_y_cur')
        self.label_x_eeprom = self.builder.get_object('label_x_eeprom')
        self.label_y_eeprom = self.builder.get_object('label_y_eeprom')
        self.hscale_x = self.builder.get_object('hscale_x')
        self.hscale_y = self.builder.get_object('hscale_y')
        self.adj_x = self.builder.get_object('adj_x')
        self.adj_y = self.builder.get_object('adj_y')
        self.chkbtn_store = self.builder.get_object('chkbtn_store')

        self.dialog.show_all()
        d = self.app.factory.control.req_cal_values()
        d.addCallback(self.onReceiveInitialCalibration)
        d.addCallback(self.onReceiveCalibration)

    def onReceiveInitialCalibration(self, d):
        self.initial_x = d['current_x']
        self.initial_y = d['current_y']
        return d

    def onReceiveCalibration(self, d):
        self.current_x = d['current_x']
        self.current_y = d['current_y']
        self.label_x_cur.set_label(str(self.current_x))
        self.label_y_cur.set_label(str(self.current_y))
        self.label_x_eeprom.set_label(str(d['eeprom_x']))
        self.label_y_eeprom.set_label(str(d['eeprom_y']))
        self.adj_x.set_value(self.current_x)
        self.adj_y.set_value(self.current_y)
        return d

    def on_dialog_calibration_response(self, dlg, response):
        if response == gtk.RESPONSE_OK:
            if self.chkbtn_store.get_active():
                self.app.factory.control.cmd_cal_store()
            self.dialog.destroy()
        if response == gtk.RESPONSE_CANCEL:
            if self.current_x == self.initial_x and self.current_y == self.initial_y:
                self.dialog.destroy()
            else:
                self.app.factory.control.send_cal_values(self.initial_x, self.initial_y)
                self.dialog.destroy()
        pass

    def on_adj_x_value_changed(self, adj):
        self.current_x = int(adj.get_value())
        self.app.factory.control.send_cal_values(self.current_x, self.current_y)

    def on_adj_y_value_changed(self, adj):
        self.current_y = int(adj.get_value())
        self.app.factory.control.send_cal_values(self.current_x, self.current_y)
