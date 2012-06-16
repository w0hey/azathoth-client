import gtk

from gtkmvc import Controller
from gtkmvc.adapters import Adapter

class CalibrationController(Controller):
    
    def __init__(self, model, view):
        Controller.__init__(self, model, view)

    def register_view(self, view):
        #self.model.requestCalibration()
        a = Adapter(self.model, 'cal_current_x')
        a.connect_widget(self.view['adj_x'])
        self.adapt(a)

        a = Adapter(self.model, 'cal_current_y')
        a.connect_widget(self.view['adj_y'])
        self.adapt(a)

        a = Adapter(self.model, 'cal_eeprom_x')
        a.connect_widget(self.view['lbl_eeprom_x'])
        self.adapt(a)

        a = Adapter(self.model, 'cal_eeprom_y')
        a.connect_widget(self.view['lbl_eeprom_y'])
        self.adapt(a)
