import gtk

from gtkmvc import View

class CalibrationView(View):
    builder = "calibrate.glade"
    top = "dialog_calibration"
    
    def run(self):
        w = self.get_top_widget()
        result = w.run()
        w.destroy()
        return result
