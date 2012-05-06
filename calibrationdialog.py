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

        self.dialog.show_all()
        d = self.app.factory.control.req_cal_values()
        d.addCallback(self.onReceiveInitialCalibration)
        d.addCallback(self.onReceiveCalibration)

    def onReceiveInitialCalibration(self, d):
        self.initial_x = d['current_x']
        self.initial_y = d['current_y']
        return d

    def onReceiveCalibration(self, d):
        self.label_x_cur.set_label(str(d['current_x']))
        self.label_y_cur.set_label(str(d['current_y']))
        self.label_x_eeprom.set_label(str(d['eeprom_x']))
        self.label_y_eeprom.set_label(str(d['eeprom_y']))
        self.adj_x.set_value(d['current_x'])
        self.adj_y.set_value(d['current_y'])
        return d

    def on_dialog_calibration_response(self, dlg, response):
        pass

    def on_adj_x_value_changed(self, adj):
        pass

    def on_adj_y_value_changed(self, adj):
        pass
